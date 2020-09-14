from simulation.component import Component


class Position(Component):

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y