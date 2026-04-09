from src.models.logical.connected_panel import ConnectedPanel
from src.models.logical.logical_floor import LogicalFloor
from src.models.physical.room_control_panel import RoomControlPanel


class RoomLightSystem:
    def __init__(self) -> None:
        self.connected_panels: list[ConnectedPanel] = []
        self.floors: dict[int, LogicalFloor] = {}

    def register_floor(self, floor: LogicalFloor) -> None:
        self.floors[floor.level] = floor

    def get_floors(self) -> list[LogicalFloor]:
        """
        Returns a list of all the floors in the system.
        The dict is keyed by floor level, so this guarantees the floors are always returned in the correct order from lowest to highest.
        """
        return [self.floors[level] for level in sorted(self.floors)]

    def add_a_control_panel(self, panel: RoomControlPanel, room_floor: int, room_number: int) -> None:
        corresponding_room = self._get_room_by_floor_and_number(room_floor, room_number)
        if not corresponding_room:
            raise ValueError(f"Cannot connect panel to non existing room {room_floor}-{room_number}.")

        new_connection = ConnectedPanel(panel, corresponding_room)
        self.connected_panels.append(new_connection)

        corresponding_room.control_panel = new_connection

    def _get_room_by_floor_and_number(self, floor: int, number: int):
        try:
            return self.floors[floor].rooms[number]
        except KeyError:
            return None
