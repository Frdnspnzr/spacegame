from typing import List, Tuple
from esper import World
import tcod
from colors import BACKGROUND_HIGHLIGHT, BACKGROUND_SELECTED_MAIN

from ui.screen import Screen
from ui.screens.consoleviews import NavigationView
from renderer import text
from ui.screens.consoleviews.scan import ScanView


class ConsoleView(Screen):

    def __init__(self, world: World):
        super().__init__(world)

    def on_add(self):
        self.__screen_list: List[Tuple[int, str, Screen]] = []
        self.__active_screen = 1

        self.__screen_list.append((1, "NAV", self.__create_navigation_screen()))
        self.__screen_list.append((2, "SCN", self.__create_scan_screen()))

    def _render_self(self, console: tcod.Console):
        self.__get_active_screen().render(console)
        self.__render_menu(console)

    def _handle_event(self, event: tcod.event.KeyboardEvent):

        self.__get_active_screen().dispatch_event(event)

        if event.type == 'KEYDOWN' and not event.repeat:
            if event.scancode == tcod.event.SCANCODE_F1:
                self.__active_screen = 1
            elif event.scancode == tcod.event.SCANCODE_F2:
                self.__active_screen = 2

    def __get_active_screen(self) -> Screen:
        for screen in self.__screen_list:
            if screen[0] == self.__active_screen:
                return screen[2]

    def __render_menu(self, console: tcod.Console):
        x = self.x
        for screen in self.__screen_list:
            color = BACKGROUND_SELECTED_MAIN if screen[0] == self.__active_screen else BACKGROUND_HIGHLIGHT
            button = f"[F{screen[0]}] {screen[1]}"
            text.with_highlighting(
                console,
                x,
                self.y + self.height - 1,
                button,
                background_color=color)
            x = x + len(button)
            text.with_highlighting(
                console,
                x,
                self.y + self.height - 1,
                " ",
                background_color=color)
            x = x + 1

    def __create_navigation_screen(self):
        view = NavigationView(self.world)
        self.__configure_screen(view)
        return view

    def __create_scan_screen(self):
        view = ScanView(self.world)
        self.__configure_screen(view)
        return view

    def __configure_screen(self, view: Screen):
        view.width = self.width-2
        view.height = self.height-4
        view.x = self.x
        view.y = self.y
        return view
