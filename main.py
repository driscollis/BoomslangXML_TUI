from edit_xml_screen import EditXMLScreen

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class BoomslangXML(App):
    BINDINGS = [
        ("ctrl+o", "open", "Open XML File"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.title = "Boomslang XML"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_open(self) -> None:
        self.push_screen(EditXMLScreen("books.xml"))


if __name__ == "__main__":
    app = BoomslangXML()
    app.run()