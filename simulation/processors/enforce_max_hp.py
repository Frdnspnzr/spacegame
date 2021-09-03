

import esper
from simulation.components.destructable import Destructable


class EnforceMaxHPProcessor(esper.Processor):

    def process(self, *args, **kwargs):
        for _, (destructable,) in self.world.get_components(Destructable):
            destructable.core_current = min(destructable.core_max, destructable.core_current)
            destructable.hull_current = min(destructable.hull_max, destructable.hull_current)
            destructable.shield_current = min(destructable.shield_max, destructable.shield_current)
