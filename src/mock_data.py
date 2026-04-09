from src.models.logical.logical_floor import LogicalFloor
from src.models.logical.logical_room import LogicalRoom
from src.models.logical.room_light_system import RoomLightSystem
from src.models.physical.light_unit import LightUnit
from src.models.physical.room_control_panel import RoomControlPanel
from src.types import ROOM_CONFIGURATIONS, RoomType
from src.models.physical.floor import Floor
from src.models.physical.property import Property
from src.models.physical.room import Room


def create_mock_property(n_of_floors: int = 3, rooms_per_floor: int = 20) -> Property:
    """Build a predictable demo hotel so the TUI always has realistic data to show."""
    hotel = Property("Test Hotel")

    add_mock_floors_to_property(hotel, n_of_floors)

    add_mock_conference_rooms_to_floor(hotel.floors[0], 3)  # 0 is the lobby floor with conference rooms

    for floor in hotel.floors[1:]:  # Skip the lobby floor with conference rooms
        add_mock_rooms_to_floor(floor, rooms_per_floor)

    return hotel


def add_mock_floors_to_property(property: Property, n_of_floors: int) -> None:
    for i in range(0, n_of_floors + 1):
        floor = Floor(i)
        property.add_floor(floor)


def add_mock_conference_rooms_to_floor(floor: Floor, count: int) -> None:
    for i in range(1, count + 1):
        room_id = f"CONF-{i}"
        room = build_mock_room(room_id, RoomType.CONFERENCE, floor.level, i)
        floor.add_room(room)


def add_mock_rooms_to_floor(floor: Floor, rooms_per_floor: int) -> None:
    for i in range(1, rooms_per_floor + 1):
        # Every fifth room is a suite so we can showcase multiple room templates (REQ-03)
        room_type = RoomType.SUITE if i % 5 == 0 else RoomType.NORMAL
        room_id = f"ROOM-{floor.level}-{i}{' (SUITE)' if room_type == RoomType.SUITE else ''}"

        room = build_mock_room(room_id, room_type, floor.level, i)
        floor.add_room(room)


def build_mock_room(id: str, type: RoomType, floor: int, room_number: int) -> Room:
    # 1. Pre build the correct number of light unites
    light_units_in_room_type = ROOM_CONFIGURATIONS[type]["light_count"]
    light_units = [LightUnit() for _ in range(light_units_in_room_type)]

    # 2. Build the control panel
    panel = RoomControlPanel()

    # 3. Build the room and attach the panel to it, then connect the lights to the panel.
    room = Room(
        id=id,
        type=type,
        floor=floor,
        room_number=room_number,
        control_panel=panel,
        light_units=light_units,
    )
    panel.attach_to_room(room)

    # 4. Connect the physical light units to the physical panel using the correct labels for this room type.
    for i, unit in enumerate(light_units):
        label = ROOM_CONFIGURATIONS[type]["labels"][i]
        panel.connect_light_unit(label, unit)

    return room


def connect_mock_property_to_system(property: Property, system: RoomLightSystem) -> None:
    """
    Helper function to connect all panels in the demo property to the system.
    This basically simulates a technician first registering all the floors and rooms in the property,
    and then going around the hotel and registering each panel to the central system after installation.
    In a real world scenario this would be a one-time setup step that happens after the physical installation of the panels.
    """

    for floor in property.floors:
        logical_floor = LogicalFloor(floor.level)
        system.register_floor(logical_floor)

        for room in floor.rooms:
            logical_room = LogicalRoom(room.id, room.type, room.floor, room.number)
            logical_floor.add_room(logical_room)

            room.control_panel.connect_to_roomlight_system(system)
