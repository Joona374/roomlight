from textual.widgets import Button
from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text

from src.models.physical.light_unit import LightUnit
from src.models.physical.room import Room
from src.types import RoomType
from src.types import Brightness


class BrightnessDownButton(Button):
    def __init__(self, light_unit: LightUnit, id: str):
        super().__init__("−", id=id, classes="brightness-btn")
        self.light_unit = light_unit


class BrightnessUpButton(Button):
    def __init__(self, light_unit: LightUnit, id: str):
        super().__init__("+", id=id, classes="brightness-btn")
        self.light_unit = light_unit


class RoomVisualizer(Widget):
    update_trigger = reactive(0)

    def __init__(self, room: "Room"):
        super().__init__()
        self.room = room

    def trigger_redraw(self):
        self.update_trigger += 1

    def _light_indicator(self, label: str) -> str:
        unit = self.room.control_panel.connected_lights.get(label)
        if unit is None or unit.brightness == Brightness.OFF:
            return "⚫ OFF"
        if unit.brightness == Brightness.LOW:
            return "🔴 DIM"
        elif unit.brightness == Brightness.MEDIUM:
            return "🟡 MED"
        else:  # HIGH
            return "🟢 HI "

    def render(self) -> Text:
        # 1. Create the dictionary of live light indicators
        # We use .get() with a fallback to avoid crashes if a label is missing
        lights = {
            label: self._light_indicator(label)
            for label in self.room.control_panel.connected_lights
        }

        # 2. Decide which drawing method to call based on the room type
        if self.room.type == RoomType.SUITE:
            lines = self._render_suite(lights)
        elif self.room.type == RoomType.CONFERENCE:
            lines = self._render_conference_room(lights)
        else:
            lines = self._render_normal(lights)

        return Text("\n".join(lines))




    def _render_normal(self, l: dict) -> list[str]:
        return [
            f"┌────────────────────────────┐",
            f"│                            │",
            f"│ {l.get('Entry', '  ---')}           {l.get('Main', '  ---')}    │",
            f"│                            │",
            f"├──    ──┐                   │",
            f"│        │                   │",
            f"│ {l.get('Bathroom', '  ---')} │                   │",
            f"│        │         {l.get('Bedside', '  ---')}    │",
            f"│        │                   │",
            f"└────────┴───────────────────┘",
        ]

    def _render_suite(self, l: dict) -> list[str]:
        return [
            f"┌────────────────┬───────────┐",
            f"│ {l.get('Entry', '  ---')}         │   {l.get('Bathroom', '---')}  │",
            f"│                │           │",
            f"│                └─    ──────┤",
            f"│                            │",
            f"├────    ──────┬─────    ────┤",
            f"│              │{l.get('Desk', '---')}       │",
            f"│              │             │",
            f"│   {l.get('Bedroom', '  ---')}     │             │",
            f"│              │             │",
            f"│              │    {l.get('Living', '  ---')}   │",
            f"└──────────────┴─────────────┘",
        ]

    def _render_conference_room(self, l: dict) -> list[str]:
        return [
            f"┌──────────────────────────────┐",
            f"│           {l.get('Stage', '  ---')}             │",
            f"│                              │",
            f"│                              │",
            f"│                              │",
            f"│                              │",
            f"│  {l.get('Left', '  ---')}              {l.get('Right', '  ---')}  │",
            f"│                              │",
            f"│                              │",
            f"│             {l.get('Center', '  ---')}           │",
            f"│                              │",
            f"│                              │",
            f"│                              │",
            f"│                              │",
            f"│            {l.get('Rear', '  ---')}            │",
            f"│                              │",
            f"│             ┌────────────────┤",
            f"│    {l.get('Entry', '  ---')}                    │",
            f"│                   {l.get('Bathroom', '---')}     │",
            f"│                              │",
            f"└───    ──────┴────────────────┘",
        ]
