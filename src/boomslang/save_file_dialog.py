from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, DirectoryTree, Footer, Header, Input, Label


class SaveFileDialog(Screen):

    CSS_PATH = "save_file_dialog.tcss"

    def __init__(self) -> None:
        super().__init__()
        self.title = "Save File"
        self.root = "/"

    def compose(self) -> ComposeResult:
        yield Vertical(
            Header(),
            Label(f"Folder name: {self.root}", id="folder"),
            DirectoryTree("/"),
            Input(placeholder="filename.txt", id="filename"),
            Button("Save File", variant="primary", id="save_file"),
            id="save_dialog",
        )

    def on_mount(self) -> None:
        """
        Focus the input widget so the user can name the file
        """
        self.query_one("#filename").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler for when the load file button is pressed
        """
        event.stop()
        filename = self.query_one("#filename").value
        full_path = Path(self.root) / filename
        self.dismiss(f"{full_path}")

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selection(self, event: DirectoryTree.DirectorySelected) -> None:
        """
        Called when the DirectorySelected message is emitted from the DirectoryTree
        """
        self.root = event.path
        self.query_one("#folder").update(f"Folder name: {event.path}")