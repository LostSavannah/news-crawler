from miner.pattern import PatternFinder
from typing import List


lines:List[str] = []
with open('routes.txt', 'r', encoding='latin-1') as f:
    lines = [i.strip() for i in f.readlines()]

p:PatternFinder = PatternFinder(lines)

print(p.get_patterns())