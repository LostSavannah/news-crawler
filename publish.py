import shutil
import os
from typing import List

path:List[str] = ["", "home", "scripts", "python", "news_crawler"]
baseFolder = os.sep.join(path)
fileName = os.sep.join([baseFolder, "log.txt"])

currentFolder:str = os.path.abspath(os.curdir)

def copio(src:str, dest:str, *, follow_symlinks=True):
    pass

def ignore(str:str, dirs:List[str]) -> List[str]:
    return [i for i in dirs if not i.startswith('.')]

shutil.copytree(currentFolder, baseFolder, dirs_exist_ok=True, ignore=ignore)