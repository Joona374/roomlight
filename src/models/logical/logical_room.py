from src.models.logical.connected_panel import ConnectedPanel
from src.types import RoomType


class LogicalRoom:
    def __init__(self, room_id: str, room_type: RoomType, floor_level: int, room_number: int):
        self.room_id = room_id
        self.room_type = room_type
        self.floor_level = floor_level
        self.room_number = room_number
        self.control_panel: ConnectedPanel # This will be set when the panel is connected to the room in the RoomLightSystem.