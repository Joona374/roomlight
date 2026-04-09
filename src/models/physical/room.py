from src.types.types import RoomTypeId
from src.models.physical.light_unit import LightUnit
from src.models.physical.room_control_panel import RoomControlPanel


class Room:

    def __init__(
        self,
        id: str,
        type_id: RoomTypeId,
        floor: int,
        room_number: int,
        control_panel: RoomControlPanel,
        light_units: list[LightUnit],
    ) -> None:
        self.id: str = id
        self.floor: int = floor
        self.number: int = room_number
        self.type_id: RoomTypeId = type_id
        self.control_panel: RoomControlPanel = control_panel
        self.light_units: list[LightUnit] = light_units
