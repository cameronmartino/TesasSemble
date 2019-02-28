class DiGraph:

	def __init__(self):
		self.nodes = dict()
		self.edges = [] 

	def copy(self):
		H_ = __class__()
		H_.add_edges_from(self.edges)
		return H_

	def maximal_non_branching_paths(self):
		# return list of paths (made up of graph nodes)
		paths = []
		visited_edges = set()
		for node in self.nodes:
			if not self.is_1_in_1_out(node):
				if self.out_degree(node) > 0:
					out_edges = self.nodes[node]['out_edges']
					for edge in out_edges:
						visited_edges.add(edge)
						to_node = edge.node_b
						non_branching_path = [edge]
						while self.is_1_in_1_out(to_node):
							out_edge = self.nodes[to_node]['out_edges'][0]
							non_branching_path.append(out_edge)
							visited_edges.add(out_edge)
							to_node = out_edge.node_b
						paths.append(non_branching_path)

		# everything left must be in a cycle
		cycle_edges = set(filter(lambda edge : edge not in visited_edges, self.edges))
		while len(cycle_edges) > 0:
			edge = cycle_edges.pop()
			non_branching_path = [edge]
			start_node = edge.node_b
			to_node = edge.node_b
			while to_node != start_node:
				out_edge = self.nodes[to_node]['out_edges'][0]
				non_branching_path.append(out_edge)
				cycle_edges.remove(out_edge)
				visited_edges.add(out_edge)
				to_node = out_edge.node_b
				if len(cycle_edges) == 0:
					break
			paths.append(non_branching_path)

		return paths

	def neighbor_graphs(self, sub_graph, super_graph, k):
		if k >= 0:
			yield sub_graph
			for neighbor in sub_graph.plus_neighbors(sub_graph):
				yield from neighbor.neighbor_graphs(neighbor, super_graph, k-1)

	def adjacent_graphs(self, sub_graph, super_graph, k):
		if k >= 0:
			yield sub_graph
			for neighbor in sub_graph.plus_neighbors(sub_graph):
				yield from neighbor.adjacent_graphs(neighbor, super_graph, k-1)
			for neighbor in sub_graph.minus_neighbors(sub_graph):
				yield from neighbor.adjacent_graphs(neighbor, super_graph, k-1)

	def plus_neighbors(self, super_graph):
		paths = list()
		# first generate paths
		for edge in self.edges:
			from_, to = edge.node_a, edge.node_b
			from_super_edges = super_graph.nodes['out_edges'][to]
			to_super_edges = super_graph.nodes['in_edges'][from_]
			not_in_H = lambda edge : edge not in H
			from_super_edges = filter(not_in_H, from_super_edges)
			to_super_edges = filter(not_In_H, to_super_edges)
			paths.extend(from_super_edges)
			paths.extend(to_super_edges)

		paths = set(paths)

		# then generate a graph for each unique path
		for path in paths:
			H_ = self.copy()
			H_.add_edge(path)
			yield H_

	def minus_neighbors(self):
		for edge in self.edges:
			H_ = self.copy()
			H_.remove_edge(edge)
			yield H_

	def add_edge(self, edge):
		node_a, node_b = edge.node_a, edge.node_b
		self.add_node(node_a)
		self.add_node(node_b)
		self.nodes[node_a]['out_edges'].append(edge)
		self.nodes[node_b]['in_edges'].append(edge)
		self.edges.append(edge)

	def add_node(self, node):
		if node not in self.nodes:
			self.nodes[node] = {'in_edges': [], 'out_edges': []}

	def in_degree(self, node):
		return len(self.nodes[node]['in_edges'])

	def out_degree(self, node):
		return len(self.nodes[node]['out_edges'])

	def is_1_in_1_out(self, node):
		return self.in_degree(node) == 1 and self.out_degree(node) == 1

	def add_edges_from(self, edges):
		for edge in edges:
			self.add_edge(edge)

	def add_nodes_from(self, nodes):
		for node in nodes:
			self.add_node(node)

	def remove_edge(self, edge):
		self.nodes[node_a]['out_edges'].remove(edge)
		self.nodes[node_b]['in_edges'].remove(edge)
		self.edges.remove(edge)
		if len(self.nodes[node_a]['out_edges']) + len(self.nodes[node_a]['in_edges']) == 0:
			self.nodes.remove(node_a)
		if len(self.nodes[node_b]['out_edges']) + len(self.nodes[node_b]['in_edges']) == 0:
			self.nodes.remove(node_b)

	def remove_node(self, node):
		for edge in self.nodes[node]['in_edges']:
			self.remove_edge(edge)
		for edge in self.nodes[node]['out_edges']:
			self.remove_edge(edge)
		assert node not in self.nodes

	def remove_edges_from(self, edges):
		for edge in edges:
			self.remove_edge(edge)

	def remove_nodes_from(self, nodes):
		for node in nodes:
			self.remove_node(node)

	def subgraph_from_edgelist(self, edges):
		# TODO assert edges are in graph
		pass

class RedBlueDiGraph(DiGraph):

	RED = 'red'
	BLUE = 'blue'

	def __init__(self):
		super(RedBlueDiGraph, self).__init__()
		self.coverage = 0
		self.color = dict()

	def score(self, alpha):
		avg_coverage = self.coverage / len(self.edges)
		paths = self.maximal_non_branching_paths()
		total_path_length = sum([len(path) for path in paths])
		avg_path_length =  total_path_length/len(paths)
		return alpha * avg_coverage + (1-alpha) * avg_path_length

	def add_edge(self, edge, color='blue'):
		super(RedBlueDiGraph, self).add_edge(edge)
		if color == self.RED:
			self.color[edge] = self.RED
			self.coverage += 1
		else:
			self.coverage -= 1
			self.color[edge] = self.BLUE
	
	def add_edges_from(self, edges, colors=None):
		if colors is not None:
			assert len(colors) == len(edges)
			for i, edge in enumerate(edges):
				self.add_edge(edge, color=colors[i])
		else:
			super(RedBlueDiGraph, self).add_edges_from(edges)

	def calculate_coverage(self):
		return self.coverage 

	def remove_edge(self, edge):
		if self.color[edge] == self.RED:
			self.coverage -= 1
		else:
			self.coverage += 1
		self.color.remove(edge)
		super(RedBlueDiGraph, self).remove_edge(edge)

