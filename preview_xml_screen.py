
from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, TextArea


class PreviewXMLScreen(ModalScreen):
    CSS_PATH = "preview_xml_screen.tcss"

    def __init__(self, xml_file_path: str, *args: tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.xml_file_path = xml_file_path
        self.title = "Preview XML"

    def compose(self) -> ComposeResult:
        with open(self.xml_file_path) as xml_file:
            xml = xml_file.read()
        text_area = TextArea(xml)
        text_area.language = "xml"
        yield Header()
        yield Vertical(
            text_area,
            Center(
                Button("Exit Preview", id="exit_preview", variant="primary")
            ),
            id="exit_preview_ui"
        )

    @on(Button.Pressed, "#exit_preview")
    def on_exit_preview(self, event: Button.Pressed) -> None:
        self.dismiss()
