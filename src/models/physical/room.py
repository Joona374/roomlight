from src.types import RoomType, ROOM_CONFIGURATIONS
from src.models.physical.light_unit import LightUnit
from src.models.physical.room_control_panel import RoomControlPanel


class Room:

    def __init__(
        self,
        id: str,
        type: RoomType,
        floor: int,
        room_number: int,
        control_panel: RoomControlPanel,
        light_units: list[LightUnit],
    ) -> None:
        self.id: str = id
        self.floor: int = floor
        self.number: int = room_number
        self.type: RoomType = type
        self.control_panel: RoomControlPanel = control_panel
        self.light_units: list[LightUnit] = light_units
