import colors
import tcod
from simulation.components.renderable import Renderable
from simulation.components.name import Name
from simulation.entity_manager import EntityManager
from tcod.console import Console


class Sidebar(tcod.event.EventDispatch[None]):

    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager

    def render(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        self._render_header(console, x, y)
        console.print(x, y+1, "∙"*width)
        self._render_entity_list(console, x, y+2, width, height - 2)


    def ev_keyup(event: tcod.event.KeyDown) -> None:
        pass

    def _render_header(self, console: Console, x: int, y: int) -> None:
        console.print(x, y, "RANGE: ", colors.TEXT_DEFAULT)
        console.print(x + 7, y, "[SCREEN]", colors.RANGE_SCREEN)
        console.print(x + 15, y, " FILTER:", colors.TEXT_DEFAULT)
        console.print(x + 24, y, "[ALL   ]",  colors.FILTER_ALL)

    def _render_entity_list(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        line = 0
        first = True
        for e in self.entity_manager.entities:
            entity_renderable = e.get_component(Renderable)
            entity_name = e.get_component(Name)
            if first:
                console.print(x+1, y+line, "►", colors.TEXT_DEFAULT)
                first = False
            console.print(x+3, y+line, entity_name.name, entity_renderable.color)
            line = line + 1
            if line > height:
                break
