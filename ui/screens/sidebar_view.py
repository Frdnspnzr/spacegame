import colors
import tcod
from simulation.components.name import Name
from simulation.components.renderable import Renderable
from simulation.components.selectable import Selectable
from tcod import Console
from ui.screen import Screen


class SidebarView(Screen):

    def _render_self(self, console: Console):
        self.__render_header(console, self.x, self.y)
        console.print(self.x, self.y+1, "∙"*self.width)
        self.__render_entity_list(
            console, self.x, self.y+2, self.width, self.height - 2)

    def _handle_event(self, event: tcod.event.KeyboardEvent):

        if event.scancode is tcod.event.SCANCODE_MINUS:
            print("Scanner Reichweite wechseln")

        if event.scancode is tcod.event.SCANCODE_EQUALS:
            print("Scanner Filter wechseln")

        if event.scancode is tcod.event.SCANCODE_RIGHTBRACKET:
            speed = 1
            if event.mod & tcod.event.KMOD_SHIFT:
                speed = 5
            self.__scanner_up(speed)

        if event.scancode is tcod.event.SCANCODE_BACKSLASH:
            speed = 1
            if event.mod & tcod.event.KMOD_SHIFT:
                speed = 5
            self.__scanner_down(speed)

    def __scanner_down(self, speed=1) -> None:
        self.__move_scanner(self.entity_list, speed)

    def __scanner_up(self, speed=1) -> None:
        self.__move_scanner(reversed(self.entity_list), speed)

    def __move_scanner(self, list, speed=1) -> None:
        counter = 999999
        selectable = None
        for entity in list:
            selectable = self.world.component_for_entity(entity, Selectable)
            counter -= 1
            if counter == 0:
                selectable.selected_main = True
                break
            if selectable.selected_main:
                counter = speed
                selectable.selected_main = False
        selectable.selected_main = True

    def __render_header(self, console: Console, x: int, y: int) -> None:
        console.print(x, y, "RANGE: ", colors.TEXT_DEFAULT)
        console.print(x + 7, y, "[SCREEN]", colors.RANGE_SCREEN)
        console.print(x + 15, y, " FILTER:", colors.TEXT_DEFAULT)
        console.print(x + 24, y, "[ALL   ]",  colors.FILTER_ALL)

    def __render_entity_list(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        line = 0
        self.entity_list = []
        for entity, (entity_renderable, entity_name, entity_selectable) in self.world.get_components(Renderable, Name, Selectable):
            self.entity_list.append(entity)
            if entity_selectable.selected_main:
                console.print(x+1, y+line, "►", colors.TEXT_DEFAULT)
                first = False
            name = entity_name.formatted_name
            console.print(x+3, y+line, name, entity_renderable.color)
            line = line + 1
            if line > height:
                break
