import esper
from gameplay.attribute import Attribute as GameplayAttribute
from simulation.components.acceleration import Acceleration
from simulation.components.attributes import Attributes
from simulation.components.destructable import Destructable


class ApplyAttributesProcessor(esper.Processor):

    def process(self, *args, **kwargs):
        for entity, (attributes) in self.world.get_components(Attributes):
            self.__update_acceleration(entity, attributes)
            self.__update_destructable(entity, attributes)

    def __update_acceleration(self, entity: int, attributes: Attributes):
        acceleration = self.world.try_component(entity, Acceleration)
        if acceleration:
            acceleration.max_acceleration = attributes[GameplayAttribute.MAX_ACCELERATION]

    def __update_destructable(self, entity: int, attributes: Attributes):
        destructable = self.world.try_component(entity, Destructable)
        if destructable:
            destructable.max_core = attributes[GameplayAttribute.MAX_CORE]
            destructable.max_hull = attributes[GameplayAttribute.MAX_HULL]
            destructable.max_shield = attributes[GameplayAttribute.MAX_SHIELD]
