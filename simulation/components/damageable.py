from enum import IntEnum
from typing import Dict

from simulation.components.component import Component


class DamageTypes(IntEnum):
    KINETIC = 1
    PIERCING = 2
    ENERGY = 3

class Damageable(Component):

    def __init__(self):
        self.instances = dict()

        for damage_type in DamageTypes:
            self.instances[damage_type] = 0

    def fromDict(self, dictionary, _):
        for damage_type in DamageTypes:
            self.instances[damage_type] = dictionary["instances"][str(damage_type.value)]