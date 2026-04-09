from src.models.physical.room import Room


class Floor:
    """
    This model represents a single physical floor in the hotel.
    It acts as a container for the physical rooms that are located on this floor.
    """
    def __init__(self, level: int) -> None:
        self.level: int = level
        self.rooms: list[Room] = []

    def add_room(self, room: Room) -> None:
        self.rooms.append(room)
