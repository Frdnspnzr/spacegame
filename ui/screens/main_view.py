import renderer.primitives as primitives
from constants import (CONSOLE_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH,
                       SIDEBAR_WIDTH, STATUS_HEIGHT)
from esper import World
from tcod import Console
from ui.screen import Screen
from ui.screens.console_view import ConsoleView
from ui.screens.sidebar_view import SidebarView
from ui.screens.space_view import SpaceView


class MainView(Screen):

    def __init__(self, world: World):

        super().__init__(world)

        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        self.add_screen(self.__create_space_view())
        self.add_screen(self.__create_console_view())
        self.add_screen(self.__create_sidebar_view())

    def __create_space_view(self):
        view = SpaceView(self.world)
        view.width = SCREEN_WIDTH-SIDEBAR_WIDTH-1
        view.height = SCREEN_HEIGHT-CONSOLE_HEIGHT-STATUS_HEIGHT
        view.x = view.y = 1
        return view

    def __create_console_view(self):
        view = ConsoleView(self.world)
        view.width = SCREEN_WIDTH-SIDEBAR_WIDTH-1
        view.height = CONSOLE_HEIGHT-2
        view.x = 1
        view.y = SCREEN_HEIGHT-CONSOLE_HEIGHT+1
        return view

    def __create_sidebar_view(self):
        view = SidebarView(self.world)
        view.width = SIDEBAR_WIDTH-2
        view.height = SCREEN_HEIGHT-7
        view.x = SCREEN_WIDTH-SIDEBAR_WIDTH+1
        view.y = 1
        return view

    def _render_self(self, console: Console):
        self.__render_frames(console)

    def __render_frames(self, console: Console) -> None:

        # Outer Frame
        primitives.box(console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Sidebar
        primitives.box(console, SCREEN_WIDTH-SIDEBAR_WIDTH,
                       0, SIDEBAR_WIDTH, SCREEN_HEIGHT)

        # Status
        primitives.box(console, SCREEN_WIDTH-SIDEBAR_WIDTH,
                       SCREEN_HEIGHT-STATUS_HEIGHT, SIDEBAR_WIDTH, STATUS_HEIGHT)

        # console
        primitives.box(console, 0, SCREEN_HEIGHT-CONSOLE_HEIGHT,
                       SCREEN_WIDTH-SIDEBAR_WIDTH+1, CONSOLE_HEIGHT)

        # Corners
        console.print(0, SCREEN_HEIGHT-CONSOLE_HEIGHT, "╠")
        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH,
                      SCREEN_HEIGHT-CONSOLE_HEIGHT, "╣")
        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH, SCREEN_HEIGHT-1, "╩")
        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH, 0, "╦")
        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH,
                      SCREEN_HEIGHT-STATUS_HEIGHT, "╠")
        console.print(SCREEN_WIDTH-1, SCREEN_HEIGHT-STATUS_HEIGHT, "╣")
