from enum import Enum

class DamageTypes(Enum):
    KINETIC = 1
    PIERCING = 2
    ENERGY = 3

class Damageable:

    def __init__(self):
        self.instances = dict()

        for damage_type in DamageTypes:
            self.instances[damage_type] = 0