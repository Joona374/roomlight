from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Label, Input, Button, OptionList
from textual.widgets.option_list import Option

from src.models.logical.room_light_system import RoomLightSystem
from src.types.room_type_catalog import ROOM_TYPE_CATALOG
from src.types.types import RoomTypeId, RoomTypeTemplate


class LightInputRow(Horizontal):
    """A custom row containing an input for a light label and a delete button."""

    def __init__(self, value: str = "", **kwargs):
        super().__init__(**kwargs)
        self.initial_value = value

    def compose(self) -> ComposeResult:
        yield Input(value=self.initial_value, classes="light-name-input")
        yield Button("X", variant="error", classes="btn-remove-light")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.has_class("btn-remove-light"):
            self.remove()
            event.stop()


class RoomTypesView(Vertical):
    """A dedicated CRUD view for configuring room types."""

    def __init__(self, roomlight: RoomLightSystem, **kwargs):
        super().__init__(**kwargs)
        self.roomlight = roomlight
        self.selected_id: str | None = None

    def compose(self) -> ComposeResult:
        yield Label("Room Type Configuration", id="title")

        with Horizontal():
            # LEFT COLUMN: Metadata, Navigation, and Persistence
            with Vertical(id="left-config-col"):
                yield Label("Existing Room Types", classes="section-header")
                yield OptionList(id="room_list")

                with Horizontal(id="list-actions"):
                    yield Button("New", id="btn_new", variant="success")
                    yield Button("Delete", id="btn_delete", variant="error")

                yield Label("Room ID:", classes="field-label")
                yield Input(placeholder="e.g. kitchen", id="input_id")

                yield Label("Display Name:", classes="field-label")
                yield Input(placeholder="e.g. Kitchen", id="input_name")

                # The 'Save to Memory' button acts as the 'Apply Changes' button
                yield Button("Update Memory", id="btn_save_memory", variant="primary")
                # The 'Save to Disk' button pinned at the bottom
                yield Button("Save to JSON", id="btn_save_disk", variant="success")

            # RIGHT COLUMN: Scrollable Light Units
            with VerticalScroll(id="right-lights-col"):
                yield Label("Light Units", classes="section-header")
                yield Vertical(id="lights_container")
                yield Button("+ Add Light Unit", id="btn_add_light", variant="success")

    def on_mount(self) -> None:
        self.refresh_list()

    def refresh_list(self) -> None:
        option_list = self.query_one("#room_list", OptionList)
        option_list.clear_options()
        for r_id, r_type in ROOM_TYPE_CATALOG.room_types.items():
            option_list.add_option(Option(f"{r_type.display_name} ({r_id})", id=r_id))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        room_id = event.option.id
        if room_id:
            room_type = ROOM_TYPE_CATALOG.get_by_id(RoomTypeId(room_id))
            if room_type:
                self.selected_id = room_id
                self.query_one("#input_id", Input).value = str(room_type.id)
                self.query_one("#input_name", Input).value = room_type.display_name
                self.populate_lights(room_type.light_labels)

    def populate_lights(self, labels: list[str]) -> None:
        container = self.query_one("#lights_container")
        container.remove_children()
        for label in labels:
            container.mount(LightInputRow(value=label))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "btn_new":
            self._add_new_roomtype()

        elif button_id == "btn_add_light":
            self._add_light_unit_input()

        elif button_id == "btn_save_memory":
            self._save_updated_roomtypes_to_memory()

        elif button_id == "btn_delete":
            self._delete_room_type()

        elif button_id == "btn_save_disk":
            self._save_to_json()


    def _add_light_unit_input(self):
        self.query_one("#lights_container").mount(LightInputRow())

    def _add_new_roomtype(self):
        self.selected_id = None
        self.query_one("#input_id", Input).value = ""
        self.query_one("#input_name", Input).value = ""
        self.query_one("#lights_container").remove_children()
        self.notify("Form cleared for new room type.")


    def _delete_room_type(self):
        if not self.selected_id:
            self.notify("No room type selected to delete.", severity="error")
            return

        ROOM_TYPE_CATALOG.room_types.pop(RoomTypeId(self.selected_id), None)
        self.query_one("#btn_new", Button).press()                
        self.refresh_list()
        self.notify("Deleted from memory.")

    def _save_updated_roomtypes_to_memory(self):
            r_id_str = self.query_one("#input_id", Input).value.strip()
            name = self.query_one("#input_name", Input).value.strip()

            if not r_id_str or not name:
                self.notify("ID and Name are required", severity="error")
                return

            light_inputs = self.query_one("#lights_container").query(Input)
            labels = [i.value.strip() for i in light_inputs if i.value.strip()]

            r_id = RoomTypeId(r_id_str)
            new_roomtype = RoomTypeTemplate(id=r_id, display_name=name, light_count=len(labels), light_labels=labels)

            # Cleanup if ID changed
            if self.selected_id and self.selected_id != r_id_str:
                ROOM_TYPE_CATALOG.room_types.pop(RoomTypeId(self.selected_id), None)

            ROOM_TYPE_CATALOG.room_types[r_id] = new_roomtype
            self.selected_id = r_id_str
            self.refresh_list()
            self.notify(f"Updated {name}")


    def _save_to_json(self):
        ROOM_TYPE_CATALOG.save()
        self.notify("Saved to room_types.json", severity="information")