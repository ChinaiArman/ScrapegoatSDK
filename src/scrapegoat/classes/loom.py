from textual.app import App
from textual.widgets import Header, Footer, Tree, Button, Label, TextArea, Collapsible, Checkbox
from textual.containers import HorizontalGroup, VerticalGroup, HorizontalScroll
from importlib.resources import files

TextNodes = [
	"p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "li", "a"
]

class NodeWrapper():
	def __init__(self, html_node, branch):
		self.id = html_node.id
		self.tag_type = html_node.tag_type
		self.node = html_node
		self.branch = branch
		self.added_to_query = False
		self.extract_attributes = []

	def _update_branch_label(self, new_label:str):
		self.branch.label = new_label
		self.branch.refresh()

	def setQuerying(self, value:bool):
		if self.added_to_query != value:
			if value == True:
				self.added_to_query = True

				node_text = f"*<{self.node.tag_type}>"
				if self.node.tag_type in TextNodes and len(self.node.body.strip()) > 0:
					node_text += f" {self.node.body.strip()}"
				self._update_branch_label(node_text)

			elif value == False:
				self.added_to_query = False

				node_text = f"<{self.node.tag_type}>"
				if self.node.tag_type in TextNodes and len(self.node.body.strip()) > 0:
					node_text += f" {self.node.body.strip()}"
				self._update_branch_label(node_text)

	def get_querying(self) -> bool:
		return self.added_to_query
	
	def get_retrieval_instructions(self) -> str:
		if len(self.extract_attributes) == 0:
			return self.node.retrieval_instructions
		else:
			instructions = self.node.retrieval_instructions
			instructions += "\nEXTRACT "
			for attribute in self.extract_attributes:
				instructions += attribute
				if attribute != self.extract_attributes[-1]:
					instructions += ", "

			instructions += ";"

			return instructions
	
	def append_attribute(self, attribute_name) -> None:
		if attribute_name not in self.extract_attributes:
			self.extract_attributes.append(attribute_name)

	def remove_attribute(self, attribute_name) -> None:
		if attribute_name in self.extract_attributes:
			self.extract_attributes.remove(attribute_name)

	def check_query_attribute(self, attribute) -> bool:
		return attribute in self.extract_attributes

class ControlPanel(VerticalGroup):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.current_node = None
		self.query_nodes = []

	def compose(self):
		self.node_details = {
			"tag_type": Label("<no node selected>"),
			"queried_attributes": HorizontalScroll()
		}

		with Collapsible(title="Node Details"):
			yield self.node_details["tag_type"]
			yield self.node_details["queried_attributes"]

		self.contextual_button = Button("<+>", id="node-add-remove", variant="success")
		self.copy_button = Button("<📋>", id="copy-query", variant="primary")

		yield HorizontalGroup(
			HorizontalGroup(self.contextual_button, id="node-add-remove-cont"),
			HorizontalGroup(self.copy_button, id="copy-query-cont"),
			id="ctrl-buttons",
		)

		yield TextArea("", read_only=True)

	def update_node(self, node:NodeWrapper):
		for child in list(self.node_details["queried_attributes"].children):
			child.remove()

		self.current_node = node
		if node is not None:
			if node.get_querying():
				self.contextual_button.label = "<->"
				self.contextual_button.variant = "error"
			else:
				self.contextual_button.label = "<+>"
				self.contextual_button.variant = "success"

			self.node_details["tag_type"].update(f"Type: <{node.tag_type}>")
			for attribute in node.node.html_attributes:
				index = f"query-attribute-{node.id}-{attribute.replace("@", "")}"

				self.node_details["queried_attributes"].mount(
					Checkbox(attribute, id=index, value=self.current_node.check_query_attribute(attribute))
				)
	
	def add_node(self):
		if self.current_node and self.current_node not in self.query_nodes:
			self.query_nodes.append(self.current_node)
			text_area = self.query_one(TextArea)

			self.current_node.setQuerying(True)
			
			text_area.text += self.current_node.get_retrieval_instructions() + "\n"

			self.contextual_button.label = "<->"
			self.contextual_button.variant = "error"

	def append_attribute(self, attribute):
		prev_instr = self.current_node.get_retrieval_instructions()
		self.current_node.append_attribute(attribute)
		new_instr = self.current_node.get_retrieval_instructions()

		text_area = self.query_one(TextArea)
		text_area.text = text_area.text.replace(prev_instr, new_instr)
	
	def remove_node(self):
		if self.current_node and self.current_node in self.query_nodes:
			self.query_nodes.remove(self.current_node)
			text_area = self.query_one(TextArea)
			
			text_area.text = text_area.text.replace(self.current_node.get_retrieval_instructions() + "\n", "")

			self.current_node.setQuerying(False)

			self.contextual_button.label = "<+>"
			self.contextual_button.variant = "success"

	def remove_attribute(self, attribute):
		prev_instr = self.current_node.get_retrieval_instructions()
		self.current_node.remove_attribute(attribute)
		new_instr = self.current_node.get_retrieval_instructions()

		text_area = self.query_one(TextArea)
		text_area.text = text_area.text.replace(prev_instr, new_instr)

class Loom(App):
	CSS_PATH = str(files("scrapegoat").joinpath("gui-styles/tapestry.tcss"))
	BINDINGS = [
		("ctrl+n", "_add_remove_node()", "Add/Remove Node"),
	]

	def __init__(self, root_node, **kwargs):
		super().__init__(**kwargs)
		self.sub_title = "Tree Visualizer"
		self.root_node = root_node
		self.nodes = {}

	def _create_tree_from_root_node(self, node):
		self.nodes = {}
		tree = None

		for child in node.preorder_traversal():
			if tree is None:
				tree = Tree(f"<{child.tag_type}>")
				tree.root._html_node_id = child.id
				self.nodes[child.id] = NodeWrapper(child, tree.root)
				continue

			node_label = f"<{child.tag_type}>"
			if child.tag_type in TextNodes and len(child.body.strip()) > 0:
				node_label += f" {child.body}"

			branch = tree.root if child.parent is None else self.nodes[child.parent.id].branch
			branch.expand()
			branch.allow_expand = False
			
			if len(child.children) == 0:
				child_branch = branch.add_leaf(node_label)
			else:
				child_branch = branch.add(node_label)

			child_branch._html_node_id = child.id
			self.nodes[child.id] = NodeWrapper(child, child_branch)

		return tree
	
	def _add_remove_node(self) -> None:
		if self.control_panel and self.control_panel.current_node:
			if self.control_panel.current_node.get_querying() == False:
				self.control_panel.add_node()
			else:
				self.control_panel.remove_node()

	def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
		if self.control_panel:
			self.control_panel.update_node(self.nodes.get(event.node._html_node_id, None))

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "node-add-remove":
			self._add_remove_node()

	def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
		if event.checkbox.value:
			self.control_panel.append_attribute(str(event.checkbox.label))
		else:
			self.control_panel.remove_attribute(str(event.checkbox.label))

	def compose(self):
		yield Header(name="ScrapeGoat", icon="🐐")
		dom_tree = self._create_tree_from_root_node(self.root_node)
		ctrl = ControlPanel()
		self.control_panel = ctrl
		dom_tree.control_panel = ctrl

		yield dom_tree
		yield ctrl

		yield Footer()

	def weave(self):
		self.run()