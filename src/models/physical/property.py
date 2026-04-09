from src.models.physical.floor import Floor


class Property:
    """
    This model represents the physical hotel property.
    It acts mainly as a (root) container for the physical floors and room models.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.floors: list[Floor] = []

    def add_floor(self, floor: Floor) -> None:
        self.floors.append(floor)
