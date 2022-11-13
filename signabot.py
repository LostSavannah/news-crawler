import json
import sqlite3
import requests
import os
from time import time, sleep, strftime
from typing import Any, Dict, List
from miner.parsing import Parser, Tag
from uuid import uuid4

os.system('TITLE Signabot')

class Signabot:
    def __init__(self, config:str, database:str) -> None:
        self.config = config
        self.database = database

    def log(self, data, isError:bool = False) -> None:
        moment:str = strftime('%d-%m-%Y %H:%M:%S')
        params = (moment, time(), data, isError)
        with sqlite3.connect(self.database) as connection:
            connection.execute('INSERT INTO Logs VALUES (?, ?, ?, ?);', params) 
            connection.commit()

    def get_routes_from(self, url:str) -> List[str]:
        self.log(f'Retrieving current signature from: {url}')
        routes:List[str] = []
        def on_data(data:str, tags:List[Tag]):
            nonlocal routes
            routes.append('/'.join([str(i) for i in tags]))
        Parser(on_data).feed(requests.get(url).text)
        return routes.copy()

    def save_signature(self, url:str, signature:List[str]) -> None:
        signatureStr:str = json.dumps(signature)
        with sqlite3.connect(self.database) as connection:
            params = (str(uuid4()), url, signatureStr, time())
            connection.execute('INSERT INTO Signatures VALUES (?, ?, ?, ?);', params) 
            connection.commit()

    def update_signature(self, signature):
        url:str = signature[0]
        routes:List[str] = self.get_routes_from(url)
        self.log(f'Updating current signature from: {url}')
        self.save_signature(url, routes) 
        self.update_configured_signature_last_run(signature)  

    def get_configured_signatures(self) -> List[Any]:        
        with sqlite3.connect(self.database) as connection:
            query:str = 'SELECT * FROM ConfiguredSignatures;'
            c = connection.cursor().execute(query)
            data = c.fetchone()
            while data is not None:
                yield data
                data = c.fetchone()

    def update_configured_signature_last_run(self, signature):
        url, update, next, tags = signature
        next = update + time()
        query = 'UPDATE ConfiguredSignatures SET nextUpdateEpoch = ? where url = ?;'
        with sqlite3.connect(self.database) as connection:
            connection.execute(query, (next, url))
            connection.commit()

    def start(self):
        active:bool = True
        while active:
            waitInterval:float = 5
            try:
                for signature in self.get_configured_signatures():
                    if time() > signature[2]:
                        self.update_signature(signature)
                sleep(waitInterval)
            except KeyboardInterrupt:
                self.log("User requested exit")
                active = False
            except Exception as e:
                self.log(e, True)


Signabot('./config/signabot.json', './database/signatures.db').start()