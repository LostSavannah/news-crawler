import hashlib
import sqlite3
from typing import List, Tuple
from miner.pattern import PatternFinder
import json

database:str = './database/signatures.db'

class XqueryPathFinder:
    def __init__(self, separator:str = '>', maxRoutes:int = 10) -> None:
        self.separator = separator
        self.maxRoutes = maxRoutes

    def get_xquery_paths(self, signature:List[str]):
        p = PatternFinder(signature).with_test_routes_max(self.maxRoutes)
        p.with_separator(self.separator)
        patterns = p.get_patterns()[0:10]
        for pattern in patterns:
            routes, score = pattern
            xqueries = routes.split(self.separator)
            relative = self.get_relative(xqueries)

    def get_relative(self, queries:List[str]) -> Tuple[str, List[str]]:
        queriesLists:List[List[str]] = [i.split('/') for i in queries]
        minLength = min([len(i) for i in queriesLists])
        common:List[str] = []
        split:int = 0
        for index in range(minLength):
            commonCandidate:str = queriesLists[0][index]
            if all([i[index] == commonCandidate for i in queriesLists]):
               common.append(commonCandidate)
               split = index
            else:
                break
        queriesListsJoint = ['/'.join(i[split+1:]) for i in queriesLists]
        commonRelative:str = '/'.join(common)
        xqueries = sorted(list(set([i for i in queriesListsJoint if i != ''])))
        hash = hashlib.md5('.'.join(xqueries).encode('latin-1')).hexdigest()
        res = {"relative": commonRelative, "hash": hash, "queries":{}}
        for i in range(len(xqueries)):
            res["queries"][str(i)] = xqueries[i]
        return res

def get_signature()->List[str]:
    with sqlite3.connect(database) as connection:
        query:str = 'SELECT signature FROM Signatures LIMIT 1;'
        rawSignature:str = connection.execute(query).fetchone()[0]
        return json.loads(rawSignature)

XqueryPathFinder().get_xquery_paths(get_signature())