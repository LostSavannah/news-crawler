from typing import Callable, List


class Buffer:
    def __init__(self, size:int, onBuffer:Callable[[List[str]], None]) -> None:
        self.size = size
        self.onBuffer = onBuffer
        self.array:List[str] = []

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        if len(self.array) > 0:
            self.onBuffer(self.array.copy())
            self.array.clear()

    def add(self, value:str) -> None:
        self.array.append(value)
        if len(self.array) >= self.size:
            self.onBuffer(self.array.copy())
            self.array.clear()