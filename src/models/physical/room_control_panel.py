from __future__ import annotations
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.physical.room import Room
    from src.models.physical.light_unit import LightUnit

class RoomControlPanel:
    def __init__(self, parent: Room) -> None:
        self.hardware_id: str = f"PANEL_{str(uuid.uuid4())}"
        self.belongs_to: Room = parent
        self.connected_lights: dict[str, LightUnit] = {}

    def connect_light_unit(self, label: str, unit: LightUnit) -> None:
        self.connected_lights[label] = unit
