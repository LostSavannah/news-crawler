import requests
from typing import List
from miner.parsing import Parser, Tag

with open('routes.txt', 'w', encoding='latin-1') as f:
    def on_data(data:str, tags:List[Tag]):
        line = '/'.join([str(i) for i in tags]) + '\n'
        f.write(line)
    Parser(on_data).feed(requests.get('https://hoy.com.do/').text)