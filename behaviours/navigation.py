from typing import Tuple
import numpy as np
from engine.behaviour import Behaviour
from esper import World
from simulation.components.acceleration import Acceleration
from simulation.components.position import Position
from simulation.components.velocity import Velocity


class BehaviourGoto(Behaviour):

    def __init__(self, target_x: int, target_y: int):
        self.__target_x = target_x
        self.__target_y = target_y
        self.__valid = True

    def priority(self):
        return super().priority()

    def valid(self):
        return self.__valid

    def execute(self, world: World, entity: int):

        # TODO As this does not break before reaching the target it enforces heavy overshooting that gradually gets worse

        # Prepare data
        try:
            self_position = world.component_for_entity(entity, Position)
            self_velocity = world.component_for_entity(entity, Velocity)
            self_acceleration = world.component_for_entity(entity, Acceleration)
            self.__valid = True
        except KeyError:
            self.__valid = False
            return

        v_self_position = np.array([self_position.x, self_position.y])
        v_self_velocity = np.array([self_velocity.x, self_velocity.y])

        v_navigation_target = np.array(self._get_target_point(world, entity))

        # What has to actually happen to get to the navigation target?
        v_course_correction = v_navigation_target - (v_self_position + v_self_velocity)

        #Enfore maximum acceleration
        v_course_correction = v_course_correction / np.linalg.norm(v_course_correction)
        v_course_correction *= self_acceleration.max_acceleration

        #Accelerate to correct course
        self_acceleration.x = v_course_correction[0]
        self_acceleration.y = v_course_correction[1]

    def _get_target_point(self) -> Tuple[int, int]:
        return (self.__target_x, self.__target_y)

class BehaviourFollow(BehaviourGoto):

    def __init__(self, target: int, distance: int = 0):
        self.__distance = distance
        self.__target = target
        self.__valid = True

    def priority(self):
        return super().priority()

    def __valid(self):
        return self.__valid

    def _get_target_point(self, world: World, entity: int) -> Tuple[int, int]:

        # Prepare data
        try:
            self_position = world.component_for_entity(entity, Position)
            target_position = world.component_for_entity(self.__target, Position)
            target_velocity = world.component_for_entity(self.__target, Velocity)
            self.__valid = super().valid()
        except KeyError:
            self.__valid = False
            return

        v_self_position = np.array([self_position.x, self_position.y])
        v_target_position = np.array([target_position.x, target_position.y])
        v_target_velocity = np.array([target_velocity.x, target_velocity.y])

        # Calculate navigation target
        v_navigation_target = v_target_position
        if self.__distance > 0:
            # Adjust for follow distance and go there
            target_velocity_size = np.linalg.norm(v_target_velocity)
            if target_velocity_size > 0:
                v_follow_velocity = v_target_velocity / target_velocity_size
            else:
                v_follow_velocity = v_target_position - v_self_position
                v_follow_velocity = v_follow_velocity / np.linalg.norm(v_follow_velocity)
            v_follow_velocity *= -1 * self.__distance
            v_navigation_target = v_target_position + v_follow_velocity
        else:
            # Navigate right to where the target will be next tick
            v_navigation_target = v_target_position + v_target_velocity

        return (v_navigation_target[0], v_navigation_target[1])
