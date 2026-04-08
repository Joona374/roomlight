from enum import Enum, IntEnum, auto

# The lighting units installed to rooms have have a 3-step brightness controll
# This is used to both model and controll that
class Brightness(IntEnum):
    LOW = 20
    MEDIUM = 50
    HIGH = 100

# Hotels might have different room types that need different lightning templates
class RoomType(Enum):
    NORMAL = auto()
    SUITE = auto()


# A centralized way to store 
ROOM_CONFIGURATIONS = {
    RoomType.NORMAL: {
        "light_count": 4, 
        "labels": ["Entry", "Main", "Bedside", "Bathroom"]
        }, 
    RoomType.SUITE: {
        "light_count": 5, 
        "labels": ["Entry", "Living", "Bedroom", "Bathroom", "Desk"]
        }
    }
