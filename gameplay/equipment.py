from typing import Optional

from gameplay.attribute import Attribute
from gameplay.attribute import Stacking
from gameplay.weapon import Weapon
from gameplay.item import Item
from utility.saveable import Saveable


class Equipment(Item, Saveable):

    def __init__(self):
        self.attributes = dict()

    def get_attribute(self, attribute: Attribute) -> float:
        if attribute in self.attributes:
            return self.attributes[attribute]
        elif attribute.get_stacking is Stacking.MULTIPLICATIVE:
            return 1
        else:
            return 0

    def provides_weapon(self) -> Optional[Weapon]:
        return None


    def fromDict(self, dictionary):
        super().fromDict(dictionary)
        self.attributes = dict()
        for (key, value) in dictionary["attributes"].items():
            self.attributes[Attribute(int(key))] = value