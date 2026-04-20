from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Label

from src.models.logical.room_light_system import RoomLightSystem
from src.tui.views.config_view.panel_editor_view import PanelEditorView
from src.tui.views.config_view.profile_crud_view import ProfileCrudView
from src.types.types import LightingProfile


class ProfilesView(Vertical):
    def __init__(self, roomlight: RoomLightSystem, **kwargs):
        super().__init__(**kwargs)
        self.roomlight = roomlight

    def compose(self) -> ComposeResult:
        yield Label("Lighting Profiles", id="title")

        with Horizontal():
            yield ProfileCrudView(
                id="profile-crud-view",
                roomlight=self.roomlight,
                on_profile_selected=self._on_profile_selected,
            )
            yield PanelEditorView(id="panel-editor-view")

    def _on_profile_selected(self, profile: LightingProfile | None) -> None:
        self.query_one(PanelEditorView).set_profile(profile)
