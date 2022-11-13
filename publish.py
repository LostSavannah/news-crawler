import shutil
import os
import sys
from typing import List

path:List[str] = ["", "scripts", "python", "news_crawler"]
#path:List[str] = ["D:", "test", "copytree"]
baseFolder = os.sep.join(path)

currentFolder:str = os.path.abspath(os.curdir)

def get_files(path:str, folder:str='.', ignoreFolders:List[str] = None):
    ignoreFolders = ignoreFolders or []
    for f in os.listdir(path):
        if f in ['.', '..']: continue
        dir:str = os.sep.join([path, f])
        if os.path.isfile(dir):
            yield (path, folder, f)
        elif f in ignoreFolders:
            continue
        else:
            for r in get_files(dir, os.sep.join([folder, f]), ignoreFolders):
                yield r

def copytree(src:str, dest:str):
    for i in get_files(src, ignoreFolders=['.git', '__pycache__']):
        baseFolder, folder, file = i
        folderPaths = folder.split(os.sep)
        folderPaths[0] = dest
        destinationFolder = os.sep.join(folderPaths)
        os.makedirs(destinationFolder, exist_ok=True)
        sourceFile = os.sep.join([baseFolder, file])
        destinationFile = os.sep.join([destinationFolder, file])
        if os.path.isfile(destinationFile):
            os.unlink(destinationFile)
        shutil.copy(sourceFile, destinationFile)

copytree(currentFolder, baseFolder)