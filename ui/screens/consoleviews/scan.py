import tcod
from esper import World

from behaviours.navigation import BehaviourFollow
from renderer import text
from simulation.components.behaviour import Behaviour
from simulation.components.name import Name
from simulation.components.player import Player
from simulation.components.selectable import Selectable
from ui.screen import Screen


class ScanView(Screen):

    def __init__(self, world: World):
        super().__init__(world)

    def _render_self(self, console: tcod.Console):
        console.print(self.x, self.y, "Scanning some stuff")