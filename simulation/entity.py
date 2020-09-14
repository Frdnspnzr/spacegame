from typing import Tuple, Optional

from simulation.component import Component


class Entity:

    def __init__(self):
        self.components = []

    def update(self, delta: float) -> None:
        pass

    def add_component(self, component: Component):
        self.components.append(component)
        component.entities.append(self)

    def has_component(self, t) -> bool:
        for c in self.components:
            if type(c) is t:
                return True
        return False

    def get_component(self, t) -> Optional[Component]:
        for c in self.components:
            if type(c) is t:
                return c