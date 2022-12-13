from simulation.components.component import Component


class Selectable(Component):
    def __init__(self):
        self.selected_main = False
        self.selected_multi = False