from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, ContentSwitcher, Label

from src.models.logical.room_light_system import RoomLightSystem
from src.tui.views.staff_view.check_ins_view import CheckInsView
from src.tui.views.staff_view.check_outs_view import CheckOutsView


class StaffView(Container):
    def __init__(self, roomlight: RoomLightSystem):
        super().__init__()
        self.roomlight = roomlight

    def compose(self):
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Staff Sections")
                yield Button("Check-ins", id="btn_check_ins")
                yield Button("Check-outs", id="btn_check_outs")

            with ContentSwitcher(initial="view_check_ins", id="main-content"):
                yield CheckInsView(id="view_check_ins", roomlight=self.roomlight)
                yield CheckOutsView(id="view_check_outs", roomlight=self.roomlight)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        switcher = self.query_one("#main-content", ContentSwitcher)

        if event.button.id == "btn_check_ins":
            switcher.current = "view_check_ins"
        elif event.button.id == "btn_check_outs":
            switcher.current = "view_check_outs"
