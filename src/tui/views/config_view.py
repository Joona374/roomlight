from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, Button


class ConfigView(Container):

    def __init__(self):
        super().__init__()

    def compose(self):
        # Layout the tab horizontally: sidebar + main content
        yield Horizontal(
            Vertical(
                Label("Config Sections"), 
                Button("Room Types"), 
                Button("Lighting Profiles"), 
                id="sidebar"
            ), 
            Container(
                Label("Select something to configure"), 
                id="main-content"
            )
        )


