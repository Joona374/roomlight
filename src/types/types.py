from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from typing import NewType


# While the percentages here are slightly arbitrary, the idea is that the system could in future
# also support continuous brigtness values with slider inputs.
class Brightness(IntEnum):
    OFF = 0
    LOW = 20
    MEDIUM = 50
    HIGH = 100

# Different room categories need different default lighting layouts.
# class RoomType(Enum):
#     NORMAL = auto()
#     SUITE = auto()
#     CONFERENCE = auto()


# While this isnt interactively accessible in the demo, being able to adjust these
# values is also part of the "configure once" ideology as  changing a template
# here affects every new room of that type. (REQ-03)
# ROOM_CONFIGURATIONS = {
#     RoomType.NORMAL: {"light_count": 4, "labels": ["Entry", "Main", "Bedside", "Bathroom"]},
#     RoomType.SUITE: {"light_count": 5, "labels": ["Entry", "Bedroom", "Bathroom", "Living", "Desk"]},
#     RoomType.CONFERENCE: {
#         "light_count": 7,
#         "labels": ["Entry", "Bathroom", "Rear", "Center", "Left", "Right", "Stage"],
#     },
# }


RoomTypeId = NewType("RoomTypeId", str)

@dataclass(frozen=True)
class RoomTypeTemplate:
    id: RoomTypeId  # e.g. "standard", "suite", "conference"
    display_name: str  # e.g. "Standard"
    light_count: int  # this is needed to be able to create new rooms of this type
    light_labels: list[str]  # replaces light_count + labels mismatch risk
