from math import sqrt

import esper
from simulation.components.acceleration import Acceleration


class EnforceMaxAccelerationProcessor(esper.Processor):

    def process(self, *args, **kwargs):
        for _, (acceleration,) in self.world.get_components(Acceleration):
            length = sqrt(acceleration.x ** 2 + acceleration.y ** 2)
            if length > acceleration.max_acceleration:
                fraction = acceleration.max_acceleration / length
                acceleration.x *= fraction
                acceleration.y *= fraction
