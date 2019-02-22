from graph_components import Node, Edge 

class DiGraph:

	def __init__(self):
		self.nodes = {} 
		self.edges = [] 
		self.in_neighbors = dict() # list of in_neibhors for each node
		self.out_neighbors = dict() # list of out_neighbors for each node

	def maximal_non_branching_paths(self):
		# return list of paths (made up of graph nodes)
		pass

	def neighbor_graphs(self, super_graph, k):
		# TODO generator
		pass

	def adjacent_graphs(self, super_graph, k):
		# TODO generator
		pass

	def add_edge(self, edge):
		nodes = edge.node_a, edge.node_b
		for node in nodes:
			self.add_node(node)

		self.out_neighbors[nodes[0]].append(nodes[1])
		self.in_neighbors[nodes[1]].append(nodes[0])

	def add_node(self, node):
		if node not in self.nodes:
			self.nodes.add(node)
			self.in_neighbors[node] = []
			self.out_neighbors[node] = []

	def in_degree(self, node):
		return len(self.in_neighbors(node))

	def out_degree(self, node):
		return len(self.out_neighbors(node))

	def add_edges_from(self, edges):
		for edge in edges:
			self.add_edge(edge)

	def add_nodes_from(self, nodes):
		for node in nodes:
			self.add_node(node)

	def remove_edge(self, edge):
		pass

	def remove_node(self, node):
		pass

	def remove_edges_from(self, edges):
		pass

	def remove_nodes_from(self, nodes):
		pass

	def subgraph_from_edgelist(self, edges):
		# TODO assert edges are in graph
		pass

	def edge_neighbors(self, edge):
		# TODO make sure this is both edges_after and edges_before
		pass

	def edges_after(self, edge):
		# TODO use edge object not list for edge
		return [[edge[1], e_to] for e_to in self.out_neighbors(edge[1])]

	def edges_before(self, edge):
		# TODO use edge object not list for edge
		return [[e_from, edge[0]] for e_from in self.in_neighbors(edge[0])]


class RedBlueDiGraph(DiGraph):

	def __init__(self):
		super(RedBlueDiGraph, self).__init__()
		self.coverage = 0

	def score(self, alpha):
		avg_coverage = self.coverage / len(self.edges)
		paths = self.maximal_non_branching_paths()
		total_path_length = sum([len(path) for path in paths])
		avg_path_length =  total_path_length/len(paths)
		return alpha * avg_coverage + (1-alpha) * avg_path_length

	def add_edge(self, edge):
		assert 'color' in edge.data
		if edge.data['color'] == 'red':
			self.coverage += 1
		super(RedBlueDiGraph, self).add_edge(edge)

	def calculate_coverage(self):
		return sum([1 for edge in self.edges if edge.data['color'] == 'red' ])


