from gameplay.attributes import Attributes as GameplayAttributes

class Attributes:

    def __init__(self) -> None:
        self.attributes = dict()
        for attribute in GameplayAttributes:
            self.attributes[attribute] = 0

    def __getitem__(self, key: GameplayAttributes):
        return self.attributes[key]
