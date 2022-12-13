from typing import Dict


class Saveable():

    def toDict(self):
        return self.__dict__

    def fromDict(self, dictionary: Dict, id_mapping: Dict[int, int] = dict()):
        for (key, value) in dictionary.items():
            self.__setattr__(key, value)
