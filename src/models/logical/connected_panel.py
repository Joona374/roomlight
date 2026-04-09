from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.logical.logical_room import LogicalRoom
    from src.models.physical.room_control_panel import RoomControlPanel

class ConnectedPanel:

    def __init__(self, panel: RoomControlPanel, room: LogicalRoom) -> None:
        self.panel = panel
        self.room: LogicalRoom = room

    def turn_lights_off_from_room(self):
        self.panel.turn_lights_off()

    def __str__(self) -> str:
        return f"ConnectedPanel(Room {self.room.floor_level}-{self.room.room_number} ({self.room.room_type.name}))"
