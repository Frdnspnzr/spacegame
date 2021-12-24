import esper
from gameplay.actor import Actor
from gameplay.attribute import Attribute
from simulation.components.acceleration import Acceleration
from simulation.components.GameplayActor import GameplayActor
from simulation.components.destructable import Destructable


class ApplyAttributesProcessor(esper.Processor):

    def process(self, *args, **kwargs):
        for entity, (actor) in self.world.get_component(GameplayActor):
            self.__update_acceleration(entity, actor.actor)
            self.__update_destructable(entity, actor.actor)

    def __update_acceleration(self, entity: int, actor: Actor):
        if not self.world.has_component(entity, Acceleration):
            return
        acceleration = self.world.component_for_entity(entity, component_type=Acceleration)
        acceleration.max_acceleration = actor.get_attribute(Attribute.MAX_ACCELERATION)

    def __update_destructable(self, entity: int, actor: Actor):
        if not self.world.has_component(entity, Destructable):
            return
        destructable = self.world.component_for_entity(entity, Destructable)
        destructable.max_core = actor.get_attribute(Attribute.MAX_CORE)
        destructable.max_hull = actor.get_attribute(Attribute.MAX_HULL)
        destructable.max_shield = actor.get_attribute(Attribute.MAX_SHIELD)
