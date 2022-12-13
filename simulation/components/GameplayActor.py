from typing import Optional
from simulation.components.component import Component
from gameplay.actor import Actor

class GameplayActor(Component):

    def __init__(self, actor: Optional[Actor] = None):
        self.actor = actor

    def toDict(self):
        return dict({"actor": self.actor.toDict()})

    def fromDict(self, dict, _):
        self.actor = Actor()
        self.actor.fromDict(dict["actor"])