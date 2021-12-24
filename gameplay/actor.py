from functools import reduce
from typing import Callable, List

from gameplay.equipment import Equipment
from gameplay.attribute import Attribute, Stacking
from gameplay.item import Item


class Actor:

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
