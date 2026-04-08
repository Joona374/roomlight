TUI_STYLE = """
Screen {
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
"""
