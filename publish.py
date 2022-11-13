import os
from typing import List

path:List[str] = ["", "scripts", "python", "news_crawler"]
baseFolder = os.sep.join(path)
fileName = os.sep.join([baseFolder, "log.txt"])

with open(fileName, "a", encoding='latin-1') as file:
    file.write("Hello moto")
