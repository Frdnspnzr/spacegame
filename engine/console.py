from behaviours.navigation import BehaviourFollow
from simulation.components.behaviour import Behaviour
import tcod
from esper import World
from renderer import text
from simulation.components.name import Name
from simulation.components.player import Player
from simulation.components.selectable import Selectable
from tcod.console import Console as tConsole


class Console(tcod.event.EventDispatch[None]):

    def __init__(self, world: World):
        self.world = world
        self.follow_target = None

    def render(self, console: tConsole, x: int, y: int, width: int, height: int) -> None:
        console.print(x, y, f"NAV TARGET: {self._get_nav_target_name()}")

        text.with_highlighting(console, x, y+2, "[F]OLLOW")
        console.print(x+9, y+2, self._get_highlighted_name())
        text.with_highlighting(console, x, y+3, "[S]TOP")

    def ev_keyup(self, event: tcod.event.KeyDown) -> None:

        if event.scancode is tcod.event.SCANCODE_S:
            self.follow_target = None
            self._set_player_stopping()

        if event.scancode is tcod.event.SCANCODE_F:
            self.follow_target = self._get_highlighted_entity()
            self._set_player_following(self.follow_target)

    def _get_nav_target_name(self):
        if self.follow_target is None or not self.world.has_component(self.follow_target, Name):
            return "NONE"
        name = self.world.component_for_entity(self.follow_target, Name)
        return name.formatted_name

    def _get_highlighted_name(self):
        for _, (selectable, name) in self.world.get_components(Selectable, Name):
            if (selectable.selected_main):
                return name.formatted_name

    def _get_highlighted_entity(self):
        for entity, selectable in self.world.get_component(Selectable):
            if selectable.selected_main:
                return entity

    def _set_player_following(self, target: int):
        behaviour = self.world.component_for_entity(self._get_player_entity(self.world), Behaviour)
        behaviour.behaviours.append(BehaviourFollow(target, 3))

    def _set_player_stopping(self):
        behaviour = self.world.component_for_entity(self._get_player_entity(self.world), Behaviour)
        behaviour.behaviours = list() #FIXME Only possible because I know what behaviours are set

    def _get_player_entity(self, world: World):
        for entity, _ in self.world.get_component(Player):
            return entity
