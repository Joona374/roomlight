from src.models.logical.connected_panel import ConnectedPanel
from src.models.physical.room_control_panel import RoomControlPanel
from src.types import RoomType


class RoomLightSystem:
    def __init__(self) -> None:
        self.connected_panels: list[ConnectedPanel] = []

    def add_a_control_panel(self, panel: RoomControlPanel, room_floor: int, room_number: int, room_type: RoomType) -> None:
        new_connection = ConnectedPanel(panel, room_floor, room_number, room_type)
        self.connected_panels.append(new_connection)