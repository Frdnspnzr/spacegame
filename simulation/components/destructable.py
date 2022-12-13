from typing import Optional
from simulation.components.component import Component


class Destructable(Component):

    def __init__(self, core: Optional[int] = 0, hull: Optional[int] = 0, shield: Optional[int] = 0):
        self.core_max = self.core_current = core
        self.hull_max = self.hull_current = hull
        self.shield_max = self.shield_current = shield

    @property
    def core_percentage(self) -> float:
        return self.core_current / self.core_max

    @property
    def hull_percentage(self) -> float:
        return self.hull_current / self.hull_max

    @property
    def shield_percentage(self) -> float:
        return self.shield_current / self.shield_max