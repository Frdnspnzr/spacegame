from typing import Dict, Optional, Tuple

import numpy as np
from esper import World

from engine.behaviour import Behaviour
from simulation.components.acceleration import Acceleration
from simulation.components.position import Position
from simulation.components.velocity import Velocity


class BehaviourGoto(Behaviour):

    def __init__(self, target_x: Optional[int] = 0, target_y: Optional[int] = 0):
        self.__target_x = target_x
        self.__target_y = target_y
        self.__valid = True

    @property
    def valid(self) -> bool:
        return self.__valid

    def execute(self, world: World, entity: int):

        # Prepare data
        try:
            self_position = world.component_for_entity(entity, Position)
            self_velocity = world.component_for_entity(entity, Velocity)
            self_acceleration = world.component_for_entity(entity, Acceleration)
            self.__valid = True
        except KeyError:
            self.__valid = False
            return

        target_position = self._get_target_point(world, entity)
        if target_position is None:
            self.__valid = False
            return

        v_self_position = np.array([self_position.x, self_position.y])
        v_self_velocity = np.array([self_velocity.x, self_velocity.y])

        v_navigation_target = np.array(target_position)

        # Calculate stopping distance
        self_speed = np.linalg.norm(v_self_velocity)
        stopping_distance = (self_speed**2) / (2 * self_acceleration.max_acceleration)

        # What has to actually happen to get to the navigation target?
        v_course_correction = v_navigation_target - (v_self_position + v_self_velocity)

        #Enfore maximum acceleration
        v_course_correction = v_course_correction / np.linalg.norm(v_course_correction)
        v_course_correction *= self_acceleration.max_acceleration

        if stopping_distance >= np.linalg.norm(v_navigation_target - v_self_position):
            v_course_correction = v_course_correction * -1

        #Accelerate to correct course
        self_acceleration.x = v_course_correction[0]
        self_acceleration.y = v_course_correction[1]

    def _get_target_point(self, world: World, entity: int) -> Optional[Tuple[int, int]]:
        return (self.__target_x, self.__target_y)

class BehaviourFollow(BehaviourGoto):

    def __init__(self, target: Optional[int] = 0, distance: Optional[int] = 0):
        self.__distance = distance
        self.__target = target

    def _get_target_point(self, world: World, entity: int) -> Optional[Tuple[int, int]]:

        if entity is self.__target:
            return None

        # Prepare data
        try:
            self_position = world.component_for_entity(entity, Position)
            target_position = world.component_for_entity(self.__target, Position)
            target_velocity = world.component_for_entity(self.__target, Velocity)
        except KeyError:
            return None

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

    def fromDict(self, dictionary, id_mapping: Dict[int, int] = dict()):
        super().fromDict(dictionary, id_mapping)
        self.__target = id_mapping[self.__target]

class BehaviourPatrol(BehaviourGoto):

    def __init__(self, target_a: Optional[Tuple[int, int]] = (0,0),
            target_b: Optional[Tuple[int, int]] = (1,1), distance: Optional[int] = 0):
        self.target_a = target_a
        self.target_b = target_b
        self.current_target_b = False
        self.distance = distance

    def _get_target_point(self, world: World, entity: int) -> Optional[Tuple[int, int]]:
        self_position = world.component_for_entity(entity, Position)
        patrol_target = self.__get_patrol_target()

        v_self_position = np.array([self_position.x, self_position.y])
        v_patrol_target = np.array([patrol_target[0], patrol_target[1]])

        distance = np.linalg.norm(v_patrol_target - v_self_position)

        if (distance <= self.distance):
            self.current_target_b = not self.current_target_b
            patrol_target = self.__get_patrol_target()
            v_patrol_target = np.array([patrol_target[0], patrol_target[1]])

        return (v_patrol_target[0], v_patrol_target[1])

    def __get_patrol_target(self) -> Tuple[int, int]:
        return self.target_b if self.current_target_b else self.target_a
