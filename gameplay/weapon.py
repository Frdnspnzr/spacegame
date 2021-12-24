from enum import Enum

from gameplay.item import Item


class WeaponTypes(Enum):

    LASER = 1
    PROJECTILE = 2
    TORPEDO = 3
    PLASMA = 4


class Weapon(Item):

    def __init__(self, type: WeaponTypes, damage: int):
        self.type = type
        self.damage = damage
