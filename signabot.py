import json
import sqlite3
import requests
import os
from time import time, sleep, strftime
from typing import List
from miner.parsing import Parser, Tag
from uuid import uuid4

configPath:str = './config/signabot.json'
database:str = './database/signatures.db'

os.system('TITLE Signabot')

def log(data:str, isError:bool = False):
    moment:str = strftime('%d-%m-%Y %H:%M:%S')
    print(f'[{moment}] {data}')

def get_routes_from(url:str) -> List[str]:
    log(f'Retrieving current signature from: {url}')
    routes:List[str] = []
    def on_data(data:str, tags:List[Tag]):
        nonlocal routes
        routes.append('/'.join([str(i) for i in tags]))
    Parser(on_data).feed(requests.get(url).text)
    return routes.copy()

def save_signature(url:str, signature:List[str]) -> None:
    signatureStr:str = json.dumps(signature)
    with sqlite3.connect(database) as connection:
        params = (str(uuid4()), url, signatureStr, time())
        connection.execute('INSERT INTO Signatures VALUES (?, ?, ?, ?);', params) 
        connection.commit()

def update_signature(signature):
    url:str = signature["url"]
    updateIntervalSeconds:int = signature["updateIntervalSeconds"]
    signature["nextUpdateEpoch"] = updateIntervalSeconds + time()
    routes:List[str] = get_routes_from(url)
    log(f'Updating current signature from: {url}')
    save_signature(url, routes)

with open(configPath, 'r+', encoding='latin-1') as file:
    active:bool = True
    while active:
        file.seek(0)
        config = json.load(file)
        waitInterval:float = config["config"]["waitIntervalSeconds"]
        try:
            for signature in config["urls"]:
                if time() > signature["nextUpdateEpoch"]:
                    update_signature(signature)
            log(f'waiting {waitInterval} seconds...')
            sleep(waitInterval)
        except KeyboardInterrupt:
            log("User requested exit")
            active = False
        except Exception as e:
            log(e)
        finally:
            file.seek(0)
            file.truncate()
            json.dump(config, file, indent=4, ensure_ascii=False)
