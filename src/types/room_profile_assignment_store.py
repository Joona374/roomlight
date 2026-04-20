import json
from pathlib import Path

from src.types.types import ProfileId


class RoomProfileAssignmentStore:
    """Persistent mapping of room keys ("floor:number") to assigned profile IDs."""

    def __init__(self, path: str | None = None) -> None:
        current_dir = Path(__file__).parent
        default_path = current_dir / "room_profile_assignments.json"
        self.path = Path(path) if path else default_path
        self.assignments: dict[str, ProfileId] = {}

    def load(self) -> None:
        if not self.path.exists():
            self.assignments = {}
            return

        with open(self.path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        if not isinstance(raw, dict):
            self.assignments = {}
            return

        self.assignments = {
            str(room_key): ProfileId(str(profile_id))
            for room_key, profile_id in raw.items()
        }

    def save(self) -> None:
        serializable = {room_key: str(profile_id) for room_key, profile_id in self.assignments.items()}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)

    def get(self, room_key: str) -> ProfileId | None:
        return self.assignments.get(room_key)

    def set(self, room_key: str, profile_id: ProfileId) -> None:
        self.assignments[room_key] = profile_id

    def delete(self, room_key: str) -> None:
        self.assignments.pop(room_key, None)


ROOM_PROFILE_ASSIGNMENT_STORE = RoomProfileAssignmentStore()
