from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Label, OptionList
from textual.widgets.option_list import Option

from src.types.lightning_profile_catalog import LIGHTING_PROFILE_CATALOG
from src.types.room_type_catalog import ROOM_TYPE_CATALOG
from src.types.types import (
    AdjustControl,
    Brightness,
    ControlId,
    ControlKind,
    LightingProfile,
    PanelControl,
    TargetMode,
    TargetSelector,
    ToggleBehavior,
    ToggleControl,
)


class PanelEditorView(Vertical):
    """Editor panel for managing control buttons inside a selected profile."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_profile: LightingProfile | None = None
        self.controls: list[PanelControl] = []
        self.selected_control_id: ControlId | None = None

        self.current_kind: ControlKind = ControlKind.TOGGLE
        self.current_target_mode: TargetMode = TargetMode.ALL
        self.current_toggle_behavior: ToggleBehavior = ToggleBehavior.SET
        self.available_target_labels: list[str] = []
        self.selected_target_labels: set[str] = set()

    def compose(self) -> ComposeResult:
        with Horizontal(id="panel-editor-content"):
            with Vertical(id="panel-editor-col-left"):
                yield Label("", id="panel-editor-room-labels")

                yield Label("Buttons in Panel", classes="section-header")
                yield OptionList(id="control-list")

                with Horizontal(id="list-actions"):
                    yield Button("New Button", id="btn_new_control", variant="success")
                    yield Button("Delete Button", id="btn_delete_control", variant="error")

                yield Label("Button Label", classes="field-label")
                yield Input(placeholder="e.g. All Off", id="input_control_label")

                yield Label("Control Type", classes="field-label")
                with Horizontal(id="control-kind-actions"):
                    yield Button("Toggle", id="btn_kind_toggle")
                    yield Button("Adjuster", id="btn_kind_adjust")
                yield Label("Current: toggle", id="control-kind-status")

                yield Label("Target", classes="field-label")
                with Horizontal(id="target-mode-actions"):
                    yield Button("All Lights", id="btn_target_all")
                    yield Button("Specific Labels", id="btn_target_labels")
                yield Label("Current: all", id="target-mode-status")
                yield Label("Click labels to select one or many:")
                yield OptionList(id="target-label-list")
                with Horizontal(id="target-label-actions"):
                    yield Button("Select All", id="btn_target_select_all")
                    yield Button("Clear", id="btn_target_clear")

            with Vertical(id="panel-editor-col-right"):
                with Vertical(id="toggle-settings-group"):
                    yield Label("Toggle Behavior", classes="field-label")
                    with Horizontal(id="toggle-behavior-actions"):
                        yield Button("Set State", id="btn_behavior_set")
                        yield Button("Toggle", id="btn_behavior_toggle")
                    yield Label("Current: set", id="toggle-behavior-status")

                    yield Label("Toggle States (OFF/LOW/MEDIUM/HIGH or 0/20/50/100)", classes="field-label")
                    yield Input(value="OFF", id="input_set_state", placeholder="Set-state when behavior = set")
                    yield Input(value="LOW", id="input_on_state", placeholder="On-state when behavior = toggle")
                    yield Input(value="OFF", id="input_off_state", placeholder="Off-state when behavior = toggle")

                with Vertical(id="adjust-settings-group"):
                    yield Label("Adjuster Symbols", classes="field-label")
                    yield Input(value="-", id="input_minus_text", placeholder="Minus button label")
                    yield Input(value="+", id="input_plus_text", placeholder="Plus button label")

                with Horizontal(id="panel-control-save-actions"):
                    yield Button("Update Button\n", id="btn_save_control", variant="primary")
                    yield Button("Save Profile Controls", id="btn_save_controls_memory", variant="primary")
                    yield Button("Save Controls to JSON", id="btn_save_controls_disk", variant="success")

    def on_mount(self) -> None:
        self._refresh_controls_list()
        self._refresh_target_label_list()
        self._refresh_mode_labels()
        self._refresh_control_type_visibility()

    def set_profile(self, profile: LightingProfile | None) -> None:
        self.selected_profile = profile
        self.controls = list(profile.controls) if profile else []
        self.selected_control_id = None

        room_labels = self.query_one("#panel-editor-room-labels", Label)

        if profile is None:
            self.available_target_labels = []
            self.selected_target_labels.clear()
            room_labels.update("Select a profile to edit panel controls.")
            self._refresh_controls_list()
            self._refresh_target_label_list()
            self._clear_control_form()
            return

        room_type = ROOM_TYPE_CATALOG.get_by_id(profile.room_type_id)
        if room_type:
            self.available_target_labels = list(room_type.light_labels)
            room_labels.update(
                f"Editing: {profile.name} | Room type: {profile.room_type_id} | "
                + "Available labels: "
                + ", ".join(room_type.light_labels)
            )
        else:
            self.available_target_labels = []
            room_labels.update(f"Editing: {profile.name} | Room type labels not found.")

        self._refresh_controls_list()
        self._refresh_target_label_list()
        self._clear_control_form()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option_list_id = event.option_list.id
        option_id = event.option.id

        if not option_id:
            return

        if option_list_id == "target-label-list":
            self._toggle_target_label(option_id)
            return

        if option_list_id != "control-list":
            return

        control = self._get_control_by_id(ControlId(option_id))
        if control is None:
            self.notify("Control not found.", severity="error")
            return

        self.selected_control_id = control.id
        self._load_control_into_form(control)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "btn_kind_toggle":
            self.current_kind = ControlKind.TOGGLE
            self._refresh_mode_labels()
            return

        if button_id == "btn_kind_adjust":
            self.current_kind = ControlKind.ADJUST
            self._refresh_mode_labels()
            return

        if button_id == "btn_target_all":
            self.current_target_mode = TargetMode.ALL
            self._refresh_mode_labels()
            return

        if button_id == "btn_target_labels":
            self.current_target_mode = TargetMode.LABELS
            self._refresh_mode_labels()
            return

        if button_id == "btn_target_select_all":
            self.selected_target_labels = set(self.available_target_labels)
            self._refresh_target_label_list()
            return

        if button_id == "btn_target_clear":
            self.selected_target_labels.clear()
            self._refresh_target_label_list()
            return

        if button_id == "btn_behavior_set":
            self.current_toggle_behavior = ToggleBehavior.SET
            self._refresh_mode_labels()
            return

        if button_id == "btn_behavior_toggle":
            self.current_toggle_behavior = ToggleBehavior.TOGGLE
            self._refresh_mode_labels()
            return

        if button_id == "btn_new_control":
            self.selected_control_id = None
            self._clear_control_form()
            self.notify("New button draft ready.")
            return

        if button_id == "btn_delete_control":
            self._delete_selected_control()
            return

        if button_id == "btn_save_control":
            self._save_control_to_draft()
            return

        if button_id == "btn_save_controls_memory":
            self._save_controls_to_profile_memory()
            return

        if button_id == "btn_save_controls_disk":
            self._save_controls_to_profile_memory()
            LIGHTING_PROFILE_CATALOG.save()
            self.notify("Profile controls saved to JSON.")

    def _refresh_mode_labels(self) -> None:
        self.query_one("#control-kind-status", Label).update(f"Current: {self.current_kind.value}")
        self.query_one("#target-mode-status", Label).update(f"Current: {self.current_target_mode.value}")
        self.query_one("#toggle-behavior-status", Label).update(f"Current: {self.current_toggle_behavior.value}")
        self._refresh_control_type_visibility()

    def _refresh_control_type_visibility(self) -> None:
        toggle_group = self.query_one("#toggle-settings-group", Vertical)
        adjust_group = self.query_one("#adjust-settings-group", Vertical)

        if self.current_kind == ControlKind.TOGGLE:
            toggle_group.remove_class("hidden")
            adjust_group.add_class("hidden")
        else:
            toggle_group.add_class("hidden")
            adjust_group.remove_class("hidden")

    def _refresh_controls_list(self) -> None:
        control_list = self.query_one("#control-list", OptionList)
        control_list.clear_options()

        for control in self.controls:
            target = "all" if control.target.mode == TargetMode.ALL else ", ".join(control.target.labels)
            label = f"{control.label} [{control.kind.value}] -> {target}"
            control_list.add_option(Option(label, id=str(control.id)))

    def _refresh_target_label_list(self) -> None:
        target_list = self.query_one("#target-label-list", OptionList)
        target_list.clear_options()

        for label in self.available_target_labels:
            marker = "[x]" if label in self.selected_target_labels else "[ ]"
            target_list.add_option(Option(f"{marker} {label}", id=label))

    def _toggle_target_label(self, label: str) -> None:
        if label in self.selected_target_labels:
            self.selected_target_labels.remove(label)
        else:
            self.selected_target_labels.add(label)
        self._refresh_target_label_list()

    def _clear_control_form(self) -> None:
        self.query_one("#input_control_label", Input).value = ""
        self.query_one("#input_set_state", Input).value = "OFF"
        self.query_one("#input_on_state", Input).value = "LOW"
        self.query_one("#input_off_state", Input).value = "OFF"
        self.query_one("#input_minus_text", Input).value = "-"
        self.query_one("#input_plus_text", Input).value = "+"
        self.selected_target_labels.clear()
        self._refresh_target_label_list()

        self.current_kind = ControlKind.TOGGLE
        self.current_target_mode = TargetMode.ALL
        self.current_toggle_behavior = ToggleBehavior.SET
        self._refresh_mode_labels()

    def _load_control_into_form(self, control: PanelControl) -> None:
        self.query_one("#input_control_label", Input).value = control.label

        self.current_kind = control.kind
        self.current_target_mode = control.target.mode

        if control.target.mode == TargetMode.LABELS:
            self.selected_target_labels = set(control.target.labels)
        else:
            self.selected_target_labels.clear()
        self._refresh_target_label_list()

        if isinstance(control, ToggleControl):
            self.current_toggle_behavior = control.behavior
            self.query_one("#input_set_state", Input).value = control.set_state.name
            self.query_one("#input_on_state", Input).value = control.on_state.name
            self.query_one("#input_off_state", Input).value = control.off_state.name
        elif isinstance(control, AdjustControl):
            self.query_one("#input_minus_text", Input).value = control.minus_text
            self.query_one("#input_plus_text", Input).value = control.plus_text

        self._refresh_mode_labels()

    def _parse_brightness(self, raw: str, default: Brightness) -> Brightness:
        value = raw.strip().upper()
        if not value:
            return default

        if value.isdigit():
            return Brightness(int(value))

        return Brightness[value]

    def _build_control_id(self, label: str) -> ControlId:
        base = label.strip().lower().replace(" ", "-")
        if not base:
            base = "button"

        existing = {str(control.id) for control in self.controls}
        if self.selected_control_id:
            existing.discard(str(self.selected_control_id))

        candidate = base
        suffix = 2
        while candidate in existing:
            candidate = f"{base}-{suffix}"
            suffix += 1

        return ControlId(candidate)

    def _build_control_from_form(self) -> PanelControl:
        label = self.query_one("#input_control_label", Input).value.strip()
        if not label:
            raise ValueError("Button label is required.")

        target_labels = [label for label in self.available_target_labels if label in self.selected_target_labels]
        if self.current_target_mode == TargetMode.LABELS and not target_labels:
            raise ValueError("Add at least one target label for specific-label mode.")

        control_id = self.selected_control_id if self.selected_control_id else self._build_control_id(label)
        target = TargetSelector(
            mode=self.current_target_mode,
            labels=target_labels if self.current_target_mode == TargetMode.LABELS else [],
        )

        if self.current_kind == ControlKind.TOGGLE:
            set_state = self._parse_brightness(self.query_one("#input_set_state", Input).value, Brightness.OFF)
            on_state = self._parse_brightness(self.query_one("#input_on_state", Input).value, Brightness.LOW)
            off_state = self._parse_brightness(self.query_one("#input_off_state", Input).value, Brightness.OFF)

            return ToggleControl(
                id=control_id,
                label=label,
                target=target,
                behavior=self.current_toggle_behavior,
                set_state=set_state,
                on_state=on_state,
                off_state=off_state,
            )

        minus_text = self.query_one("#input_minus_text", Input).value.strip() or "-"
        plus_text = self.query_one("#input_plus_text", Input).value.strip() or "+"

        return AdjustControl(
            id=control_id,
            label=label,
            target=target,
            minus_text=minus_text,
            plus_text=plus_text,
        )

    def _get_control_by_id(self, control_id: ControlId) -> PanelControl | None:
        for control in self.controls:
            if control.id == control_id:
                return control
        return None

    def _save_control_to_draft(self) -> None:
        if self.selected_profile is None:
            self.notify("Select a profile first.", severity="warning")
            return

        try:
            control = self._build_control_from_form()
        except (KeyError, ValueError) as exc:
            self.notify(str(exc), severity="error")
            return

        replaced = False
        for i, existing in enumerate(self.controls):
            if existing.id == control.id:
                self.controls[i] = control
                replaced = True
                break

        if not replaced:
            self.controls.append(control)

        self.selected_control_id = control.id
        self._refresh_controls_list()
        self.notify(f"Button '{control.label}' updated in editor draft.")

    def _delete_selected_control(self) -> None:
        if self.selected_control_id is None:
            self.notify("No button selected to delete.", severity="warning")
            return

        self.controls = [control for control in self.controls if control.id != self.selected_control_id]
        self.selected_control_id = None
        self._refresh_controls_list()
        self._clear_control_form()
        self.notify("Button deleted from editor draft.")

    def _save_controls_to_profile_memory(self) -> None:
        if self.selected_profile is None:
            self.notify("Select a profile first.", severity="warning")
            return

        updated_profile = LightingProfile(
            id=self.selected_profile.id,
            room_type_id=self.selected_profile.room_type_id,
            name=self.selected_profile.name,
            controls=list(self.controls),
        )

        LIGHTING_PROFILE_CATALOG.upsert(updated_profile)
        self.selected_profile = updated_profile
        self.notify("Profile controls updated in memory.")
