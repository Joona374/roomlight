from textual.widget import Widget
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Tree, Label, Button

from src.tui.widgets import RoomVisualizer, BrightnessDownButton, BrightnessUpButton


class PhysicalView(Container):

    def __init__(self, property_data):
        super().__init__()
        self.hotel_property = property_data

    def compose(self):
        yield Vertical(Tree("Hotel Property", id="navigation"), id="sidebar")
        yield Container(id="room-view")

    def on_mount(self):
        tree = self.query_one("#navigation", Tree)
        tree.root.expand()

        for floor in self.hotel_property.floors:
            floor_node = tree.root.add(f"Floor {floor.level}", expand=True)
            floor_node.collapse()
            for room in floor.rooms:
                floor_node.add_leaf(room.id, data=room)

    # ✅ moved here
    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        room = event.node.data
        if room:
            await self.display_room(room)

    # ✅ moved here
    async def display_room(self, room):
        view = self.query_one("#room-view")

        # safer remove (avoid crash if first time)
        old = view.query("#room-content")
        if old:
            await old.remove()

        content = Horizontal(
            Container(RoomVisualizer(room), id="visualizer-container"),
            Vertical(id="controls-container"),
            id="room-content",
        )

        await view.mount(content)

        controls = self.query_one("#controls-container")
        await controls.mount(Label(f"Room: {room.id} Panel"))

        for label, unit in room.control_panel.connected_lights.items():
            hw_id = unit.hardware_id

            row = Vertical(
                Label(label, classes="light-label"),
                Horizontal(
                    BrightnessDownButton(unit, id=f"DOWN_{hw_id}"),
                    BrightnessUpButton(unit, id=f"UP_{hw_id}"),
                    classes="light-buttons",
                ),
                classes="light-row",
            )

            await controls.mount(row)

    # ✅ moved here
    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button

        if isinstance(btn, BrightnessDownButton):
            btn.light_unit.decrease_brightness()
        elif isinstance(btn, BrightnessUpButton):
            btn.light_unit.increase_brightness()
        else:
            return

        # redraw ONLY inside this view
        try:
            self.query_one(RoomVisualizer).trigger_redraw()
        except:
            pass
