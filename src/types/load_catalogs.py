from src.types.lightning_profile_catalog import LIGHTING_PROFILE_CATALOG
from src.types.room_profile_assignment_catalog import ROOM_PROFILE_ASSIGNMENT_CATALOG
from src.types.room_type_catalog import ROOM_TYPE_CATALOG

# Helper used to load all the catalogs from disk at the start of the program.
def load_catalogs() -> None:
    ROOM_TYPE_CATALOG.load()
    LIGHTING_PROFILE_CATALOG.load()
    ROOM_PROFILE_ASSIGNMENT_CATALOG.load()