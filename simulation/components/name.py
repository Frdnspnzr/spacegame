from typing import Optional
from simulation.components.component import Component


class Name(Component):

    def __init__(self, name: Optional[str] = "", callsign: Optional[str] = ""):
        super().__init__()
        self.name = name
        self.callsign = callsign

    @property
    def formatted_name(self) -> str:
        return f"[{self.callsign}] {self.name}"