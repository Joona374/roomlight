from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, Button, ContentSwitcher

from src.models.logical.room_light_system import RoomLightSystem
from src.models.physical.property import Property
from src.tui.views.config_view.room_types_view import RoomTypesView
from src.tui.views.config_view.profiles_view import ProfilesView
from src.tui.views.config_view.room_profile_assignment_view import RoomProfileAssignmentView


class ConfigView(Container):

    def __init__(self, roomlight: RoomLightSystem, property_data: Property):
        super().__init__()
        self.roomlight = roomlight
        self.property_data = property_data

    def compose(self):
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Config Sections")
                # Add 'id' to buttons to identify them in the handler
                yield Button("Room Types", id="btn_room_types")
                yield Button("Lighting Profiles", id="btn_profiles")
                yield Button("Room Profile Assignment", id="btn_room_profile_assignment")

            # ContentSwitcher manages the visible area
            with ContentSwitcher(initial="default-message", id="main-content"):
                yield RoomTypesView(id="view_room_types", roomlight=self.roomlight)
                yield ProfilesView(id="view_profiles", roomlight=self.roomlight)
                yield RoomProfileAssignmentView(id="view_room_profile_assignment", property_data=self.property_data)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when any button inside this container is pressed."""
        switcher = self.query_one("#main-content", ContentSwitcher)

        if event.button.id == "btn_room_types":
            switcher.current = "view_room_types"
        elif event.button.id == "btn_profiles":
            switcher.current = "view_profiles"
        elif event.button.id == "btn_room_profile_assignment":
            switcher.current = "view_room_profile_assignment"
