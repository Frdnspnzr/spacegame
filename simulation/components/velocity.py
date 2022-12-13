from simulation.components.component import Component


class Velocity(Component):
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y