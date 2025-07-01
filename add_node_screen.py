from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Footer, Input


class AddNodeScreen(ModalScreen):
    BINDINGS = [
        ("escape", "esc", "Exit dialog"),
    ]
    CSS_PATH = "add_node_screen.tcss"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "Add New Node"

    def compose(self) -> ComposeResult:
        self.node_name = Input(id="node_name")
        self.node_name.border_title = "Node Name"
        self.node_value = Input(id="node_value")
        self.node_value.border_title = "Node Value"

        yield Vertical(
            Header(),
            self.node_name,
            self.node_value,
            Horizontal(
                Button("Save Node", variant="primary", id="save_node"),
                Button("Cancel", variant="warning", id="cancel_node"),
            ),
            Footer(),
            id="add_node_screen_ui",
        )

    @on(Button.Pressed, "#save_node")
    def on_save(self) -> None:
        self.dismiss((self.node_name.value, self.node_value.value))

    @on(Button.Pressed, "#cancel_node")
    def on_cancel(self) -> None:
        self.dismiss()

    def action_esc(self) -> None:
        """
        Close the dialog when the user presses ESC
        """
        self.dismiss()
