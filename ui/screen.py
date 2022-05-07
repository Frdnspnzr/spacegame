from __future__ import annotations

from enum import Enum
from typing import List, Optional

import tcod
from esper import World
from tcod.console import Console


class BoundsError(RuntimeError):
    pass


class Screen(object):

    def __init__(self, world: World):
        self.world = world

        self.__sub_screens: List[Screen] = []

        self.__x = 0
        self.__y = 0
        self.__width = 0
        self.__height = 0

        self.__parent: Optional[Screen] = None

    def add_screen(self, screen: Screen):
        self.__sub_screens.append(screen)

    def remove_screen(self, screen: Screen):
        self.__sub_screens.remove(screen)

    def render(self, console: Console):
        self._render_self(console)
        for screen in self.__sub_screens:
            screen.render(console)

    def dispatch_event(self, event: tcod.event.KeyboardEvent):
        for screen in self.__sub_screens:
            screen.dispatch_event(event)
        self._handle_event(event)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def parent(self) -> Screen:
        return self.__parent

    @parent.setter
    def parent(self, parent: Screen):
        self._parent = parent
        self.__check_bounds()

    @x.setter
    def x(self, x: int) -> None:
        self.__x = x
        self.__check_bounds()

    @y.setter
    def y(self, y: int) -> None:
        self.__y = y
        self.__check_bounds()

    @width.setter
    def width(self, width: int) -> None:
        self.__width = width
        self.__check_bounds()

    @height.setter
    def height(self, height: int) -> None:
        self.__height = height
        self.__check_bounds()

    def _render_self(self, console: Console):
        pass

    def _handle_event(self, event: tcod.event.KeyboardEvent):
        pass

    def __check_bounds(self) -> None:
        if self.x < 0:
            raise BoundsError("Start x must be greater than 0")
        if self.y < 0:
            raise BoundsError("Start y must be greater than 0")
        if self.width < 0:
            raise BoundsError("Width must be greater than 0")
        if self.height < 0:
            raise BoundsError("Height must be greater than 0")

        if self.parent is not None:
            if self.x < self.parent.x:
                raise BoundsError(
                    "Start x must be greater than parent's start x")
            if self.y < self.parent.x:
                raise BoundsError(
                    "Start y must be greater than parent's start y")

            if self.x + self.width > self.parent.width:
                raise BoundsError(
                    "Start x + width must be less than parent width")
            if self.y + self.height > self.parent.height:
                raise BoundsError(
                    "Start y + height must be less than parent height")
