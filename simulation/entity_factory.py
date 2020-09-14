from __future__ import annotations

import colors
from simulation.components.player import Player
from simulation.components.position import Position
from simulation.components.renderable import Renderable
from simulation.components.name import Name
from simulation.entity import Entity


def player_ship() -> Entity:
    e = Entity()
    e.add_component(Player())
    e.add_component(Position(0, 0))
    e.add_component(Renderable("@", colors.OBJECT_PLAYER))
    e.add_component(Name("[PLR-12345] Player ship"))
    return e

def asteroid() -> Entity:
    e = Entity()
    e.add_component(Renderable("#", colors.OBJECT_JUNK))
    e.add_component(Name("Asteroid"))
    return e
