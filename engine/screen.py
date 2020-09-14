from typing import Tuple

from simulation.entity_manager import EntityManager
from simulation.components.player import Player
from simulation.components.position import Position
from simulation.components.renderable import Renderable
from tcod.console import Console


class Screen:

    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager

    def render_main(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        if self.entity_manager.get_player() is None:
            return
        player_position = self.entity_manager.get_player().get_component(Position)

        mid_x = x + width // 2
        mid_y = x + height // 2
        for e in self.entity_manager.entities:
            entity_position = e.get_component(Position)
            diff_x = entity_position.x - player_position.x
            diff_y = entity_position.y - player_position.y
            pos_x = mid_x + diff_x
            pos_y = mid_y + diff_y

            if pos_x >= x and pos_y >= y and pos_x <= x + width and pos_y <= y + height:
                entity_renderable = e.get_component(Renderable)
                xx = mid_x + diff_x
                yy = mid_y + diff_y
                if (e.has_component(Player)):
                    console.print(mid_x + diff_x, mid_y + diff_y, entity_renderable.char, entity_renderable.color, (50, 50, 50))
                else:
                    console.print(mid_x + diff_x, mid_y + diff_y, entity_renderable.char, entity_renderable.color)

    def render_console(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        pass
