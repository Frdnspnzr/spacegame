import colors
from simulation.components.player import Player
from simulation.components.position import Position
from simulation.components.renderable import Renderable
from simulation.components.selectable import Selectable
from tcod import Console
from ui.screen import Screen


class SpaceView(Screen):

    def _render_self(self, console: Console):
        player = self.__get_player()
        if not player:
            return

        player_position = self.world.component_for_entity(player, Position)

        mid_x = self.x + self.width // 2
        mid_y = self.x + self.height // 2
        for e, (entity_position, entity_renderable, entity_selectable) in self.world.get_components(Position, Renderable, Selectable):
            diff_x = entity_position.x - player_position.x
            diff_y = entity_position.y - player_position.y
            pos_x = mid_x + diff_x
            pos_y = mid_y + diff_y

            background_color = colors.BACKGROUND_CLEAR

            if entity_selectable.selected_main:
                background_color = colors.BACKGROUND_SELECTED_MAIN

            if pos_x >= self.x and pos_y >= self.y and pos_x <= self.x + self.width and pos_y <= self.y + self.height:
                console.print(mid_x + diff_x, mid_y + diff_y, entity_renderable.char,
                              entity_renderable.color, background_color)

    def __get_player(self) -> int:
        for e, player in self.world.get_components(Player):
            return e
