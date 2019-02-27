import unittest
from itertools import cycle
from TesasSemble.graph import *
from TesasSemble.graph_components import *

class TestGraphClass(unittest.TestCase):

	def setup_ABC_graph(self):
		"""
		Constructs a small triangle graph
		"""
		self.G = RedBlueDiGraph()

		self.A = Node('A')
		self.B = Node('B')
		self.C = Node('C')
		self.AB = Edge('AB', self.A, self.B)
		self.AC = Edge('AC', self.A, self.C)
		self.BC = Edge('BC', self.B, self.C)

		self.G.add_edges_from([self.AB, self.AC, self.BC], ['red', 'blue', 'red'])

	def teardown_ABC_graph(self):
		del self.G
		del self.A 
		del self.B 
		del self.C 
		del self.AB
		del self.AC
		del self.BC

	def setup_small_cycle_graph(self):
		self.G = RedBlueDiGraph()

		self.A = Node('A')
		self.B = Node('B')
		self.C = Node('C')
		self.D = Node('D')

		self.AB = Edge('AB', self.A, self.B)
		self.BC = Edge('BC', self.B, self.C)
		self.CD = Edge('CD', self.C, self.D)
		self.DA = Edge('DA', self.D, self.A)

		self.G.add_edges_from([self.AB, self.BC, self.CD, self.DA], ['red', 'blue', 'red', 'red'])

	def teardown_small_cycle_graph(self):
		del self.G

		del self.A
		del self.B
		del self.C
		del self.D

		del self.AB
		del self.BC
		del self.CD
		del self.DA

	def test_DiGraph_init(self):
		G = DiGraph()

		self.assertEqual(G.nodes, dict())
		self.assertEqual(G.edges, [])
	
	def test_RedBlueDiGraph_init(self):
		H = RedBlueDiGraph()

		self.assertEqual(H.coverage, 0)
		self.assertTrue('a' not in H.color)

	def test_add_edge(self):
		self.setup_ABC_graph()

		self.assertEqual(self.G.coverage, 1) # 1 - 1 + 1
		self.assertEqual(self.G.color[self.AB], 'red')
		self.assertEqual(self.G.color[self.AC], 'blue')
		self.assertEqual(self.G.color[self.BC], 'red')
		self.assertIn(self.AB, self.G.nodes[self.A]['out_edges'])
		self.assertNotIn(self.BC, self.G.nodes[self.A]['in_edges'])
		self.assertIn(self.AB, self.G.edges)

		self.teardown_ABC_graph()

	def test_copy(self):
		self.setup_ABC_graph()

		D = Node('D')

		CD = Edge('CD', self.C, D)

		H = self.G.copy()
		H.add_edge(CD)

		# check nothing got added to G
		self.assertNotIn(D, self.G.nodes)
		self.assertNotIn(CD, self.G.edges)
		self.assertNotIn(CD, self.G.nodes[self.C]['out_edges'])

		# check old things are a part of H
		self.assertIn(self.A, H.nodes)
		self.assertIn(self.AC, H.nodes[self.C]['in_edges'])

		self.teardown_ABC_graph()

	def test_max_non_branch_paths_small_triangle(self):
		self.setup_ABC_graph()

		paths = self.G.maximal_non_branching_paths()
		expected_paths = [[self.AB, self.BC], [self.AC]]
		self.assertCountEqual(paths, expected_paths)

		self.teardown_ABC_graph()

	def test_mnbp_cycle(self):
		self.setup_small_cycle_graph()

		paths = self.G.maximal_non_branching_paths()
		expected_path = [self.AB, self.BC, self.CD, self.DA]

		# there should only be one maximal nonbranching path
		print(paths)
		self.assertTrue(len(paths) == 1)
		self.assertIn(expected_path, cycle(paths[0]))

		self.teardown_small_cycle_graph()

