from enum import Enum
from typing import Dict, Tuple

import esper
from simulation.components.damageable import Damageable, DamageTypes
from simulation.components.destructable import Destructable
from utility.math import clamp


class DefenceTypes(Enum):
    CORE = 1
    HULL = 2
    SHIELD = 3

class ApplyDamageProcessor(esper.Processor):

    def __init__(self):
        self.__damage_matrix = self.__prepare_damage_matrix()

    def process(self, *args, **kwargs):
        for _, (destructable, damageable) in self.world.get_components(Destructable, Damageable):
            for type in DamageTypes:
                destructable.shield_current = clamp(
                    destructable.shield_current - round(damageable.instances[type] * self.__damage_matrix[type, DefenceTypes.SHIELD]),
                    0,
                    destructable.shield_max)
                destructable.hull_current = clamp(
                    destructable.hull_current - round(damageable.instances[type] * self.__damage_matrix[type, DefenceTypes.HULL]),
                    0,
                    destructable.hull_max)
                destructable.core_current = clamp(
                    destructable.core_current - round(damageable.instances[type] * self.__damage_matrix[type, DefenceTypes.CORE]),
                    0,
                    destructable.core_max)
                damageable.instances[type] = 0

    def __prepare_damage_matrix(self) -> Dict[Tuple[DamageTypes, DefenceTypes], float]:
        damage_matrix = dict()

        for defence in DefenceTypes:
            for damage in DamageTypes:
                damage_matrix[damage, defence] = 1

        damage_matrix[DamageTypes.ENERGY, DefenceTypes.HULL] = 0.66
        damage_matrix[DamageTypes.ENERGY, DefenceTypes.CORE] = 0.33

        damage_matrix[DamageTypes.PIERCING, DefenceTypes.SHIELD] = 0.33
        damage_matrix[DamageTypes.PIERCING, DefenceTypes.CORE] = 0.66

        damage_matrix[DamageTypes.KINETIC, DefenceTypes.HULL] = 0.33
        damage_matrix[DamageTypes.KINETIC, DefenceTypes.SHIELD] = 0.66

        return damage_matrix
