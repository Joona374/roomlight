from textual.widget import Widget
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Tree, Label, Button

from src.models.physical.property import Property
from src.models.physical.room import Room
from src.tui.views.physical_view.widgets import (
    RoomVisualizer,
    BrightnessDownButton,
    BrightnessUpButton,
    ProfileToggleButton,
    ProfileAdjustDownButton,
    ProfileAdjustUpButton,
)
from src.types.lightning_profile_catalog import LIGHTING_PROFILE_CATALOG
from src.types.types import LightingProfile, ToggleControl, AdjustControl


class PhysicalView(Container):

    def __init__(self, property_data: Property):
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
        room: Room | None = event.node.data
        if room:
            await self.display_room(room)

    # ✅ moved here
    async def display_room(self, room: Room):
        self.current_room = room
        view = self.query_one("#room-view")

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

        profile = None
        if getattr(room, "profile_id", None):
            profile = LIGHTING_PROFILE_CATALOG.get(room.profile_id)

        if profile:
            await self._mount_profile_controls(room, profile)
        else:
            await self._mount_fallback_controls(room)

    async def _mount_profile_controls(self, room: Room, profile: LightingProfile):
        controls = self.query_one("#controls-container")

        for control in profile.controls:
            if isinstance(control, ToggleControl):
                row = Horizontal(
                    ProfileToggleButton(control, id=f"PT_{control.id}"),
                    classes="light-buttons",
                )
                await controls.mount(
                    Vertical(
                        Label(control.label, classes="light-label"),
                        row,
                        classes="light-row",
                    )
                )

            elif isinstance(control, AdjustControl):
                row = Horizontal(
                    ProfileAdjustDownButton(control, id=f"PAD_{control.id}"),
                    ProfileAdjustUpButton(control, id=f"PAU_{control.id}"),
                    classes="light-buttons",
                )
                await controls.mount(
                    Vertical(
                        Label(control.label, classes="light-label"),
                        row,
                        classes="light-row",
                    )
                )

    async def _mount_fallback_controls(self, room):
        controls = self.query_one("#controls-container")
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
        room = self.current_room
        if room is None:
            return

        if isinstance(btn, BrightnessDownButton):
            btn.light_unit.decrease_brightness()
        elif isinstance(btn, BrightnessUpButton):
            btn.light_unit.increase_brightness()
        elif isinstance(btn, ProfileToggleButton):
            room.control_panel.apply_toggle_control(btn.control)
        elif isinstance(btn, ProfileAdjustDownButton):
            room.control_panel.apply_adjust_control(btn.control, -1)
        elif isinstance(btn, ProfileAdjustUpButton):
            room.control_panel.apply_adjust_control(btn.control, +1)
        else:
            return

        self.query_one(RoomVisualizer).trigger_redraw()
