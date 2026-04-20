import json
from pathlib import Path

from src.types.types import (
    AdjustControl,
    ControlKind,
    LightingProfile,
    ProfileId,
    RoomTypeId,
    ToggleControl,
)


class LightingProfileCatalog:
    def __init__(self, path: str | None = None) -> None:
        current_dir = Path(__file__).parent
        default_path = current_dir / "lighting_profiles.json"
        self.path = Path(path) if path else default_path
        self.profiles: dict[ProfileId, LightingProfile] = {}

    def load(self) -> None:
        if not self.path.exists():
            self.profiles = {}
            return

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        loaded: dict[ProfileId, LightingProfile] = {}
        for lighting_profile in data:
            controls = []

            for control in lighting_profile["controls"]:
                if control["kind"] == ControlKind.TOGGLE.value:
                    controls.append(ToggleControl.from_dict(control))

                elif control["kind"] == ControlKind.ADJUST.value:
                    controls.append(AdjustControl.from_dict(control))

            profile = LightingProfile.from_dict(lighting_profile, controls)

            loaded[profile.id] = profile

        self.profiles = loaded

    def save(self) -> None:
        data = []
        for profile in self.profiles.values():
            data.append(profile.to_dict())

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_all(self) -> list[LightingProfile]:
        return list(self.profiles.values())

    def get_for_room_type(self, room_type_id: RoomTypeId | None) -> list[LightingProfile]:
        if not room_type_id:
            raise ValueError("room_type_id cannot be None when fetching lighting profiles for a room type.")
        return [p for p in self.profiles.values() if p.room_type_id == room_type_id]

    def get(self, profile_id: ProfileId) -> LightingProfile | None:
        return self.profiles.get(profile_id)

    def upsert(self, profile: LightingProfile) -> None:
        self.profiles[profile.id] = profile

    def delete(self, profile_id: ProfileId) -> None:
        self.profiles.pop(profile_id, None)


LIGHTING_PROFILE_CATALOG = LightingProfileCatalog()
