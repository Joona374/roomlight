from datetime import datetime, timedelta

from src.models.logical.connected_panel import ConnectedPanel
from src.models.logical.logical_floor import LogicalFloor
from src.models.logical.logical_room import LogicalRoom
from src.models.physical.room_control_panel import RoomControlPanel


class RoomLightSystem:
    def __init__(self) -> None:
        self.connected_panels: list[ConnectedPanel] = []
        self.floors: dict[int, LogicalFloor] = {}
        # Simulation clock ticks 1 minute every real second from app loop.
        self.simulated_time: datetime = datetime(2026, 1, 1, 12, 0)
        self.checkout_schedules: dict[tuple[int, int], datetime] = {}
        self.checkin_schedules: dict[tuple[int, int], datetime] = {}

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

    def get_room_by_floor_and_number(self, floor: int, number: int) -> LogicalRoom | None:
        return self._get_room_by_floor_and_number(floor, number)

    def get_rooms_for_floor(self, floor: int) -> list[LogicalRoom]:
        if floor not in self.floors:
            return []
        return self.floors[floor].get_rooms()

    def get_simulated_time(self) -> datetime:
        return self.simulated_time

    def set_checkout_time(self, room_floor: int, room_number: int, hour: int, minute: int) -> datetime:
        corresponding_room = self._get_room_by_floor_and_number(room_floor, room_number)
        if not corresponding_room:
            raise ValueError(f"Cannot set checkout for non existing room {room_floor}-{room_number}.")

        scheduled = self.simulated_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if scheduled <= self.simulated_time:
            scheduled += timedelta(days=1)

        self.checkout_schedules[(room_floor, room_number)] = scheduled
        return scheduled

    def set_checkin_time(self, room_floor: int, room_number: int, hour: int, minute: int) -> datetime:
        corresponding_room = self._get_room_by_floor_and_number(room_floor, room_number)
        if not corresponding_room:
            raise ValueError(f"Cannot set check-in for non existing room {room_floor}-{room_number}.")

        scheduled = self.simulated_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if scheduled <= self.simulated_time:
            scheduled += timedelta(days=1)

        self.checkin_schedules[(room_floor, room_number)] = scheduled
        return scheduled

    def clear_checkout_time(self, room_floor: int, room_number: int) -> None:
        self.checkout_schedules.pop((room_floor, room_number), None)

    def clear_checkin_time(self, room_floor: int, room_number: int) -> None:
        self.checkin_schedules.pop((room_floor, room_number), None)

    def get_checkout_time(self, room_floor: int, room_number: int) -> datetime | None:
        return self.checkout_schedules.get((room_floor, room_number))

    def get_checkin_time(self, room_floor: int, room_number: int) -> datetime | None:
        return self.checkin_schedules.get((room_floor, room_number))

    def tick_one_minute(self) -> list[tuple[int, int]]:
        self.simulated_time += timedelta(minutes=1)

        due_keys = [room_key for room_key, scheduled_time in self.checkout_schedules.items() if scheduled_time <= self.simulated_time]

        turned_off: list[tuple[int, int]] = []
        for room_floor, room_number in due_keys:
            room = self._get_room_by_floor_and_number(room_floor, room_number)
            if room is not None and hasattr(room, "control_panel"):
                room.control_panel.turn_lights_off_from_room()
                turned_off.append((room_floor, room_number))

            self.checkout_schedules.pop((room_floor, room_number), None)

        due_checkins = [room_key for room_key, scheduled_time in self.checkin_schedules.items() if scheduled_time <= self.simulated_time]

        for room_floor, room_number in due_checkins:
            room = self._get_room_by_floor_and_number(room_floor, room_number)
            if room is not None and hasattr(room, "control_panel"):
                room.control_panel.turn_lights_on_dim_from_room()

            self.checkin_schedules.pop((room_floor, room_number), None)

        return turned_off

    def fast_forward_minutes(self, minutes: int) -> None:
        if minutes <= 0:
            return

        for _ in range(minutes):
            self.tick_one_minute()

    def fast_forward_hours(self, hours: int) -> None:
        self.fast_forward_minutes(hours * 60)

    def fast_forward_days(self, days: int) -> None:
        self.fast_forward_minutes(days * 24 * 60)

    def _get_room_by_floor_and_number(self, floor: int, number: int) -> LogicalRoom | None:
        try:
            return self.floors[floor].rooms[number]
        except KeyError:
            return None
