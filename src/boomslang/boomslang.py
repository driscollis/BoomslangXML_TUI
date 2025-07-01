from pathlib import Path

from edit_xml_screen import EditXMLScreen
from file_browser_screen import FileBrowser

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Header, Footer, OptionList


class BoomslangXML(App):
    BINDINGS = [
        ("ctrl+o", "open", "Open XML File"),
    ]
    CSS_PATH = "main.tcss"

    def __init__(self) -> None:
        super().__init__()
        self.title = "Boomslang XML"
        self.recent_files_path = Path(__file__).absolute().parent / "recent_files.txt"
        self.app_selected_file: Path | None = None
        self.current_recent_file: Path | None = None

    def compose(self) -> ComposeResult:
        self.recent_files = OptionList("", id="recent_files")
        self.recent_files.border_title = "Recent Files"
        yield Header()
        yield self.recent_files
        yield Vertical(
            Horizontal(
                Button("Open XML File", id="open_xml_file", variant="primary"),
                Button("Open Recent", id="open_recent_file", variant="warning"),
                id="button_row",
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        self.update_recent_files_ui()

    def action_open(self) -> None:
        self.push_screen(FileBrowser())

    def on_file_browser_selected(self, message: FileBrowser.Selected) -> None:
        path = message.path
        if path.suffix.lower() == ".xml":
            self.update_recent_files_on_disk(path)
            self.push_screen(EditXMLScreen(path))
        else:
            self.notify("Please choose an XML File!", severity="error", title="Error")

    @on(Button.Pressed, "#open_xml_file")
    def on_open_xml_file(self) -> None:
        self.push_screen(FileBrowser())

    @on(Button.Pressed, "#open_recent_file")
    def on_open_recent_file(self) -> None:
        if self.current_recent_file is not None and self.current_recent_file.exists():
            self.push_screen(EditXMLScreen(self.current_recent_file))

    @on(OptionList.OptionSelected, "#recent_files")
    def on_recent_files_selected(self, event: OptionList.OptionSelected) -> None:
        self.current_recent_file = Path(event.option.prompt)

    def update_recent_files_ui(self) -> None:
        if self.recent_files_path.exists():
            self.recent_files.clear_options()
            files = self.recent_files_path.read_text()
            for file in files.split("\n"):
                self.recent_files.add_option(file.strip())

    def update_recent_files_on_disk(self, path: Path) -> None:
        if path.exists() and self.recent_files_path.exists():
            recent_files = self.recent_files_path.read_text()
            if str(path) in recent_files:
                return

            with open(self.recent_files_path, mode="a") as f:
                f.write(str(path) + "\n")

            self.update_recent_files_ui()
        elif not self.recent_files_path.exists():
            with open(self.recent_files_path, mode="a") as f:
                f.write(str(path) + "\n")


if __name__ == "__main__":
    app = BoomslangXML()
    app.run()
