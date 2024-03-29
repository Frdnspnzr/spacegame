from typing import Optional, cast

from simulation.components.component import Component


class Position(Component):

    def __init__(self, x: Optional[int] = 0, y: Optional[int] = 0):
        super().__init__()
        self.__x = cast(float, x)
        self.__y = cast(float, y)

    def move(self, x: float, y: float) -> None:
        self.__x += x
        self.__y += y

    def __get_x(self) -> int:
        return round(self.__x)

    def __set_x(self, val: int):
        self.__x = val

    x = property(__get_x, __set_x)

    def __get_y(self) -> int:
        return round(self.__y)

    def __set_y(self, val: int):
        self.__y = val

    y = property(__get_y, __set_y)
