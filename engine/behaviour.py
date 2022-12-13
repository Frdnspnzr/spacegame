from enum import Enum

from esper import World

from utility.saveable import Saveable


class BehaviourGroup(Enum):
    pass

class Behaviour(Saveable):

    @property
    def priority(self) -> float:
        return 0

    @property
    def valid(self) -> bool:
        return True

    def execute(self, world: World, entity: int) -> None:
        pass
