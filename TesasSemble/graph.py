from graph_components import Node, Edge 

class DiGraph:

	def __init__(self):
		self.nodes = []
		self.edges = []

	def maximal_non_branching_paths(self):
		None
		pass

	def neighbor_graphs(self, super_graph, k):
		# TODO generator
		pass

	def adjacent_graphs(self, super_graph, k):
		# TODO generator
		pass

	def add_edge(self, edge):
		pass

	def add_node(self, node):
		pass

	def add_edges_from(self, edge):
		pass

	def add_nodes_from(self, edge):
		pass

	def remove_edge(self, edge):
		pass

	def remove_node(self, node):
		pass

	def remove_edges_from(self, edges):
		pass

	def remove_nodes_from(self, nodes):
		pass

	def subgraph_from_edgelist(self, edges):
		pass

class RedBlueDiGraph(DiGraph):

	def __init__(self):
		super(RedBlueDiGraph, self).__init__()
		self.coverage = 0

	def score(self):
		pass

	def add_edge(self, edge, color):
		pass

	def add_edges_from(self, edgelist):
		# TODO specify input form
		pass

	def calculate_coverage(self):
		# TODO return sum([1 if edge.data['color'] == 'blue' for edge in self.edges])
		pass

	def subgraph_from_edgelist(self, edges):
		subgraph = super(RedBlueDiGraph, self).subgraph_from_edgelist(edges)
		subgraph.coverage = self.calculate_coverage()



