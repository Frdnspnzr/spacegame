from __future__ import annotations

import tcod


class EventHandler(tcod.event.EventDispatch[None]):

    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()