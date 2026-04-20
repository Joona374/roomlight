from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane

from src.models.logical.room_light_system import RoomLightSystem
from src.models.physical.property import Property
from src.tui.tui_style import TUI_STYLE
from src.tui.views.physical_view.physical_view import PhysicalView
from src.tui.views.config_view.config_view import ConfigView
from src.tui.views.staff_view import StaffView


class RoomLightApp(App):
    CSS = TUI_STYLE

    def __init__(self, property_data: Property, roomlight: RoomLightSystem):
        super().__init__()
        self.hotel_property = property_data
        self.roomlight = roomlight

    def compose(self) -> ComposeResult:
        yield Header()

        with TabbedContent():
            with TabPane("Physical"):
                # This view represents the actual physical state of the hotel
                # So its just a simulation level representation of the physical rooms
                # the guests see and interact with, and the state of the lighting units in those rooms.
                yield PhysicalView(self.hotel_property)

            with TabPane("Config"):
                # This view represents the configuration and setup options of the RoomLight system,
                # so its more of a technical staff / admin view.
                yield ConfigView(self.roomlight, self.hotel_property)

            with TabPane("Staff"):
                # This view represents the interface used for daily operations by staff.
                yield StaffView(self.roomlight)

        yield Footer()

    def on_mount(self) -> None:
        # Advance simulation time globally so staff timers keep running across view switches.
        self.set_interval(1.0, self._tick_simulation_clock)

    def _tick_simulation_clock(self) -> None:
        self.roomlight.tick_one_minute()
