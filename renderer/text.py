from typing import Tuple

from colors import TEXT_DEFAULT, TEXT_HIGHLIGHT
from tcod.console import Console


def with_highlighting(
    console: Console,
    x: int,
    y: int,
    text: str,
    text_color: Tuple[int, int, int] = TEXT_DEFAULT,
    highlight_color: Tuple[int, int, int] = TEXT_HIGHLIGHT
    ) -> None:
    dx = x
    color = text_color
    for char in text:
        if char is "[":
            color = highlight_color
        console.print(dx, y, char, color)
        if char is "]":
            color = text_color
        dx = dx + 1
