import tcod
import esper

import colors
from simulation.components.renderable import Renderable
from simulation.components.name import Name
from tcod.console import Console


class Sidebar(tcod.event.EventDispatch[None]):

    def __init__(self, world:  esper.World):
        self.world = world

    def render(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        self._render_header(console, x, y)
        console.print(x, y+1, "∙"*width)
        self._render_entity_list(console, x, y+2, width, height - 2)

    def ev_keyup(self, event: tcod.event.KeyDown) -> None:
        pass

    def _render_header(self, console: Console, x: int, y: int) -> None:
        console.print(x, y, "RANGE: ", colors.TEXT_DEFAULT)
        console.print(x + 7, y, "[SCREEN]", colors.RANGE_SCREEN)
        console.print(x + 15, y, " FILTER:", colors.TEXT_DEFAULT)
        console.print(x + 24, y, "[ALL   ]",  colors.FILTER_ALL)

    def _render_entity_list(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        line = 0
        first = True
        for _, (entity_renderable, entity_name) in self.world.get_components(Renderable, Name):
            if first:
                console.print(x+1, y+line, "►", colors.TEXT_DEFAULT)
                first = False
            console.print(x+3, y+line, entity_name.name, entity_renderable.color)
            line = line + 1
            if line > height:
                break
