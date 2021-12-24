from __future__ import annotations

import colors
import esper
from engine import engine

from simulation.components.acceleration import Acceleration
from simulation.components.behaviour import Behaviour
from simulation.components.damageable import Damageable
from simulation.components.destructable import Destructable
from simulation.components.GameplayActor import GameplayActor
from simulation.components.name import Name
from simulation.components.player import Player
from simulation.components.position import Position
from simulation.components.renderable import Renderable
from simulation.components.selectable import Selectable
from simulation.components.velocity import Velocity

from gameplay.data import templates

asteroid_counter = 0

def player_ship(world: esper.World) -> int:
    return world.create_entity(
        Player(),
        Position(0, 0),
        Renderable("@", colors.OBJECT_PLAYER),
        Velocity(0, 0),
        Acceleration(0, 0, 0.001),
        Selectable(),
        Destructable(1000, 1000, 1000),
        Damageable(),
        Behaviour(),
        Name("Player ship", "PLR-12345"),
        GameplayActor(templates.get("template:player"))
    )

def asteroid(world: esper.World) -> int:
    global asteroid_counter
    asteroid_counter += 1
    return world.create_entity(
        Renderable("#", colors.OBJECT_JUNK),
        Selectable(),
        Destructable(20, 100, 0),
        Velocity(0, 0),
        Name("Asteroid", f"AST-{asteroid_counter:05d}")
    )

def enemy_fighter(world: esper.World) -> int:
    return world.create_entity(
        Position(10, 10),
        Renderable("V", colors.OBJECT_ENEMY),
        Velocity(0, 0),
        Acceleration(0, 0, 0.001),
        Selectable(),
        Destructable(10, 20, 20),
        Damageable(),
        Behaviour(),
        Name("Some wanker", "WNK-80085")
    )
