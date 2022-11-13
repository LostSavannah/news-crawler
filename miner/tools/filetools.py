from typing import List

def get_lines(filename:str) -> List[str]:
    with open(filename, 'r', encoding='latin-1') as f:
        for fo in f.readlines():
            yield fo.strip()
