from src.models.physical.room_control_panel import RoomControlPanel
from src.types import RoomType


class ConnectedPanel:
    def __init__(self, panel: RoomControlPanel, floor_number: int, room_number: int, room_type: RoomType) -> None:
        self.panel = panel
        self.floor_number = floor_number
        self.room_number = room_number
        self.room_type = room_type

    def turn_lights_off_from_room(self):
        self.panel.turn_lights_off()

