from __future__ import annotations
from typing import TYPE_CHECKING
from src.types.room_type_catalog import ROOM_TYPE_CATALOG

if TYPE_CHECKING:
    from src.models.logical.logical_room import LogicalRoom
    from src.models.physical.room_control_panel import RoomControlPanel

class ConnectedPanel:

    def __init__(self, panel: RoomControlPanel, room: LogicalRoom) -> None:
        self.panel = panel
        self.room: LogicalRoom = room

    def turn_lights_off_from_room(self):
        self.panel.turn_lights_off()

    def turn_lights_on_dim_from_room(self):
        for unit in self.panel.connected_lights.values():
            unit.turn_on()

    def __str__(self) -> str:
        room_type = ROOM_TYPE_CATALOG.get_by_id(self.room.room_type_id)
        room_type_name = room_type.display_name if room_type else "Unknown Type"
        return f"ConnectedPanel(Room {self.room.floor_level}-{self.room.room_number} ({room_type_name}))"
