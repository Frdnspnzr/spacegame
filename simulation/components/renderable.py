from typing import Tuple

from simulation.component import Component


class Renderable(Component):

    def __init__(self, char: str, color: Tuple[int, int, int]):
        super().__init__()
        self.char = char
        self.color = color