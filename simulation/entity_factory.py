from __future__ import annotations

import colors
from simulation.components.player import Player
from simulation.components.position import Position
from simulation.components.renderable import Renderable
from simulation.components.name import Name
import esper


def player_ship(world: esper.World) -> int:
    return world.create_entity(
        Player(),
        Position(0, 0),
        Renderable("@", colors.OBJECT_PLAYER),
        Name("[PLR-12345] Player ship")
    )

def asteroid(world: esper.World) -> int:
    return world.create_entity(
        Renderable("#", colors.OBJECT_JUNK),
        Name("Asteroid")
    )
