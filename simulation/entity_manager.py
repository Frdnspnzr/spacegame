from typing import Optional

from simulation.components.player import Player
from simulation.entity import Entity


class EntityManager:

    def __init__(self):
        self.entities = []
        self.player = None

    def update(self, delta: float) -> None:
        for e in self.entities:
            e.update(delta)

    def add(self, entity: Entity) -> None:
        self.entities.append(entity)

    def get_player(self) -> Optional[Entity]:
        for e in self.entities:
            if e.has_component(Player):
                return e
