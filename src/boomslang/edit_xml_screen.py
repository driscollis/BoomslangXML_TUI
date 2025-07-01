import lxml.etree as ET
import tempfile
from pathlib import Path

from .add_node_screen import AddNodeScreen
from .preview_xml_screen import PreviewXMLScreen

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Footer, Header, Input, Tree
from textual.widgets._tree import TreeNode


class DataInput(Input):
    """
    Create a variant of the Input widget that stores data
    """

    def __init__(self, xml_obj: ET.Element, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.xml_obj = xml_obj


class EditXMLScreen(ModalScreen):
    BINDINGS = [
        ("ctrl+s", "save", "Save"),
        ("ctrl+a", "add_node", "Add Node"),
        ("p", "preview", "Preview"),
        ("escape", "esc", "Exit dialog"),
    ]
    CSS_PATH = "edit_xml_screens.tcss"

    def __init__(self, xml_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xml_tree = ET.parse(xml_path)
        self.expanded = {}
        self.selected_tree_node: None | TreeNode = None

    def compose(self) -> ComposeResult:
        xml_root = self.xml_tree.getroot()
        self.expanded[id(xml_root)] = ""
        yield Header()
        yield Horizontal(
            Vertical(Tree("No Data Loaded", id="xml_tree"), id="left_pane"),
            VerticalScroll(id="right_pane"),
            id="main_ui_container",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.load_tree()

    @on(Tree.NodeExpanded)
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """
        When a tree node is expanded, parse the newly shown leaves and make
        them expandable, if necessary.
        """
        xml_obj = event.node.data
        if id(xml_obj) not in self.expanded and xml_obj is not None:
            for top_level_item in xml_obj.getchildren():
                child = event.node.add_leaf(top_level_item.tag, data=top_level_item)
                if top_level_item.getchildren():
                    child.allow_expand = True
                else:
                    child.allow_expand = False
            self.expanded[id(xml_obj)] = ""

    @on(Tree.NodeSelected)
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """
        When a node in the tree control is selected, update the right pane to show
        the data in the XML, if any
        """
        xml_obj = event.node.data
        right_pane = self.query_one("#right_pane", VerticalScroll)
        right_pane.remove_children()
        self.selected_tree_node = event.node

        if xml_obj is not None:
            for child in xml_obj.getchildren():
                if child.getchildren():
                    continue
                text = child.text if child.text else ""
                data_input = DataInput(child, text)
                data_input.border_title = child.tag
                container = Horizontal(data_input)
                right_pane.mount(container)
            else:
                # XML object has no children, so just show the tag and text
                if getattr(xml_obj, "tag") and getattr(xml_obj, "text"):
                    if xml_obj.getchildren() == []:
                        data_input = DataInput(xml_obj, xml_obj.text)
                        data_input.border_title = xml_obj.tag
                        container = Horizontal(data_input)
                        right_pane.mount(container)

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        """
        When an XML element changes, update the XML object
        """
        xml_obj = event.input.xml_obj
        # self.notify(f"{xml_obj.text} is changed to new value: {event.input.value}")
        xml_obj.text = event.input.value

    def action_esc(self) -> None:
        """
        Close the dialog when the user presses ESC
        """
        self.dismiss()

    def action_add_node(self) -> None:
        """
        Add another node to the XML tree and the UI
        """

        # Show dialog and use callback to update XML and UI
        def add_node(result: tuple[str, str] | None) -> None:
            if result is not None:
                node_name, node_value = result
                self.update_xml_tree(node_name, node_value)

        self.app.push_screen(AddNodeScreen(), add_node)

    def action_preview(self) -> None:
        temp_directory = Path(tempfile.gettempdir())
        xml_path = temp_directory / "temp.xml"
        self.xml_tree.write(xml_path)
        self.app.push_screen(PreviewXMLScreen(xml_path))

    def action_save(self) -> None:
        self.xml_tree.write(r"C:\Temp\books.xml")
        self.notify("Saved!")

    def load_tree(self) -> None:
        """
        Load the XML tree UI with data parsed from the XML file
        """
        tree = self.query_one("#xml_tree", Tree)
        xml_root = self.xml_tree.getroot()
        self.expanded[id(xml_root)] = ""

        tree.reset(xml_root.tag)
        tree.root.expand()

        # If the root has children, add them
        if xml_root.getchildren():
            for top_level_item in xml_root.getchildren():
                child = tree.root.add(top_level_item.tag, data=top_level_item)
                if top_level_item.getchildren():
                    child.allow_expand = True
                else:
                    child.allow_expand = False

    def update_tree_nodes(self, node_name: str, node: ET.SubElement) -> None:
        """
        When adding a new node, update the UI Tree element to reflect the new element added
        """
        child = self.selected_tree_node.add(node_name, data=node)
        child.allow_expand = False

    def update_xml_tree(self, node_name: str, node_value: str) -> None:
        """
        When adding a new node, update the XML object with the new element
        """
        element = ET.SubElement(self.selected_tree_node.data, node_name)
        element.text = node_value
        self.update_tree_nodes(node_name, element)
