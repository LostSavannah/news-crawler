from typing import Dict, List, Tuple

class PatternFinder:
    def __init__(self, routes:List[str]) -> None:
        self.routes:List[str] = routes
        self.separator:str = '>'
        self.minFrequency:int = 4
        self.minRoutes:int = 4
        self.minScore:int = 100
        self.testRoutesMax:int = 20

    def with_separator(self, separator:str):
        self.separator = separator
        return self

    def with_min_frequency(self, minFrequency:int):
        self.minFrequency = minFrequency
        return self

    def with_min_routes(self, minRoutes:int):
        self.minRoutes = minRoutes
        return self

    def with_min_score(self, minScore:int):
        self.minScore = minScore
        return self

    def with_test_routes_max(self, testRoutesMax:int):
        self.testRoutesMax = testRoutesMax
        return self

    def get_patterns(self) -> Tuple[str, int]:
        fulltext:str = self.separator.join(self.routes)
        total: int = len(self.routes)
        scores:Dict[str, Tuple[int, int]] = {}
        for start in range(total):
            for count in range(1, min(total-start, self.testRoutesMax)):
                line:str = self.separator.join(self.routes[start:start+count])
                if line in scores:
                    continue
                scores[line] = (fulltext.count(line), line.count(self.separator))
        keys:List[str] = [i for i in scores]
        for route in keys:
            freq, size = scores[route]
            if freq < self.minFrequency or size < self.minRoutes or freq * size < self.minScore:
                del scores[route]

        filtered:Tuple[str, int] = [(i, scores[i][0] * scores[i][1]) for i in scores]
        return sorted(filtered, key= lambda a: a[1], reverse=True)