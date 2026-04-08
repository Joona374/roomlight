from src.mock_data import create_mock_property
from src.tui.app import RoomLightApp

if __name__ == "__main__":
    # Create the data first
    hotel_data = create_mock_property()

    # Inject it into the TUI
    app = RoomLightApp(property_data=hotel_data)
    app.run()
