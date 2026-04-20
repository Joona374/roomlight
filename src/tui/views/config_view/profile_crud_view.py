from collections.abc import Callable

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Label, OptionList
from textual.widgets.option_list import Option

from src.models.logical.room_light_system import RoomLightSystem
from src.types.lightning_profile_catalog import LIGHTING_PROFILE_CATALOG
from src.types.room_type_catalog import ROOM_TYPE_CATALOG
from src.types.types import LightingProfile, ProfileId, RoomTypeId


class ProfileCrudView(Vertical):
    def __init__(
        self,
        roomlight: RoomLightSystem,
        on_profile_selected: Callable[[LightingProfile | None], None] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.roomlight = roomlight
        self.on_profile_selected = on_profile_selected
        self.selected_room_type_id: RoomTypeId | None = None
        self.selected_profile_id: ProfileId | None = None

    def compose(self) -> ComposeResult:
        with Vertical(id="profile-crud-column"):
            yield Label("Room Types", classes="section-header")
            yield OptionList(id="room_type_list")

            yield Label("Profiles", classes="section-header")
            yield OptionList(id="profile_list")

            with Horizontal(id="list-actions"):
                yield Button("New Profile", id="btn_new_profile", variant="success")
                yield Button("Delete Profile", id="btn_delete_profile", variant="error")

            yield Label("Profile Metadata", classes="section-header")

            yield Label("Profile Name", classes="field-label")
            yield Input(placeholder="e.g. Suite Default", id="input_profile_name")

            yield Label("Room Type ID", classes="field-label")
            yield Input(disabled=True, id="input_room_type_id")

            with Horizontal(id="profile-meta-actions"):
                yield Button("Update Memory", id="btn_save_memory", variant="primary")
                yield Button("Save to JSON", id="btn_save_disk", variant="success")

    def _generate_profile_id(self, profile_name: str) -> ProfileId:
        return ProfileId(profile_name.strip().lower().replace(" ", "-"))

    def _notify_profile_selected(self, profile: LightingProfile | None) -> None:
        if self.on_profile_selected is not None:
            self.on_profile_selected(profile)

    def on_mount(self) -> None:
        self._refresh_room_type_list()
        self._notify_profile_selected(None)

    def _refresh_room_type_list(self) -> None:
        room_type_list = self.query_one("#room_type_list", OptionList)
        room_type_list.clear_options()

        for room_type_id, room_type in ROOM_TYPE_CATALOG.room_types.items():
            room_type_list.add_option(Option(f"{room_type.display_name} ({room_type_id})", id=str(room_type_id)))

    def _refresh_profile_list(self) -> None:
        profile_list = self.query_one("#profile_list", OptionList)
        profile_list.clear_options()

        if self.selected_room_type_id is None:
            return

        profiles = LIGHTING_PROFILE_CATALOG.get_for_room_type(self.selected_room_type_id)
        for profile in profiles:
            profile_list.add_option(Option(profile.name, id=str(profile.id)))

    def _load_profile_into_form(self, profile: LightingProfile) -> None:
        self.query_one("#input_profile_name", Input).value = profile.name
        self.query_one("#input_room_type_id", Input).value = str(profile.room_type_id)

    def _clear_profile_form(self) -> None:
        self.selected_profile_id = None
        self.query_one("#input_profile_name", Input).value = ""
        self.query_one("#input_room_type_id", Input).value = str(self.selected_room_type_id) if self.selected_room_type_id else ""

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        list_id = event.option_list.id
        option_id = event.option.id

        if not option_id:
            return

        if list_id == "room_type_list":
            self.selected_room_type_id = RoomTypeId(option_id)
            self.selected_profile_id = None
            self._refresh_profile_list()
            self._clear_profile_form()
            self._notify_profile_selected(None)
            return

        if list_id == "profile_list":
            profile = LIGHTING_PROFILE_CATALOG.get(ProfileId(option_id))
            if profile is None:
                self.notify("Profile not found.", severity="error")
                self._notify_profile_selected(None)
                return
            self.selected_profile_id = profile.id
            self.selected_room_type_id = profile.room_type_id
            self._load_profile_into_form(profile)
            self._notify_profile_selected(profile)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "btn_new_profile":
            if self.selected_room_type_id is None:
                self.notify("Select a room type first.", severity="warning")
                return
            self._clear_profile_form()
            self._notify_profile_selected(None)
            self.notify("New profile draft ready.")

        elif button_id == "btn_save_memory":
            self._save_profile_to_memory()

        elif button_id == "btn_save_disk":
            LIGHTING_PROFILE_CATALOG.save()
            self.notify("Saved lighting profiles to JSON.")

        elif button_id == "btn_delete_profile":
            self._delete_selected_profile()

    def _save_profile_to_memory(self) -> None:
        if self.selected_room_type_id is None:
            self.notify("Select a room type first.", severity="error")
            return

        profile_name = self.query_one("#input_profile_name", Input).value.strip()

        if not profile_name:
            self.notify("Profile name is required.", severity="error")
            return

        generated_id = self._generate_profile_id(profile_name)

        existing_profile = None
        if self.selected_profile_id:
            existing_profile = LIGHTING_PROFILE_CATALOG.get(self.selected_profile_id)
        if existing_profile is None:
            existing_profile = LIGHTING_PROFILE_CATALOG.get(generated_id)

        profile = LightingProfile(
            id=generated_id,
            room_type_id=self.selected_room_type_id,
            name=profile_name,
            controls=existing_profile.controls if existing_profile else [],
        )

        if self.selected_profile_id and self.selected_profile_id != generated_id:
            LIGHTING_PROFILE_CATALOG.delete(self.selected_profile_id)

        LIGHTING_PROFILE_CATALOG.upsert(profile)
        self.selected_profile_id = profile.id
        self._refresh_profile_list()
        self._notify_profile_selected(profile)
        self.notify(f"Profile '{profile.name}' updated in memory.")

    def _delete_selected_profile(self) -> None:
        if self.selected_profile_id is None:
            self.notify("No profile selected to delete.", severity="warning")
            return

        LIGHTING_PROFILE_CATALOG.delete(self.selected_profile_id)
        self._refresh_profile_list()
        self._clear_profile_form()
        self._notify_profile_selected(None)
        self.notify("Profile deleted from memory.")
