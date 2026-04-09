from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, Button

class StaffView(Container):

    def __init__(self):
        super().__init__()

    def compose(self):
        yield Horizontal(
            Vertical(
                Label("Staff Actions"), 
                Button("Turn off floor"), 
                Button("Emergency mode"), 
                id="sidebar"
            ), 
            Container(
                Label("Staff dashboard"), 
                id="main-content"
            )
        )
