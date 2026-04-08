import uuid

from src.types import Brightness

class LightUnit:
    def __init__(self):
        self.hardware_id: str = f"LIGHT_{str(uuid.uuid4())}"
        self.brightness: Brightness = Brightness.OFF

    def increase_brightness(self):
        levels = list(Brightness)
        current_index = levels.index(self.brightness)
        if current_index < len(levels) - 1:
            self.brightness = levels[current_index + 1]

    def decrease_brightness(self):
        levels = list(Brightness)
        current_index = levels.index(self.brightness)
        if current_index > 0:
            self.brightness = levels[current_index - 1]

    def turn_on(self):
        if self.brightness == Brightness.OFF:
            self.brightness = Brightness.LOW

    def turn_off(self):
        self.brightness = Brightness.OFF
