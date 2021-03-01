from enum import Enum

from esper import World

class BehaviourGroup(Enum):
    pass

class Behaviour(object):

    @property
    def priority(self):
        return 0

    @property
    def valid(self):
        return True

    def execute(self, world: World, entity: int):
        pass