from typing import Optional
from simulation.components.component import Component


class Acceleration(Component):

    def __init__(self, x: Optional[float] = 0, y: Optional[float] = 0, max_acceleration: Optional[float] = 0):
        self.x = x
        self.y = y
        self.max_acceleration = max_acceleration