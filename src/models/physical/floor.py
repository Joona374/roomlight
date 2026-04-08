from src.models.physical.room import Room


class Floor:
    def __init__(self, level: int) -> None:
        self.level: int = level
        self.rooms: list[Room] = []

    def add_room(self, room: Room) -> None:
        self.rooms.append(room)