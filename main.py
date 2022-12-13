import tcod
import argparse

from engine.engine import Engine
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def main() -> None:

    tileset = tcod.tileset.load_tilesheet(
        "default_font.png", 32, 8, tcod.tileset.CHARMAP_CP437
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--Savegame", help="Filepath to savegame")
    args = parser.parse_args()

    engine = Engine()

    if (args.Savegame):
        engine.initialize_from_file(args.Savegame)
    else:
        engine.initialize_test_data()

    with tcod.context.new_terminal(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        tileset=tileset,
        title="Spacegame",
        vsync=True
    ) as context:
        root_console = tcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        while True:
            engine.handle_events()
            engine.update()
            engine.render(root_console, context)

if __name__ == "__main__":
    main()
