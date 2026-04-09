import uuid

from src.types import Brightness

class LightUnit:
    """
    This model represents a single controllable light fixture in a room.
    The 'brightness' attribute simulates the state of the light, and methods allow changing it.
    The unit shouldnt be a adjusted directly, but instead all interactions should go through the control panel
    to mimic the real-world setup.
    """
    def __init__(self):
        self.hardware_id: str = f"LIGHT_{str(uuid.uuid4())}"  # Randomized IDs help simulate real hardware identity.
        self.brightness: Brightness = Brightness.OFF  # Brightness has discrete levels defined in the Brightness enum INCLUDING OFF

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
        # We wake up at LOW to avoid sudden full brightness in a hotel context.
        if self.brightness == Brightness.OFF:
            self.brightness = Brightness.LOW

    def turn_off(self):
        self.brightness = Brightness.OFF
