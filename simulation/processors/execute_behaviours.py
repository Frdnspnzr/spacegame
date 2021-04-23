import esper
from simulation.components.behaviour import Behaviour


class ExecuteBehaviourProcessor(esper.Processor):

    def process(self, *args, **kwargs):
        for entity, (behaviour,) in self.world.get_components(Behaviour):
            for b in sorted(behaviour.behaviours, key=lambda b: b.priority):
                b.execute(self.world, entity)
