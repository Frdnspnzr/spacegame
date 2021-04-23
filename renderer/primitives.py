from typing import Tuple

from tcod.console import Console


def box(console: Console, x: int, y: int, width: int, height: int) -> None:
    for dx in range(0, width):
        console.print(x+dx, y, "═")
        console.print(x+dx, y+height-1, "═")
    for dy in range(0, height):
        console.print(x, y+dy, "║")
        console.print(x+width-1, y+dy, "║")
    console.print(x, y, "╔")
    console.print(x+width-1, y, "╗")
    console.print(x, y+height-1, "╚")
    console.print(x+width-1, y+height-1, "╝")

def bar(console: Console, x: int, y: int, width: int, fill: float, color: Tuple[int, int, int]) -> None:
    for cx in range(x, x + width):
        percentage = (cx - x) / width
        if percentage <= fill:
            console.print(cx, y, "█", fg=color)
        else:
            console.print(cx, y, "▒", fg=color)
