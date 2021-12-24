from enum import Enum


class Stacking(Enum):

    ADDITIVE = 1
    MULTIPLICATIVE = 2


class Attribute(Enum):

    # MOVEMENT
    MAX_ACCELERATION = 10

    # HIT POINTS
    MAX_CORE = 20
    MAX_HULL = 21
    MAX_SHIELD = 22

    def get_stacking(self) -> Stacking:
        return Stacking.ADDITIVE
