from utility.saveable import Saveable


class Item(Saveable):

    def __init__(self):
        self.name = "?"
        self.weight = 0
        self.size = 0
