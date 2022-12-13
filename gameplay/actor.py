from functools import reduce
from typing import Callable, List

from gameplay.equipment import Equipment
from gameplay.attribute import Attribute, Stacking
from gameplay.item import Item
from utility.saveable import Saveable


class Actor(Saveable):

    def __init__(self):

        self.inventory: List[Item] = list()
        self.equipped: List[Equipment] = list()

    def get_attribute(self, attribute: Attribute) -> float:
        return reduce(self.__get_reduce_function(attribute), map(lambda e: e.get_attribute(attribute), self.equipped))

    def __get_reduce_function(self, attribute: Attribute) -> Callable[[float, float], float]:
        if attribute.get_stacking() is Stacking.ADDITIVE:
            return lambda a, b: a + b
        else:
            return lambda a, b: a * b

    def toDict(self):
        return dict({
            "inventory": [i.toDict() for i in self.inventory],
            "equipped": [e.toDict() for e in self.equipped]
        })

    def fromDict(self, dict):
        for i in dict["inventory"]:
            item = Item()
            item.fromDict(i)
            self.inventory.append(item)
        for e in dict["equipped"]:
            equipment = Equipment()
            equipment.fromDict(e)
            self.equipped.append(equipment)
