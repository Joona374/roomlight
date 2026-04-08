from src.types import RoomType, ROOM_CONFIGURATIONS
from src.models.physical.light_unit import LightUnit
from src.models.physical.room_control_panel import RoomControlPanel


class Room:
    def __init__(self, id: str, type: RoomType) -> None:
        self.id: str = id
        self.type: RoomType = type

        self.control_panel: RoomControlPanel = self.generate_mock_control_panel()
        self.light_units: list[LightUnit] = self.generate_mock_light_units()


        
    def generate_mock_control_panel(self) -> RoomControlPanel:
        panel = RoomControlPanel(self)
        return panel
    
    def generate_mock_light_units(self) -> list[LightUnit]:
        units = []
        for _ in range(ROOM_CONFIGURATIONS[self.type]["light_count"]):
            unit = LightUnit()
            units.append(unit)

        return units
    
    def connect_light_units_to_panel(self):
        for i, unit in enumerate(self.light_units):
            label = ROOM_CONFIGURATIONS[self.type]["labels"][i]
            self.control_panel.connect_light_unit(label, unit)
        