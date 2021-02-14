import esper

from simulation.components.position import Position
from simulation.components.velocity import Velocity


class MovementProcessor(esper.Processor):

    def process(self, *args, **kwargs):
        for _, (vel, pos) in self.world.get_components(Velocity, Position):
            pos.move(vel.x, vel.y)
