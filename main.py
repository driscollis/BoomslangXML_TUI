import lxml.etree as ET

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Label, Input, Tree

class DataInput(Input):

    def __init__(self, xml_obj: ET.Element, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.xml_obj = xml_obj

class BoomslangXML(App):

    def __init__(self) -> None:
        super().__init__()
        self.expanded = {}

    def compose(self) -> ComposeResult:
        xml_tree = ET.parse("books.xml")
        xml_root = xml_tree.getroot()
        self.expanded[id(xml_root)] = ''
        yield Horizontal(
            Vertical(
                Tree("No Data Loaded", id="xml_tree"),
                id="left_pane"
            ),
            Vertical(
                Button("Add Node", id="add_node"),
                id="right_pane"
            ),
            id="main_ui_container"
        )

    def on_mount(self) -> None:
        self.load_tree()

    @on(Tree.NodeExpanded)
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        xml_obj = event.node.data
        if id(xml_obj) not in self.expanded and xml_obj is not None:
            for top_level_item in xml_obj.getchildren():
                child = event.node.add_leaf(top_level_item.tag, data=top_level_item)
                if top_level_item.getchildren():
                    child.allow_expand = True
                else:
                    child.allow_expand = False
            self.expanded[id(xml_obj)] = ''

    @on(Tree.NodeSelected)
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        xml_obj = event.node.data
        self.notify(f"{xml_obj} is selected")
        right_pane = self.query_one("#right_pane", Vertical)
        right_pane.remove_children()

        if xml_obj is not None:
            for child in xml_obj.getchildren():
                if child.getchildren():
                    continue
                text = child.text if child.text else ''
                container = Horizontal(
                    Label(child.tag),
                    DataInput(child, text)
                )
                right_pane.mount(container)
            else:
                # XML object has no children, so just show the tag and text
                if getattr(xml_obj, 'tag') and getattr(xml_obj, 'text'):
                    if xml_obj.getchildren() == []:
                        container = Horizontal(
                            Label(xml_obj.tag),
                            DataInput(xml_obj, xml_obj.text)
                        )
                        right_pane.mount(container)

        right_pane.mount(Button("Add Node"))

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        """
        When an XML element changes, update the XML object
        """
        xml_obj = event.input.xml_obj
        # self.notify(f"{xml_obj.text} is changed to new value: {event.input.value}")
        xml_obj.text = event.input.value

    def load_tree(self) -> None:
        tree = self.query_one("#xml_tree", Tree)
        xml_tree = ET.parse("books.xml")
        xml_root = xml_tree.getroot()
        self.expanded[id(xml_root)] = ''

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


if __name__ == "__main__":
    app = BoomslangXML()
    app.run()