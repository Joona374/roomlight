from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, Button, Label
from textual.containers import Container, Vertical, Horizontal  # Added Horizontal
from src.models.physical.property import Property
from src.models.physical.light_unit import LightUnit
from src.tui.tui_style import TUI_STYLE

# Import your new widget!
from src.tui.widgets import RoomVisualizer, BrightnessDownButton, BrightnessUpButton


class LightButton(Button):
    def __init__(self, label: str, light_unit: LightUnit, id: str, classes: str):
        super().__init__(label, id=id, classes=classes)
        self.light_unit = light_unit


class RoomLightApp(App):
    CSS = TUI_STYLE

    def __init__(self, property_data: Property):
        super().__init__()
        self.hotel_property = property_data

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(Tree("Hotel Property", id="navigation"), id="sidebar")
        yield Container(id="room-view")
        yield Footer()

    def on_mount(self) -> None:
        tree = self.query_one("#navigation", Tree)
        tree.root.expand()

        for floor in self.hotel_property.floors:
            floor_node = tree.root.add(f"Floor {floor.level}", expand=True)
            floor_node.collapse()
            for room in floor.rooms:
                floor_node.add_leaf(room.id, data=room)

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        room = event.node.data
        if room:
            await self.display_room(room)  # schedule async call

    async def display_room(self, room):
        view = self.query_one("#room-view")
        await view.query("#room-content").remove()

        content = Horizontal(Container(RoomVisualizer(room), id="visualizer-container"), Vertical(id="controls-container"), id="room-content")
        await view.mount(content)

        controls = self.query_one("#controls-container")
        await controls.mount(Label(f"Room: {room.id} Panel"))

        for label, unit in room.control_panel.connected_lights.items():
            hw_id = unit.hardware_id
            row = Vertical(
                Label(label, classes="light-label"), Horizontal(BrightnessDownButton(unit, id=f"DOWN_{hw_id}"), BrightnessUpButton(unit, id=f"UP_{hw_id}"), classes="light-buttons"), classes="light-row"
            )
            await controls.mount(row)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button
        if isinstance(btn, BrightnessDownButton):
            btn.light_unit.decrease_brightness()
        elif isinstance(btn, BrightnessUpButton):
            btn.light_unit.increase_brightness()
        else:
            return

        try:
            self.query_one(RoomVisualizer).trigger_redraw()
        except:
            pass
