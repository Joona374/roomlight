from src.models.logical.logical_room import LogicalRoom


class LogicalFloor:
    def __init__(self, level: int):
        self.level = level
        self.rooms: dict[int, LogicalRoom] = {}

    def add_room(self, room: LogicalRoom):
        self.rooms[room.room_number] = room

    def get_rooms(self) -> list[LogicalRoom]:
        """
        Returns a list of all the rooms on the floor.
        The dict is keyed by room number, so this guarantees the rooms are always returned in the correct order from lowest to highest number.
        """
        return [self.rooms[room_number] for room_number in sorted(self.rooms)]