from src.mock.mock_data import create_mock_property, connect_mock_property_to_system
from src.models.logical.room_light_system import RoomLightSystem
from src.tui.app import RoomLightApp
from src.types.room_type_catalog import RoomTypeCatalog

if __name__ == "__main__":
    # This models and represents the actual physical hardware and infrastructure of the hotel.
    # In the actual real world scenario this layer wouldnt be needed as we would be interacting with the real hardware,
    # in this demo / simulation we need to model the hardware and its interactions to be able to demonstrate the RoomLight system controlling it.
    hotel_data = create_mock_property()

    # This is the actual central control system and the hart of the actual product.
    # It represents the software solution that enables centralized controll of the physical controll panels and lighting units (represented by hotel_data).
    system = RoomLightSystem()

    # This step represents the initial instalation and configuration step required when first installing the RoomLight system to a physical hotel property.
    # In real world this would require physically interacting with the control panels to pair them to the lighting units and the central system.
    # So this is again just a simulation level step.
    connect_mock_property_to_system(hotel_data, system)

    # RoomLightApp is a visual demo representation of the systems behaviour.
    # It attempts to visualize both the actual physical state of the hotel (lighting states and controll panels in different rooms) seen by guests,
    # and the functionality RoomLightSystem offers to the staff of the hotel.
    app = RoomLightApp(property_data=hotel_data, roomlight=system)
    app.run()
