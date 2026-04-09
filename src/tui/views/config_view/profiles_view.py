from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, SelectionList

from src.models.logical.room_light_system import RoomLightSystem


class ProfilesView(Vertical):
    """A dedicated view for lighting profiles."""
    def __init__(self, roomlight: RoomLightSystem, **kwargs):
        super().__init__(**kwargs)
        self.roomlight = roomlight

    def compose(self) -> ComposeResult:
        yield Label("Lighting Profiles", id="title")
        # Example of a different widget for this view
        yield SelectionList(
            ("Cinema Mode", "cinema"),
            ("Reading", "reading"),
            ("All Off", "off"),
        )
