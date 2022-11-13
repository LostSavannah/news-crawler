import shutil
import os
from typing import List

path:List[str] = ["", "scripts", "python", "news_crawler"]
baseFolder = os.sep.join(path)
fileName = os.sep.join([baseFolder, "log.txt"])

foldersToCopy:List[str] = ["config", "database", "miner"]

with open(fileName, "a", encoding='latin-1') as file:
    file.write("Hello moto")


def copio(src:str, dest:str, *, follow_symlinks=True):
    pass

def ignore(str:str, dirs:List[str]) -> List[str]:
    return [i for i in dirs if not i.startswith('.')]

shutil.copytree('.', baseFolder, dirs_exist_ok=True, ignore=ignore)