from textual.app import App
from textual.widgets import Header, Footer, Tree, Button, Label, TextArea
from textual.containers import HorizontalGroup, VerticalGroup
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

	def getQuerying(self) -> bool:
		return self.added_to_query
	
	def getRetrievalInstructions(self) -> str:
		return self.node.retrieval_instructions

class ControlPanel(VerticalGroup):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.current_node = None
		self.query_nodes = []

	def compose(self):
		self.node_label = Label("<no node selected>", id="node-info")
		self.contextual_button = Button("<+>", id="node-add-remove", variant="success")

		yield HorizontalGroup(
			self.node_label,
			HorizontalGroup(
				self.contextual_button,
				id="node-buttons",
			)
		)
		yield TextArea("", read_only=True)

	def update_node(self, node:NodeWrapper):
		self.current_node = node
		lab = self.node_label
		if node is None:
			lab.update("<no node selected>")
		else:
			info = f"ID: {node.id} | Tag: {node.tag_type}"
			lab.update(info)

			if node.getQuerying():
				self.contextual_button.label = "<->"
				self.contextual_button.variant = "error"
			else:
				self.contextual_button.label = "<+>"
				self.contextual_button.variant = "success"
	
	def add_node(self):
		if self.current_node and self.current_node not in self.query_nodes:
			self.query_nodes.append(self.current_node)
			text_area = self.query_one(TextArea)

			self.current_node.setQuerying(True)
			
			text_area.text += self.current_node.getRetrievalInstructions() + "\n"

			self.update_node(self.current_node)
	
	def remove_node(self):
		if self.current_node and self.current_node in self.query_nodes:
			self.query_nodes.remove(self.current_node)
			text_area = self.query_one(TextArea)
			lines = text_area.text.split("\n")
			lines = [line for line in lines if line.strip() != self.current_node.getRetrievalInstructions()]
			text_area.text = "\n".join(lines)

			self.current_node.setQuerying(False)

			self.update_node(self.current_node)

class Loom(App):
	CSS_PATH = str(files("scrapegoat").joinpath("gui-styles/tapestry.tcss"))
	BINDINGS = []

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

	def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
		if self.control_panel:
			self.control_panel.update_node(self.nodes.get(event.node._html_node_id, None))

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "node-add-remove":
			if self.control_panel and self.control_panel.current_node:
				if self.control_panel.current_node.getQuerying() == False:
					self.control_panel.add_node()
				else:
					self.control_panel.remove_node()

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