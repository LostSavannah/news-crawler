import shutil
import os
from typing import List

path:List[str] = ["", "scripts", "python", "news_crawler"]
baseFolder = os.sep.join(path)
fileName = os.sep.join([baseFolder, "log.txt"])

currentFolder:str = os.path.abspath(os.curdir)

def copio(src:str, dest:str, *, follow_symlinks=True):
    print(src, dest)
    return dest

def ignore(str:str, dirs:List[str]) -> List[str]:
    return [i for i in dirs if not i.startswith('.')]

shutil.copytree(currentFolder, baseFolder, copy_function=copio, dirs_exist_ok=True, ignore=ignore)