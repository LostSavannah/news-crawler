from html.parser import HTMLParser
from typing import Callable, List, Tuple

class HtmlNode:
    def __init__(self) -> None:
        pass

class Tag:
    def __init__(self, tagName:str, attr:List[Tuple[str, str]]) -> None:
        self.tagName = tagName
        self.className:str = dict(attr).get('class', None) 
        pass

    def __str__(self) -> str:
        if self.className is not None:
            return f'{self.tagName}[@class={self.className}]'
        else:
            return self.tagName


OnData = Callable[[str, List[Tag]], None]

class Parser(HTMLParser):
    def __init__(self, onData:OnData, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.path:List[Tag] = []
        self.onData = onData

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        self.path.append(Tag(tag, attrs))

    def handle_endtag(self, tag: str) -> None:
        while self.path.pop().tagName != tag:
            pass

    def handle_data(self, data: str) -> None:
        self.onData(data, self.path.copy())