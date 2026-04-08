from src.types import RoomType
from src.models.physical.floor import Floor
from src.models.physical.property import Property
from src.models.physical.room import Room


def create_mock_property(n_of_floors: int = 3, rooms_per_floor: int = 20) -> Property:
    hotel = Property("Test Hotel")

    add_mock_floors_to_property(hotel, n_of_floors)

    add_mock_conference_rooms_to_floor(hotel.floors[0], 3)  # Add 2 conference rooms to the first floor

    for floor in hotel.floors:
        add_mock_rooms_to_floor(floor, rooms_per_floor)

    return hotel


def add_mock_floors_to_property(property: Property, n_of_floors: int) -> None:
    for i in range(1, n_of_floors+1):
        floor = Floor(i)
        property.add_floor(floor)


def add_mock_conference_rooms_to_floor(floor: Floor, count: int) -> None:
    for i in range(count):
        room_id = f"CONF-{floor.level}-{i}"
        room = Room(room_id, RoomType.CONFERENCE)
        floor.add_room(room)


def add_mock_rooms_to_floor(floor: Floor, rooms_per_floor: int) -> None:
    for i in range(rooms_per_floor):
        room_type = RoomType.SUITE if i % 5 == 0 else RoomType.NORMAL
        room_id = f"ROOM-{floor.level}-{i}{" (SUITE)" if room_type == RoomType.SUITE else ""}"
        room = Room(room_id, room_type)
        floor.add_room(room)
