from __future__ import annotations
from simulation.components.selectable import Selectable

import esper

import colors
from simulation.components.velocity import Velocity
from simulation.components.player import Player
from simulation.components.position import Position
from simulation.components.renderable import Renderable
from simulation.components.name import Name

asteroid_counter = 0

def player_ship(world: esper.World) -> int:
    return world.create_entity(
        Player(),
        Position(0, 0),
        Renderable("@", colors.OBJECT_PLAYER),
        Selectable(),
        Name("Player ship", "PLR-12345")
    )

def asteroid(world: esper.World) -> int:
    global asteroid_counter
    asteroid_counter += 1
    return world.create_entity(
        Renderable("#", colors.OBJECT_JUNK),
        Selectable(),
        Name("Asteroid", f"AST-{asteroid_counter:05d}")
    )
