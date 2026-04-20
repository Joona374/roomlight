from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import NewType, TypeAlias


# These are just used for better type safety and readability
RoomTypeId = NewType("RoomTypeId", str)
ProfileId = NewType("ProfileId", str)
ControlId = NewType("ControlId", str)


# While the percentages here are slightly arbitrary, the idea is that the system could in future
# also support continuous brigtness values with slider inputs.
class Brightness(IntEnum):
    OFF = 0
    LOW = 20
    MEDIUM = 50
    HIGH = 100


class TargetMode(Enum):
    ALL = "all"
    LABELS = "labels"


class ControlKind(Enum):
    TOGGLE = "toggle"
    ADJUST = "adjust"


class ToggleBehavior(Enum):
    SET = "set"
    TOGGLE = "toggle"


@dataclass(frozen=True)
class RoomTypeTemplate:  # (REQ-03)
    id: RoomTypeId  # e.g. "standard", "suite", "conference"
    display_name: str  # e.g. "Standard"
    light_count: int  # this is needed to be able to create new rooms of this type
    light_labels: list[str]  # replaces light_count + labels mismatch risk


@dataclass(frozen=True)
class TargetSelector:
    # "all" means every light in the room
    # "labels" means only named lights like ["Living", "Desk"]
    mode: TargetMode
    labels: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ToggleControl:
    id: ControlId
    kind: ControlKind = ControlKind.TOGGLE
    label: str = ""
    target: TargetSelector = field(default_factory=lambda: TargetSelector(mode=TargetMode.ALL))
    behavior: ToggleBehavior = ToggleBehavior.SET
    set_state: Brightness = Brightness.OFF
    on_state: Brightness = Brightness.LOW
    off_state: Brightness = Brightness.OFF

    @classmethod
    def from_dict(cls, data: dict) -> "ToggleControl":
        return cls(
            id=ControlId(data["id"]),
            label=data.get("label", ""),
            target=TargetSelector(
                mode=TargetMode(data["target"]["mode"]),
                labels=data["target"].get("labels", []),
            ),
            behavior=ToggleBehavior(data.get("behavior", ToggleBehavior.SET.value)),
            set_state=Brightness(data.get("set_state", 0)),
            on_state=Brightness(data.get("on_state", 20)),
            off_state=Brightness(data.get("off_state", 0)),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "kind": self.kind.value,
            "label": self.label,
            "target": {"mode": self.target.mode.value, "labels": self.target.labels},
            "behavior": self.behavior.value,
            "set_state": int(self.set_state),
            "on_state": int(self.on_state),
            "off_state": int(self.off_state),
        }


@dataclass(frozen=True)
class AdjustControl:
    id: ControlId
    kind: ControlKind = ControlKind.ADJUST
    label: str = ""
    target: TargetSelector = field(default_factory=lambda: TargetSelector(mode=TargetMode.ALL))
    minus_text: str = "-"
    plus_text: str = "+"

    @classmethod
    def from_dict(cls, data: dict) -> "AdjustControl":
        return cls(
            id=ControlId(data["id"]),
            label=data.get("label", ""),
            target=TargetSelector(
                mode=TargetMode(data["target"]["mode"]),
                labels=data["target"].get("labels", []),
            ),
            minus_text=data.get("minus_text", "-"),
            plus_text=data.get("plus_text", "+"),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "kind": self.kind.value,
            "label": self.label,
            "target": {"mode": self.target.mode.value, "labels": self.target.labels},
            "minus_text": self.minus_text,
            "plus_text": self.plus_text,
        }


# Needs to be defined down here so that ToggleControl and AdjustControl are already defined
PanelControl: TypeAlias = ToggleControl | AdjustControl


@dataclass(frozen=True)
class LightingProfile:
    id: ProfileId
    room_type_id: RoomTypeId
    name: str
    controls: list[PanelControl]

    @classmethod
    def from_dict(cls, data: dict, controls: list[PanelControl]) -> "LightingProfile":
        return cls(
            id=ProfileId(data["id"]),
            room_type_id=RoomTypeId(data["room_type_id"]),
            name=data["name"],
            controls=controls,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "room_type_id": str(self.room_type_id),
            "name": self.name,
            "controls": [control.to_dict() for control in self.controls],
        }
