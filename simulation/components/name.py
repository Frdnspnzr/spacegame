from simulation.component import Component


class Name(Component):

    def __init__(self, name: str):
        super().__init__()
        self.name = name