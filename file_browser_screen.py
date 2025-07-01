from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Grid, Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, DirectoryTree, Footer, Label, Header


class WarningScreen(Screen):
    """
    Creates a pop-up Screen that displays a warning message to the user
    """

    def __init__(self, warning_message: str) -> None:
        super().__init__()
        self.warning_message = warning_message

    def compose(self) -> ComposeResult:
        """
        Create the UI in the Warning Screen
        """
        yield Grid(
            Label(self.warning_message, id="warning_msg"),
            Button("OK", variant="primary", id="ok_warning"),
            id="warning_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler for when the OK button - dismisses the screen
        """
        self.dismiss()
        event.stop()


class FileBrowser(Screen):
    BINDINGS = [
        ("escape", "esc", "Exit dialog"),
    ]

    CSS_PATH = "file_browser_screen.tcss"

    class Selected(Message):
        """
        File selected message
        """

        def __init__(self, path: Path) -> None:
            self.path = path
            super().__init__()

    def __init__(self) -> None:
        super().__init__()
        self.selected_file = Path("")
        self.title = "Load XML Files"

    def compose(self) -> ComposeResult:
        yield Vertical(
            Header(),
            DirectoryTree("/"),
            Center(
                Button("Load File", variant="primary", id="load_file"),
            ),
            id="file_browser_dialog",
        )

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """
        Called when the FileSelected Message is emitted from the DirectoryTree
        """
        self.selected_file = event.path

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler for when the load file button is pressed
        """
        event.stop()

        if self.selected_file.suffix.lower() != ".xml" and self.selected_file.is_file():
            self.app.push_screen(WarningScreen("ERROR: You must choose a XML file!"))
            return

        self.post_message(self.Selected(self.selected_file))
        self.dismiss()

    def action_esc(self) -> None:
        """
        Close the dialog when the user presses ESC
        """
        self.dismiss()
