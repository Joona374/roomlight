TUI_STYLE = """
Screen {
    layout: horizontal;
}
PhysicalView {
    layout: horizontal;
}
#sidebar {
    width: 30;
    background: $panel;
    border-right: solid $accent;
}
#room-view {
    width: 1fr;
    padding: 1;
}

/* NEW RULES FOR THE SPLIT VIEW */
#room-content {
    layout: horizontal;
    height: 1fr;
}
#visualizer-container {
    width: 1fr;
    align: center middle;
}
#controls-container {
    width: 45;
    padding: 1 2;
    border-left: solid $panel;
}
.light-button {
    margin: 1 0;
    width: 100%;
}
.light-row {
    height: auto;
    margin: 1 0;
}
.light-label {
    width: 100%;
}
.light-buttons {
    height: auto;
}
.brightness-btn {
    width: 1fr;
}
/* CRUD Layout rules */
.crud-column {
    width: 1fr;
    height: auto;
    padding: 1 2;
}

.button-row {
    height: auto;
    margin-top: 1;
}

.button-row Button {
    margin-right: 1;
}

#btn_save_disk {
    margin-top: 1;
    width: 100%;
}

/* Custom Row for Light Inputs */
LightInputRow {
    height: auto;
    margin-bottom: 1;
}

.light-name-input {
    width: 1fr;
    margin-right: 1;
}

.btn-remove-light {
    min-width: 5;
    width: 5;
}

/* Ensure the container doesn't force unnecessary height */
#lights_container {
    height: auto;
    margin-bottom: 1;
}

#btn_add_light {
    margin-bottom: 2;
}

.section-header {
    text-style: bold;
    margin-bottom: 1;
}
/* Columns */
#left-config-col {
    width: 40;
    padding: 1 2;
    border-right: tall $primary;
}

#right-config-col {
    width: 1fr;
    padding: 1 2;
}

#profile-crud-view {
    width: 1fr;
    padding: 1 1;
    border-right: tall $primary;
}

#panel-editor-view {
    width: 2fr;
    padding: 1 1;
}

#profile-crud-column {
    width: 1fr;
    padding: 0 1;
}

#profile-meta-actions {
    height: auto;
    margin-top: 1;
}

#profile-meta-actions Button {
    width: 1fr;
}

#panel-editor-content {
    layout: horizontal;
    width: 1fr;
}

#panel-editor-col-left {
    width: 1fr;
    padding: 0 1;
}

#panel-editor-col-right {
    width: 1fr;
    padding: 0 1;
    border-left: tall $surface;
}

#panel-control-save-actions {
    height: auto;
    margin-top: 1;
}

#panel-control-save-actions Button {
    width: 1fr;
}

.hidden {
    display: none;
}

#target-label-list {
    height: 8;
    margin-bottom: 1;
}

#control-list {
    height: 5;
    overflow-y: auto;
    margin-bottom: 1;
}

#target-label-actions {
    height: auto;
    margin-bottom: 1;
}

#target-label-actions Button {
    width: 1fr;
}

#toggle-behavior-actions {
    height: auto;
    margin-top: 1;
    margin-bottom: 1;
}

#toggle-behavior-actions Button {
    width: 1fr;
}

#toggle-behavior-status {
    margin-bottom: 1;
}

#input_set_state {
    margin-top: 1;
}

#right-lights-col {
    width: 1fr;
    padding: 1 2;
}

/* Internal Layouts */
#list-actions {
    height: auto;
    margin-bottom: 1;
}

#list-actions Button {
    width: 1fr;
}

.field-label {
    margin-top: 1;
    text-style: bold;
    color: $accent;
}

.section-header {
    text-style: underline bold;
    margin-bottom: 1;
    width: 100%;
    content-align: center middle;
}

/* Light Row Styling */
LightInputRow {
    height: auto;
    margin-bottom: 0;
}

.light-name-input {
    width: 1fr;
}

#btn_save_memory, #btn_save_disk {
    margin-top: 1;
    width: 100%;
}

#room-profile-assignment-content {
    layout: horizontal;
    width: 1fr;
}

#room-profile-filters-col {
    width: 38;
    padding: 0 1;
    border-right: tall $primary;
}

#room-profile-rooms-col {
    width: 1fr;
    padding: 0 1;
}

#assignment_floor_list,
#assignment_room_type_list,
#assignment_profile_list {
    height: 6;
    margin-bottom: 1;
}

#assignment_room_list {
    height: 1fr;
    margin-bottom: 1;
}

#assignment-actions,
#assignment-apply-actions {
    height: auto;
    margin-bottom: 1;
}

#assignment-actions Button,
#assignment-apply-actions Button {
    width: 1fr;
}
"""
