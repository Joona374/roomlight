import uuid

from src.types import Brightness

class LightUnit:
    def __init__(self):
        self.hardware_id: str = str(uuid.uuid4())
        self.on: bool = False
        self.brightness: Brightness = Brightness.MEDIUM

    def toggle(self):
        self.on = not self.on
