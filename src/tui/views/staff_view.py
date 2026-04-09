from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, Button

from src.models.logical.room_light_system import RoomLightSystem

class StaffView(Container):

    def __init__(self, roomlight: RoomLightSystem):
        super().__init__()
        self.roomlight = roomlight

    def compose(self):
        yield Horizontal(
            Vertical(
                Label("Staff Actions"), 
                Button("Turn off floor"), 
                Button("Emergency mode"), 
                id="sidebar"
            ), 
            Container(
                Label("Staff dashboard"), 
                id="main-content"
            )
        )
