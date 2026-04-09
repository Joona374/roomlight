from __future__ import annotations
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.physical.room import Room
    from src.models.physical.light_unit import LightUnit
    from src.models.logical.room_light_system import RoomLightSystem

class RoomControlPanel:
    """
    This model represents the physical control panel in a room that guests interact with.
    It provides the visitor with a simple interface to control the connected light units. (REQ-01)
    The options in the panel are controller by the 'logical controll panel' (src/models/logical/connected_panel.py)
    """

    def __init__(self) -> None:
        self.hardware_id: str = f"PANEL_{str(uuid.uuid4())}"
        self.belongs_to: Room | None = None  # This will be set when the panel is assigned to a room.
        self.connected_lights: dict[str, LightUnit] = {}

    def attach_to_room(self, room: Room):
        self.belongs_to = room

    def connect_light_unit(self, label: str, unit: LightUnit) -> None:
        self.connected_lights[label] = unit

    def connect_to_roomlight_system(self, system: RoomLightSystem) -> None:
        """
        Register this panel to the central room light system.
        This creates the logical connection between the physical
        panel and the system that allows configuring and controlling it remotely.
        """
        room = self.belongs_to
        if room is None:
            # While in the real world this is attempting to model, this would be a physical impossibility,
            # logically it makes no sense to have a panel that doesnt belong to a room connecting to the system, so we guard against it here.
            raise Exception("Panel must be attached to a room before connecting to the system.")
        system.add_a_control_panel(self, room.floor, room.number)

    def turn_lights_off(self):
        """
        While most functions in the panel are confugired by the logical control panel,
        the "turn all lights off" function is such a common and basic feature that we can
        implement it directly in the physical panel model.
        """
        for unit in self.connected_lights.values():
            unit.turn_off()
