import json
from pathlib import Path
from src.types.types import RoomTypeId, RoomTypeTemplate

class RoomTypeCatalog:
    def __init__(self, path: str | None = None) -> None:
        current_dir = Path(__file__).parent
        default_path = current_dir / "room_types.json"
        self.path = Path(path) if path else default_path
        self.room_types: dict[RoomTypeId, RoomTypeTemplate] = {}

    def load(self) -> None:
        with open(self.path, "r", encoding="utf-8") as f:
            rooms = json.load(f)
            if rooms:
                self.room_types = {RoomTypeId(room["id"]): RoomTypeTemplate(**room) for room in rooms}

    def save(self) -> None:
        serializable = []
        for _, template in self.room_types.items():
            serializable.append({
                "id": str(template.id),
                "display_name": template.display_name,
                "light_labels": template.light_labels,
                "light_count": template.light_count
                })

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)

    def get_by_id(self, room_type_id: RoomTypeId) -> RoomTypeTemplate | None:
        return self.room_types.get(room_type_id)

ROOM_TYPE_CATALOG = RoomTypeCatalog()
