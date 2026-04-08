from src.models.physical.floor import Floor


class Property:
    def __init__(self, name: str) -> None:
        self.name = name
        self.floors: list[Floor] = []

    def add_floor(self, floor: Floor) -> None:
        self.floors.append(floor)