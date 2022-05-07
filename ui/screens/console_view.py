import tcod
from behaviours.navigation import BehaviourFollow
from esper import World
from renderer import text
from simulation.components.behaviour import Behaviour
from simulation.components.name import Name
from simulation.components.player import Player
from simulation.components.selectable import Selectable
from tcod import Console
from ui.screen import Screen


class ConsoleView(Screen):

    def __init__(self, world: World):
        super().__init__(world)
        self.follow_target = None

    def _render_self(self, console: Console):
        console.print(self.x, self.y,
                      f"NAV TARGET: {self._get_nav_target_name()}")

        text.with_highlighting(console, self.x, self.y+2, "[F]OLLOW")
        console.print(self.x+9, self.y+2, self._get_highlighted_name())
        text.with_highlighting(console, self.x, self.y+3, "[S]TOP")

    def _handle_event(self, event: tcod.event.KeyboardEvent):

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

    def _get_highlighted_name(self) -> str:
        for _, (selectable, name) in self.world.get_components(Selectable, Name):
            if selectable.selected_main:
                return name.formatted_name
        return ""

    def _get_highlighted_entity(self) -> int:
        for entity, selectable in self.world.get_component(Selectable):
            if selectable.selected_main:
                return entity
        return -1

    def _set_player_following(self, target: int):
        behaviour = self.world.component_for_entity(
            self._get_player_entity(self.world), Behaviour)
        behaviour.behaviours.append(BehaviourFollow(target, 3))

    def _set_player_stopping(self):
        behaviour = self.world.component_for_entity(
            self._get_player_entity(self.world), Behaviour)
        # FIXME Only possible because I know what behaviours are set
        behaviour.behaviours = list()

    def _get_player_entity(self, world: World) -> int:
        for entity, _ in self.world.get_component(Player):
            return entity
        return -1
