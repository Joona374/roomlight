from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label, OptionList
from textual.widgets.option_list import Option

from src.models.physical.property import Property
from src.types.lightning_profile_catalog import LIGHTING_PROFILE_CATALOG
from src.types.room_type_catalog import ROOM_TYPE_CATALOG
from src.types.types import ProfileId, RoomTypeId


class RoomProfileAssignmentView(Vertical):
    """Assign lighting profiles to rooms filtered by floor and room type."""

    def __init__(self, property_data: Property, **kwargs):
        super().__init__(**kwargs)
        self.property_data = property_data
        self.selected_floor: int | None = None
        self.selected_room_type_id: RoomTypeId | None = None
        self.selected_profile_id: ProfileId | None = None
        self.selected_room_keys: set[str] = set()

    def compose(self) -> ComposeResult:
        yield Label("Room Profile Assignment", id="title")

        with Horizontal(id="room-profile-assignment-content"):
            with Vertical(id="room-profile-filters-col"):
                yield Label("Filter by Floor", classes="section-header")
                yield OptionList(id="assignment_floor_list")

                yield Label("Filter by Room Type", classes="section-header")
                yield OptionList(id="assignment_room_type_list")

                yield Label("Profile to Apply", classes="section-header")
                yield OptionList(id="assignment_profile_list")

            with Vertical(id="room-profile-rooms-col"):
                yield Label("Rooms", classes="section-header")
                yield Label(
                    "Select rooms to assign profile. Current profile is shown per room.",
                    id="assignment_help",
                )
                yield OptionList(id="assignment_room_list")

                with Horizontal(id="assignment-actions"):
                    yield Button("Select All Visible", id="btn_assignment_select_all")
                    yield Button("Clear Selection", id="btn_assignment_clear")

                yield Label("Selected profile: none", id="assignment_selected_profile")

                with Horizontal(id="assignment-apply-actions"):
                    yield Button("Apply Profile to Selected Rooms", id="btn_assignment_apply", variant="primary")

    def on_mount(self) -> None:
        self._refresh_floor_list()
        self._refresh_room_type_list()
        self._refresh_profile_list()
        self._refresh_room_list()

    def _room_key(self, floor: int, room_number: int) -> str:
        return f"{floor}:{room_number}"

    def _parse_room_key(self, key: str) -> tuple[int, int]:
        floor_str, room_number_str = key.split(":", maxsplit=1)
        return int(floor_str), int(room_number_str)

    def _get_all_rooms(self):
        for floor in self.property_data.floors:
            for room in floor.rooms:
                yield room

    def _get_filtered_rooms(self):
        for room in self._get_all_rooms():
            if self.selected_floor is not None and room.floor != self.selected_floor:
                continue
            if self.selected_room_type_id is not None and room.type_id != self.selected_room_type_id:
                continue
            yield room

    def _refresh_floor_list(self) -> None:
        floor_list = self.query_one("#assignment_floor_list", OptionList)
        floor_list.clear_options()
        floor_list.add_option(Option("All Floors", id="all"))

        for floor in sorted(self.property_data.floors, key=lambda f: f.level):
            floor_list.add_option(Option(f"Floor {floor.level}", id=str(floor.level)))

    def _refresh_room_type_list(self) -> None:
        room_type_list = self.query_one("#assignment_room_type_list", OptionList)
        room_type_list.clear_options()
        room_type_list.add_option(Option("All Room Types", id="all"))

        for room_type_id, room_type in ROOM_TYPE_CATALOG.room_types.items():
            room_type_list.add_option(Option(f"{room_type.display_name}", id=str(room_type_id)))

    def _refresh_profile_list(self) -> None:
        profile_list = self.query_one("#assignment_profile_list", OptionList)
        profile_list.clear_options()

        if self.selected_room_type_id is None:
            profile_list.add_option(Option("Select a room type first", id="none"))
            self.selected_profile_id = None
            self.query_one("#assignment_selected_profile", Label).update("Selected profile: none")
            return

        profiles = LIGHTING_PROFILE_CATALOG.get_for_room_type(self.selected_room_type_id)
        if not profiles:
            profile_list.add_option(Option("No profiles for this room type", id="none"))
            self.selected_profile_id = None
            self.query_one("#assignment_selected_profile", Label).update("Selected profile: none")
            return

        for profile in profiles:
            profile_list.add_option(Option(profile.name, id=str(profile.id)))

        # Keep previous selected profile if still valid.
        if self.selected_profile_id not in {profile.id for profile in profiles}:
            self.selected_profile_id = profiles[0].id

        if self.selected_profile_id is None:
            self.query_one("#assignment_selected_profile", Label).update("Selected profile: none")
            return

        selected_profile = LIGHTING_PROFILE_CATALOG.get(self.selected_profile_id)
        if selected_profile:
            self.query_one("#assignment_selected_profile", Label).update(
                f"Selected profile: {selected_profile.name}"
            )
        else:
            self.query_one("#assignment_selected_profile", Label).update("Selected profile: none")

    def _refresh_room_list(self) -> None:
        room_list = self.query_one("#assignment_room_list", OptionList)
        room_list.clear_options()

        for room in self._get_filtered_rooms():
            key = self._room_key(room.floor, room.number)
            marker = "[x]" if key in self.selected_room_keys else "[ ]"

            room_type = ROOM_TYPE_CATALOG.get_by_id(room.type_id)
            room_type_name = room_type.display_name if room_type else str(room.type_id)

            current_profile_name = "None"
            if getattr(room, "profile_id", None):
                current_profile = LIGHTING_PROFILE_CATALOG.get(room.profile_id)
                if current_profile:
                    current_profile_name = current_profile.name

            label = (
                f"{marker} Room {room.floor}-{room.number} ({room_type_name}) | Current: {current_profile_name}"
            )
            room_list.add_option(Option(label, id=key))

    def _toggle_room_selected(self, room_key: str) -> None:
        if room_key in self.selected_room_keys:
            self.selected_room_keys.remove(room_key)
        else:
            self.selected_room_keys.add(room_key)
        self._refresh_room_list()

    def _select_all_visible_rooms(self) -> None:
        for room in self._get_filtered_rooms():
            self.selected_room_keys.add(self._room_key(room.floor, room.number))
        self._refresh_room_list()

    def _clear_selected_rooms(self) -> None:
        self.selected_room_keys.clear()
        self._refresh_room_list()

    def _apply_profile_to_selected_rooms(self) -> None:
        if self.selected_profile_id is None:
            self.notify("Select a profile to apply.", severity="warning")
            return

        target_rooms = []
        selected = set(self.selected_room_keys)
        for room in self._get_all_rooms():
            if self._room_key(room.floor, room.number) in selected:
                target_rooms.append(room)

        if not target_rooms:
            self.notify("Select at least one room.", severity="warning")
            return

        profile = LIGHTING_PROFILE_CATALOG.get(self.selected_profile_id)
        if profile is None:
            self.notify("Selected profile not found.", severity="error")
            return

        applied_count = 0
        for room in target_rooms:
            # Safety guard: apply only compatible profile for this room type.
            if room.type_id != profile.room_type_id:
                continue
            room.profile_id = profile.id
            applied_count += 1

        self._refresh_room_list()

        if applied_count == 0:
            self.notify("No matching room types in selected rooms for this profile.", severity="warning")
            return

        self.notify(f"Applied '{profile.name}' to {applied_count} room(s).")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        list_id = event.option_list.id
        option_id = event.option.id

        if not option_id:
            return

        if list_id == "assignment_floor_list":
            self.selected_floor = None if option_id == "all" else int(option_id)
            self.selected_room_keys.clear()
            self._refresh_room_list()
            return

        if list_id == "assignment_room_type_list":
            self.selected_room_type_id = None if option_id == "all" else RoomTypeId(option_id)
            self.selected_room_keys.clear()
            self._refresh_profile_list()
            self._refresh_room_list()
            return

        if list_id == "assignment_profile_list":
            if option_id == "none":
                self.selected_profile_id = None
                self.query_one("#assignment_selected_profile", Label).update("Selected profile: none")
                return

            self.selected_profile_id = ProfileId(option_id)
            profile = LIGHTING_PROFILE_CATALOG.get(self.selected_profile_id)
            profile_name = profile.name if profile else "none"
            self.query_one("#assignment_selected_profile", Label).update(
                f"Selected profile: {profile_name}"
            )
            return

        if list_id == "assignment_room_list":
            self._toggle_room_selected(option_id)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "btn_assignment_select_all":
            self._select_all_visible_rooms()
            return

        if button_id == "btn_assignment_clear":
            self._clear_selected_rooms()
            return

        if button_id == "btn_assignment_apply":
            self._apply_profile_to_selected_rooms()
