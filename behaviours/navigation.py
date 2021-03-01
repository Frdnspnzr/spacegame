import numpy as np
from engine.behaviour import Behaviour
from esper import World
from simulation.components.acceleration import Acceleration
from simulation.components.position import Position
from simulation.components.velocity import Velocity


class BehaviourFollow(Behaviour):

    def __init__(self, target: int, distance: int = 0):
        self.distance = distance
        self.target = target
        self.valid = True

    def priority(self):
        return super().priority()

    def valid(self):
        return self.valid

    def execute(self, world: World, entity: int):

        # TODO As this does not break before reaching the target it enforces heavy overshooting that gradually gets worse

        # Prepare data
        try:
            self_position = world.component_for_entity(entity, Position)
            self_velocity = world.component_for_entity(entity, Velocity)
            self_acceleration = world.component_for_entity(entity, Acceleration)

            target_position = world.component_for_entity(self.target, Position)
            target_velocity = world.component_for_entity(self.target, Velocity)
        except KeyError:
            self.valid = False
            return

        # Prepare data as vectors
        v_self_position = np.array([self_position.x, self_position.y])
        v_self_velocity = np.array([self_velocity.x, self_velocity.y])

        v_target_position = np.array([target_position.x, target_position.y])
        v_target_velocity = np.array([target_velocity.x, target_velocity.y])

        # Calculate navigation target
        v_navigation_target = v_target_position
        if self.distance > 0:
            # Adjust for follow distance and go there
            target_velocity_size = np.linalg.norm(v_target_velocity)
            if target_velocity_size > 0:
                v_follow_velocity = v_target_velocity / target_velocity_size
            else:
                v_follow_velocity = v_target_position - v_self_position
                v_follow_velocity = v_follow_velocity / np.linalg.norm(v_follow_velocity)
            v_follow_velocity *= -1 * self.distance
            v_navigation_target = v_target_position + v_follow_velocity
        else:
            # Navigate right to where the target will be next tick
            v_navigation_target = v_target_position + v_target_velocity

        # What has to actually happen to get to the navigation target?
        v_course_correction = v_navigation_target - (v_self_position + v_self_velocity)

        # FIXME Enforce some maximum acceleration. The maximum acceleration of entities should be a system.
        v_course_correction = v_course_correction / np.linalg.norm(v_course_correction)
        v_course_correction *= 0.001

        self_acceleration.x = v_course_correction[0]
        self_acceleration.y = v_course_correction[1]
