from textual.app import App
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.widgets import Header, Footer, Tree, Button, Static, TextArea, Collapsible, Checkbox, Input, ListView, ListItem
from textual.containers import HorizontalGroup, VerticalGroup, HorizontalScroll, Container
from textual.css.query import NoMatches
from importlib.resources import files
from platform import system
from subprocess import Popen, PIPE

NodeAttributes = [
	"tag_type", "id", "has_data", "body"
]

def write_to_clipboard(string:str) -> None:
	os_name = system()
	match os_name:
		case "Windows":
			Popen("clip", env={'LANG': 'en_US.UTF-8'}, stdin=PIPE).communicate(string.encode("utf-8"))
		case "Darwin":
			Popen("pbcopy", env={'LANG': 'en_US.UTF-8'}, stdin=PIPE).communicate(string.encode("utf-8"))
		case "Linux":
			pass
		case _:
			pass

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

	def set_querying(self, value:bool):
		if self.added_to_query != value:
			if value == True:
				self.added_to_query = True

				node_text = f"*<{self.node.tag_type}>"
				if len(self.node.body.strip()) > 0:
					node_text += f" {self.node.body.strip()}"
				self._update_branch_label(node_text)

			elif value == False:
				self.added_to_query = False

				node_text = f"<{self.node.tag_type}>"
				if len(self.node.body.strip()) > 0:
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
	
	def __contains__(self, item) -> bool:	
		if item in f"<{self.tag_type}>":
			return True
		
		if item in self.node.body:
			return True
		
		for html_attribute in self.node.html_attributes.keys():
			if item in f"@{html_attribute}={self.node.html_attributes[html_attribute]}":
				return True
			
		for node_attribute in NodeAttributes:
			if item in f"#{node_attribute}={self.node.to_dict()[node_attribute]}":
				return True
		
		return False

class ControlPanel(VerticalGroup):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.current_node = None
		self.query_nodes = []

	def compose(self):
		self.node_details = {
			"node_desc": ListView(),
			"queried_attributes": HorizontalScroll()
		}

		with Collapsible(title="Node Details"):
			yield self.node_details["node_desc"]
			yield self.node_details["queried_attributes"]

		self.contextual_button = Button("<+>", id="node-add-remove", variant="success")
		self.copy_button = Button("<Copy>", id="copy-query", variant="primary")

		yield HorizontalGroup(
			self.contextual_button,
			self.copy_button,
			id="ctrl-buttons",
		)

		yield TextArea("", read_only=True)

	def update_node(self, node:NodeWrapper):
		self.node_details["node_desc"].clear()
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

			for node_attribute in NodeAttributes:
				index = f"node-attribute-{node.id}-{node_attribute}"

				if node.node.has_attribute(node_attribute):
					if node_attribute != "body":
						self.node_details["node_desc"].append(ListItem(Static(f"{node_attribute}: {node.node.to_dict()[node_attribute]}")))
					elif len(node.node.body) > 0:
						self.node_details["node_desc"].append(ListItem(Static(f"{node_attribute}: ...")))
					self.node_details["queried_attributes"].mount(
						Checkbox(f"{node_attribute}", id=index, value=self.current_node.check_query_attribute(node_attribute))
					)

			for html_attribute in node.node.html_attributes:
				index = f"html-attribute-{node.id}-{html_attribute.replace("@", "")}"

				self.node_details["node_desc"].append(ListItem(Static(f"{html_attribute}: {node.node.html_attributes[html_attribute]}")))
				self.node_details["queried_attributes"].mount(
					Checkbox(f"{html_attribute}", id=index, value=self.current_node.check_query_attribute(html_attribute))
				)

			
	
	def add_node(self):
		if self.current_node and self.current_node not in self.query_nodes:
			self.query_nodes.append(self.current_node)
			text_area = self.query_one(TextArea)

			self.current_node.set_querying(True)
			
			text_area.text += "\n" + self.current_node.get_retrieval_instructions()
			text_area.text = text_area.text.strip()

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
			
			text_area.text = text_area.text.replace(self.current_node.get_retrieval_instructions(), "")
			text_area.text = text_area.text.strip()

			self.current_node.set_querying(False)

			self.contextual_button.label = "<+>"
			self.contextual_button.variant = "success"

	def remove_attribute(self, attribute):
		prev_instr = self.current_node.get_retrieval_instructions()
		self.current_node.remove_attribute(attribute)
		new_instr = self.current_node.get_retrieval_instructions()

		text_area = self.query_one(TextArea)
		text_area.text = text_area.text.replace(prev_instr, new_instr)

	def get_query(self):
		return self.query_one(TextArea).text

class FindModal(ModalScreen):
	BINDINGS = [
		("escape", "app.pop_screen", "Exit Find")
	]

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def compose(self):
		yield Input(placeholder="Search...", id="find-node-input")
		yield Button("Next", id="find-node-next", variant="primary")
		yield Button("Prev", id="find-node-prev", variant="primary")

class Loom(App):
	CSS_PATH = str(files("scrapegoat").joinpath("gui-styles/tapestry.tcss"))
	SCREENS = {"find": FindModal}
	BINDINGS = [
		Binding("ctrl+n", "add_remove_node", "Add/Remove Node", priority=True, tooltip="Adds or removes the selected node."),
		Binding("ctrl+f", "push_screen('find')", "Search Tree", tooltip="Shows/Hides the node search widget."),
	]

	def __init__(self, root_node, **kwargs):
		super().__init__(**kwargs)
		self.sub_title = "Tree Visualizer"
		self.root_node = root_node
		self.nodes = {}
		self.current_search_nodes = []
		self.search_node_index = 0

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
			if len(child.body.strip()) > 0:
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
	
	def _search_tree(self, search_string:str) -> list[NodeWrapper]:
		return_list = []
		for node in self.nodes.values():
			if search_string in node:
				return_list.append(node)
		return return_list
	
	def action_add_remove_node(self) -> None:
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
			self.action_add_remove_node()
		elif event.button.id == "copy-query":
			write_to_clipboard(self.control_panel.get_query())
		elif event.button.id == "find-node-next":
			if len(self.current_search_nodes) > 0:
				self.search_node_index += 1
				if self.search_node_index >= len(self.current_search_nodes):
					self.search_node_index = 0

				self.query_one(Tree).move_cursor(self.current_search_nodes[self.search_node_index].branch, True)
		elif event.button.id == "find-node-prev":
			if len(self.current_search_nodes) > 0:
				self.search_node_index -= 1
				if self.search_node_index < 0:
					self.search_node_index = len(self.current_search_nodes) - 1

				self.query_one(Tree).move_cursor(self.current_search_nodes[self.search_node_index].branch, True)

	def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
		if event.checkbox.value:
			self.control_panel.append_attribute(str(event.checkbox.label))
		else:
			self.control_panel.remove_attribute(str(event.checkbox.label))

	def on_input_changed(self, event: Input.Changed) -> None:
		if event.input.id == "find-node-input":
			self.current_search_nodes = self._search_tree(event.input.value)
			if len(self.current_search_nodes) > 0:
				self.search_node_index = 0
				self.query_one(Tree).move_cursor(self.current_search_nodes[self.search_node_index].branch, True)

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