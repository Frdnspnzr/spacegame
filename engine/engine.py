from __future__ import annotations

import time

import renderer.primitives as primitives
import tcod.event
from tcod.random import Random
from constants import CONSOLE_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, SIDEBAR_WIDTH, STATUS_HEIGHT
from engine.event_handler import EventHandler
from engine.screen import Screen
from engine.sidebar import Sidebar
import simulation.entity_factory as factory
from simulation.entity_manager import EntityManager
from simulation.components.position import Position
from tcod.console import Console
from tcod.context import Context


class Engine:

    UPDATE_RATE = 1/60

    def __init__(self):
        self.entity_manager = EntityManager()
        self.event_handler = EventHandler()
        self.screen = Screen(self.entity_manager)
        self.sidebar = Sidebar(self.entity_manager)

        self.last_update = time.monotonic()
        self.accumulator = 0

        rand_x = Random()
        rand_y = Random()

        # Add player ship
        ship = factory.player_ship()
        self.entity_manager.add(ship)
        self.entity_manager.player = ship

        # Add some asteroids
        for _ in range(150):
            asteroid = factory.asteroid()
            position = Position(int(50 * rand_x.guass(0, 0.3)), int(50 * rand_y.guass(0, 0.3)))
            asteroid.add_component(position)
            self.entity_manager.add(asteroid)

    def update(self) -> None:
        self.__update_accumulator()
        if self.accumulator > Engine.UPDATE_RATE:
            self.accumulator = self.accumulator - Engine.UPDATE_RATE
            self.entity_manager.update(Engine.UPDATE_RATE)

    def render(self, console: Console, context: Context) -> None:

        self.__mockup_render(console)
        self.screen.render_main(console, 1, 1, SCREEN_WIDTH-SIDEBAR_WIDTH-1, SCREEN_HEIGHT-CONSOLE_HEIGHT-2)
        self.sidebar.render(console, SCREEN_WIDTH-SIDEBAR_WIDTH+1, 1, SIDEBAR_WIDTH-2, SCREEN_HEIGHT-8)
        self.render_frames(console)

        context.present(console)
        console.clear()

    def handle_events(self) -> None:
        for event in tcod.event.get():
            self.event_handler.dispatch(event)

    def render_frames(self, console: Console) -> None:

        # Outer Frame
        primitives.box(console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT-1)

        # Sidebar
        primitives.box(console, SCREEN_WIDTH-SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT-1)

        # Status
        primitives.box(console, SCREEN_WIDTH-SIDEBAR_WIDTH, SCREEN_HEIGHT-1-STATUS_HEIGHT, SIDEBAR_WIDTH, STATUS_HEIGHT)

        # Console
        primitives.box(console, 0, SCREEN_HEIGHT-CONSOLE_HEIGHT-1, SCREEN_WIDTH-SIDEBAR_WIDTH+1, CONSOLE_HEIGHT)

        # Corners
        console.print(0, SCREEN_HEIGHT-CONSOLE_HEIGHT-1, "╠")
        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH, SCREEN_HEIGHT-CONSOLE_HEIGHT-1, "╣")
        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH, SCREEN_HEIGHT-2, "╩")
        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH, 0, "╦")
        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH, SCREEN_HEIGHT-STATUS_HEIGHT-1, "╠")
        console.print(SCREEN_WIDTH-1, SCREEN_HEIGHT-STATUS_HEIGHT-1, "╣")

    def __update_accumulator(self) -> None:
        now = time.monotonic()
        difference = now - self.last_update
        self.accumulator = self.accumulator + difference
        self.last_update = time.monotonic()

    def __mockup_render(self, console: Console) -> None:

        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH+1, SCREEN_HEIGHT-STATUS_HEIGHT, "CORE", fg=(235, 164, 52))
        for x in range(SCREEN_WIDTH-SIDEBAR_WIDTH+6, SCREEN_WIDTH-1):
            console.print(x, SCREEN_HEIGHT-STATUS_HEIGHT, "█", fg=(235, 164, 52))

        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH+1, SCREEN_HEIGHT-STATUS_HEIGHT+1, "HULL", fg=(168, 168, 168))
        for x in range(SCREEN_WIDTH-SIDEBAR_WIDTH+6, SCREEN_WIDTH-SIDEBAR_WIDTH+12):
            console.print(x, SCREEN_HEIGHT-STATUS_HEIGHT+1, "█", fg=(168, 168, 168))
        for x in range(SCREEN_WIDTH-SIDEBAR_WIDTH+12, SCREEN_WIDTH-1):
            console.print(x, SCREEN_HEIGHT-STATUS_HEIGHT+1, "▒", fg=(168, 168, 168))

        console.print(SCREEN_WIDTH-SIDEBAR_WIDTH+1, SCREEN_HEIGHT-STATUS_HEIGHT+2, "SHLD", fg=(109, 182, 214))
        for x in range(SCREEN_WIDTH-SIDEBAR_WIDTH+6, SCREEN_WIDTH-SIDEBAR_WIDTH+24):
            console.print(x, SCREEN_HEIGHT-STATUS_HEIGHT+2, "█", fg=(109, 182, 214))
        for x in range(SCREEN_WIDTH-SIDEBAR_WIDTH+24, SCREEN_WIDTH-1):
            console.print(x, SCREEN_HEIGHT-STATUS_HEIGHT+2, "▒", fg=(109, 182, 214))

        console.print(0, SCREEN_HEIGHT-1, "[F1] MAIN", fg=(255, 255, 33))
        console.print(10, SCREEN_HEIGHT-1, "[F2] COMM")
        console.print(20, SCREEN_HEIGHT-1, "[F3] MODS")
