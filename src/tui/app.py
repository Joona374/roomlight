from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane

from src.tui.tui_style import TUI_STYLE
from src.tui.views.physical_view import PhysicalView
from src.tui.views.config_view import ConfigView
from src.tui.views.staff_view import StaffView


class RoomLightApp(App):
    CSS = TUI_STYLE  # ✅ stays here

    def __init__(self, property_data):
        super().__init__()
        self.hotel_property = property_data

    def compose(self) -> ComposeResult:
        yield Header()

        with TabbedContent():
            with TabPane("Physical"):
                yield PhysicalView(self.hotel_property)

            with TabPane("Config"):
                yield ConfigView()

            with TabPane("Staff"):
                yield StaffView()

        yield Footer()
