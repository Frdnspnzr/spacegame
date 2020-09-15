from typing import Tuple

class Renderable():

    def __init__(self, char: str, color: Tuple[int, int, int]):
        super().__init__()
        self.char = char
        self.color = color