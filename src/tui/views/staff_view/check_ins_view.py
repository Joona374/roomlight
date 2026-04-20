from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Input, Label, OptionList
from textual.widgets.option_list import Option

from src.models.logical.room_light_system import RoomLightSystem
from src.types.room_type_catalog import ROOM_TYPE_CATALOG


class CheckInsView(Container):
    def __init__(self, roomlight: RoomLightSystem, **kwargs):
        super().__init__(**kwargs)
        self.roomlight = roomlight
        self.selected_floor: int | None = None
        self.selected_room_number: int | None = None

    def compose(self):
        with Horizontal(id="staff-checkin-content"):
            with Vertical(id="staff-checkin-filters"):
                yield Label("Check-ins", classes="section-header")
                yield Label("Simulation clock", classes="field-label")
                yield Label("--:--", id="staff-sim-clock-checkin")
                with Horizontal(id="staff-checkin-time-skip"):
                    yield Button("+1h", id="btn_checkin_plus_1h")
                    yield Button("+1d", id="btn_checkin_plus_1d")

                yield Label("Floor", classes="field-label")
                yield OptionList(id="staff-checkin-floor-list")

                yield Label("Room", classes="field-label")
                yield OptionList(id="staff-checkin-room-list")

            with Vertical(id="staff-checkin-actions"):
                yield Label("Check-in Scheduler", classes="section-header")
                yield Label("Set check-in time (HH:MM)", classes="field-label")
                yield Input(value="12:00", id="staff-checkin-time")

                with Horizontal(id="staff-checkin-buttons"):
                    yield Button("Set Check-in", id="btn_set_checkin", variant="primary")
                    yield Button("Clear Check-in", id="btn_clear_checkin")

                yield Label("", id="staff-selected-room-checkin")
                yield Label("Current check-in: none", id="staff-current-checkin")

    def on_mount(self) -> None:
        self._refresh_floor_list()
        self._refresh_room_list()
        self._refresh_clock_display()
        self.set_interval(1.0, self._refresh_clock_display)

    def _refresh_clock_display(self) -> None:
        self.query_one("#staff-sim-clock-checkin", Label).update(
            self.roomlight.get_simulated_time().strftime("%Y-%m-%d %H:%M")
        )

    def _refresh_floor_list(self) -> None:
        floor_list = self.query_one("#staff-checkin-floor-list", OptionList)
        floor_list.clear_options()

        floors = self.roomlight.get_floors()
        if not floors:
            return

        for floor in floors:
            floor_list.add_option(Option(f"Floor {floor.level}", id=str(floor.level)))

        if self.selected_floor is None:
            self.selected_floor = floors[0].level

    def _refresh_room_list(self) -> None:
        room_list = self.query_one("#staff-checkin-room-list", OptionList)
        room_list.clear_options()

        if self.selected_floor is None:
            return

        rooms = self.roomlight.get_rooms_for_floor(self.selected_floor)
        for room in rooms:
            room_type = ROOM_TYPE_CATALOG.get_by_id(room.room_type_id)
            room_type_name = room_type.display_name if room_type else str(room.room_type_id)
            room_list.add_option(Option(f"Room {room.floor_level}-{room.room_number} ({room_type_name})", id=str(room.room_number)))

        if self.selected_room_number is None and rooms:
            self.selected_room_number = rooms[0].room_number

        self._refresh_selected_room_labels()

    def _refresh_selected_room_labels(self) -> None:
        selected_room_label = self.query_one("#staff-selected-room-checkin", Label)
        checkin_label = self.query_one("#staff-current-checkin", Label)

        if self.selected_floor is None or self.selected_room_number is None:
            selected_room_label.update("No room selected")
            checkin_label.update("Current check-in: none")
            return

        selected_room_label.update(f"Selected room: {self.selected_floor}-{self.selected_room_number}")
        checkin = self.roomlight.get_checkin_time(self.selected_floor, self.selected_room_number)
        if checkin is None:
            checkin_label.update("Current check-in: none")
        else:
            checkin_label.update(f"Current check-in: {checkin.strftime('%Y-%m-%d %H:%M')}")

    def _parse_hhmm(self, raw: str) -> tuple[int, int]:
        text = raw.strip()
        if ":" not in text:
            raise ValueError("Use HH:MM format.")

        hh_str, mm_str = text.split(":", maxsplit=1)
        hour = int(hh_str)
        minute = int(mm_str)

        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError("Time must be between 00:00 and 23:59.")

        return hour, minute

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option_id = event.option.id
        if not option_id:
            return

        if event.option_list.id == "staff-checkin-floor-list":
            self.selected_floor = int(option_id)
            self.selected_room_number = None
            self._refresh_room_list()
            return

        if event.option_list.id == "staff-checkin-room-list":
            self.selected_room_number = int(option_id)
            self._refresh_selected_room_labels()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_checkin_plus_1h":
            self.roomlight.fast_forward_hours(1)
            self._refresh_clock_display()
            self._refresh_selected_room_labels()
            return

        if event.button.id == "btn_checkin_plus_1d":
            self.roomlight.fast_forward_days(1)
            self._refresh_clock_display()
            self._refresh_selected_room_labels()
            return

        if self.selected_floor is None or self.selected_room_number is None:
            self.notify("Select a floor and room first.", severity="warning")
            return

        if event.button.id == "btn_set_checkin":
            raw_time = self.query_one("#staff-checkin-time", Input).value
            try:
                hour, minute = self._parse_hhmm(raw_time)
                scheduled = self.roomlight.set_checkin_time(
                    self.selected_floor,
                    self.selected_room_number,
                    hour,
                    minute,
                )
                self.notify(f"Check-in set for {scheduled.strftime('%Y-%m-%d %H:%M')}")
            except ValueError as exc:
                self.notify(str(exc), severity="error")
            self._refresh_selected_room_labels()
            return

        if event.button.id == "btn_clear_checkin":
            self.roomlight.clear_checkin_time(self.selected_floor, self.selected_room_number)
            self.notify("Check-in cleared.")
            self._refresh_selected_room_labels()
