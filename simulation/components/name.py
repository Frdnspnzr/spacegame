class Name():

    def __init__(self, name: str, callsign: str):
        super().__init__()
        self.name = name
        self.callsign = callsign

    @property
    def formatted_name(self):
        return f"[{self.callsign}] {self.name}"