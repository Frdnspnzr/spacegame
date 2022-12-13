from typing import Dict
from simulation.components.component import Component
import behaviours


class Behaviour(Component):

    def __init__(self):
        self.behaviours = list()

    def toDict(self):
        d = dict({"behaviours": dict()})
        for b in self.behaviours:
            d["behaviours"][type(b).__name__] = b.toDict()
        return d

    def fromDict(self, dictionary, id_mapping: Dict[int, int] = dict()):
        for (name, data) in dictionary["behaviours"].items():
            behaviour = getattr(behaviours, name)()
            behaviour.fromDict(data, id_mapping)
            self.behaviours.append(behaviour)