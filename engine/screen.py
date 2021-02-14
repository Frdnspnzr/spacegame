from typing import Tuple

import esper
import tcod
from tcod.console import Console

import colors
from simulation.components.player import Player
from simulation.components.position import Position
from simulation.components.renderable import Renderable
from simulation.components.selectable import Selectable


class Screen:

    def __init__(self, world: esper.World):
        self.world = world

    def render_main(self, console: Console, player: int, x: int, y: int, width: int, height: int) -> None:
        if not self.world.has_component(player, Player):
            return
        player_position = self.world.component_for_entity(player, Position)

        mid_x = x + width // 2
        mid_y = x + height // 2
        for e, (entity_position, entity_renderable, entity_selectable) in self.world.get_components(Position, Renderable, Selectable):
            diff_x = entity_position.x - player_position.x
            diff_y = entity_position.y - player_position.y
            pos_x = mid_x + diff_x
            pos_y = mid_y + diff_y

            background_color = colors.BACKGROUND_CLEAR

            if entity_selectable.selected_main:
                background_color = colors.BACKGROUND_SELECTED_MAIN

            if pos_x >= x and pos_y >= y and pos_x <= x + width and pos_y <= y + height:
                console.print(mid_x + diff_x, mid_y + diff_y, entity_renderable.char, entity_renderable.color, background_color)

    def render_console(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        pass
