from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, Button, ContentSwitcher

from src.models.logical.room_light_system import RoomLightSystem
from src.tui.views.config_view.room_types_view import RoomTypesView
from src.tui.views.config_view.profiles_view import ProfilesView


class ConfigView(Container):

    def __init__(self, roomlight: RoomLightSystem):
        super().__init__()
        self.roomlight = roomlight

    def compose(self):
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Config Sections")
                # Add 'id' to buttons to identify them in the handler
                yield Button("Room Types", id="btn_room_types")
                yield Button("Lighting Profiles", id="btn_profiles")

            # ContentSwitcher manages the visible area
            with ContentSwitcher(initial="default-message", id="main-content"):
                yield RoomTypesView(id="view_room_types", roomlight=self.roomlight)
                yield ProfilesView(id="view_profiles", roomlight=self.roomlight)


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when any button inside this container is pressed."""
        switcher = self.query_one("#main-content", ContentSwitcher)

        if event.button.id == "btn_room_types":
            switcher.current = "view_room_types"
        elif event.button.id == "btn_profiles":
            switcher.current = "view_profiles"
