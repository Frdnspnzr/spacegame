from typing import Optional, Tuple

from simulation.components.component import Component

class Renderable(Component):

    def __init__(self, char: Optional[str] = "", color: Optional[Tuple[int, int, int]] = (0,0,0)):
        super().__init__()
        self.char = char
        self.color = color