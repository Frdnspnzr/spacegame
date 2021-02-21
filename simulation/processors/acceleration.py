import esper

from simulation.components.velocity import Velocity
from simulation.components.acceleration import Acceleration


class AccelerationProcessor(esper.Processor):

    def process(self, *args, **kwargs):
        for _, (vel, acc) in self.world.get_components(Velocity, Acceleration):
            vel.x = vel.x + acc.x
            vel.y = vel.y + acc.y
