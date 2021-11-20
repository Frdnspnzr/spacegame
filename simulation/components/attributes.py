from gameplay.attribute import Attribute as GameplayAttribute

class Attributes:

    def __init__(self) -> None:
        self.attributes = dict()
        for attribute in GameplayAttribute:
            self.attributes[attribute] = 0

    def __getitem__(self, key: GameplayAttribute):
        return self.attributes[key]
