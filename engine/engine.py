from __future__ import annotations

import datetime
import json
import os
import time

import esper
import tcod
import tcod.event
from tcod.console import Console as tConsole
from tcod.context import Context
from tcod.random import Random

import simulation.components
import simulation.entity_factory as factory
from behaviours import BehaviourPatrol
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from simulation.components import (Acceleration, Behaviour, Player, Position,
                                   Selectable)
from simulation.processors.acceleration import AccelerationProcessor
from simulation.processors.apply_attributes import ApplyAttributesProcessor
from simulation.processors.apply_damage import ApplyDamageProcessor
from simulation.processors.enforce_max_acceleration import \
    EnforceMaxAccelerationProcessor
from simulation.processors.enforce_max_hp import EnforceMaxHPProcessor
from simulation.processors.execute_behaviours import ExecuteBehaviourProcessor
from simulation.processors.movement import MovementProcessor
from ui.screens.main_view import MainView

UPDATE_RATE = 1/60


class Engine(tcod.event.EventDispatch[None]):

    def __init__(self):
        self.world = esper.World()

        # New renderer
        self.main_screen = MainView(self.world)
        self.main_screen.width = SCREEN_WIDTH
        self.main_screen.heigt = SCREEN_HEIGHT
        self.main_screen.x = 0
        self.main_screen.y = 0

        self.last_update = time.monotonic()
        self.accumulator = 0

        # Add processors
        self.__initialize_processors()

    def initialize_test_data(self):
        self.world.clear_database()

        rand_x = Random()
        rand_y = Random()

        # Add player ship
        self.player_ship = factory.player_ship(self.world)
        self.world.component_for_entity(
            self.player_ship, Selectable).selected_main = True
        # Add some asteroids
        for i in range(20):
            asteroid = factory.asteroid(self.world)
            position = Position(int(50 * rand_x.guass(0, 0.3)),
                                int(50 * rand_y.guass(0, 0.3)))
            self.world.add_component(asteroid, position)

        # Add patroling enemy
        enemy = factory.enemy_fighter(self.world)
        enemy_behaviour: Behaviour = self.world.component_for_entity(
            enemy, Behaviour)
        enemy_behaviour.behaviours.append(
            BehaviourPatrol((10, 10), (10, -10), 2))

    def initialize_from_file(self, filename: str):
        self.world.clear_database()
        self.__deserialize_world(filename)

    def __deserialize_world(self, filename: str):
        with open(filename, "r") as f:
            id_mapping = dict()
            deserialized = json.load(f)
            for entity, _ in deserialized["entities"].items():
                new_entity = self.world.create_entity()
                id_mapping[int(entity)] = new_entity
            for entity, components in deserialized["entities"].items():
                for name, data in components.items():
                    component = getattr(simulation.components, name)()
                    component.fromDict(data, id_mapping)
                    self.world.add_component(id_mapping[int(entity)], component)

        for (e, _) in self.world.get_component(Player):
            self.player_ship = e

    def __serialize_world(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
        with open(filepath, "w") as f:
            serialized = dict({"version": 1, "time": str(datetime.datetime.now()), "entities": dict()})
            for e in list(self.world._entities):
                serialized["entities"][e] = self.__get_components_as_json(e)
            json.dump(serialized, f)

    def __get_components_as_json(self, entity: int):
        components = self.world.components_for_entity(entity)
        serialized = dict()
        for c in components:
            serialized[type(c).__name__] = c.toDict()
        return serialized

    def update(self) -> None:
        self.__update_accumulator()
        if self.accumulator > UPDATE_RATE:
            self.accumulator = self.accumulator - UPDATE_RATE
            self.world.process(UPDATE_RATE)

    def render(self, console: tConsole, context: Context) -> None:
        self.main_screen.render(console)

        context.present(console)
        console.clear()

    def handle_events(self) -> None:
        for event in tcod.event.get():
            self.dispatch(event)
            if event.type == "KEYDOWN" or event.type == "KEYUP":
                self.main_screen.dispatch_event(event)

    def ev_keyup(self, event: tcod.event.KeyUp) -> None:
        acceleration = self.world.component_for_entity(
            self.player_ship, Acceleration)

        if event.scancode == tcod.event.SCANCODE_W and event.mod & tcod.event.KMOD_LCTRL:
            acceleration.y -= 0.01
        if event.scancode == tcod.event.SCANCODE_S and event.mod & tcod.event.KMOD_LCTRL:
            acceleration.y += 0.01
        if event.scancode == tcod.event.SCANCODE_A and event.mod & tcod.event.KMOD_LCTRL:
            acceleration.x -= 0.01
        if event.scancode == tcod.event.SCANCODE_D and event.mod & tcod.event.KMOD_LCTRL:
            acceleration.x += 0.01

    def ev_quit(self, _: tcod.event.Quit) -> None:
        self.__serialize_world("autosave.sgs")
        raise SystemExit()

    def __update_accumulator(self) -> None:
        now = time.monotonic()
        difference = now - self.last_update
        self.accumulator = self.accumulator + difference
        self.last_update = time.monotonic()

    def __initialize_processors(self):

        priority = 1000

        # Low level gameplay housekeeping
        priority -= 1
        self.world.add_processor(ApplyAttributesProcessor(), priority)

        # Attribute enforcement
        priority -= 1
        self.world.add_processor(EnforceMaxAccelerationProcessor(), priority)
        self.world.add_processor(EnforceMaxHPProcessor(), priority)

        # Simulation effects, high priority
        priority -= 1
        self.world.add_processor(AccelerationProcessor(), priority)

        # Simulation effects, low priority
        priority -= 1
        self.world.add_processor(MovementProcessor(), priority)
        self.world.add_processor(ApplyDamageProcessor(), priority)

        # AI and player actions
        priority -= 1
        self.world.add_processor(ExecuteBehaviourProcessor(), priority)

    # def __mockup_render(self, console: tConsole) -> None:
    #     values = self.world.component_for_entity(
    #         self.player_ship, Destructable)

    #     console.print(SCREEN_WIDTH-SIDEBAR_WIDTH+1, SCREEN_HEIGHT -
    #                   STATUS_HEIGHT, "CORE", fg=(235, 164, 52))
    #     primitives.bar(console, SCREEN_WIDTH-SIDEBAR_WIDTH+6, SCREEN_HEIGHT -
    #                    STATUS_HEIGHT, 28, values.core_percentage, (235, 164, 52))

    #     console.print(SCREEN_WIDTH-SIDEBAR_WIDTH+1, SCREEN_HEIGHT -
    #                   STATUS_HEIGHT+1, "HULL", fg=(168, 168, 168))
    #     primitives.bar(console, SCREEN_WIDTH-SIDEBAR_WIDTH+6, SCREEN_HEIGHT -
    #                    STATUS_HEIGHT+1, 28, values.hull_percentage, (168, 168, 168))

    #     console.print(SCREEN_WIDTH-SIDEBAR_WIDTH+1, SCREEN_HEIGHT -
    #                   STATUS_HEIGHT+2, "SHLD", fg=(109, 182, 214))
    #     primitives.bar(console, SCREEN_WIDTH-SIDEBAR_WIDTH+6, SCREEN_HEIGHT -
    #                    STATUS_HEIGHT+2, 28, values.shield_percentage, (109, 182, 214))

    #     console.print(0, SCREEN_HEIGHT-1,
    #                   "[F1] MAIN", fg=colors.TEXT_HIGHLIGHT)
    #     console.print(10, SCREEN_HEIGHT-1, "[F2] COMM")
    #     console.print(20, SCREEN_HEIGHT-1, "[F3] MODS")
