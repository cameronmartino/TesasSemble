import unittest
from TesasSemble.graph import *
from TesasSemble.graph_components import *

class TestGraphClass(unittest.TestCase):

	def test_DiGraph_init(self):
		G = DiGraph()

		self.assertEqual(G.nodes, dict())
		self.assertEqual(G.edges, [])
	
	def test_RedBlueDiGraph_init(self):
		H = RedBlueDiGraph()

		self.assertEqual(H.coverage, 0)
		self.assertTrue('a' not in H.color)

	def test_add_edge(self):
		G = RedBlueDiGraph()

		A = Node('A')
		B = Node('B')
		C = Node('C')
		AB = Edge('AB', A, B)
		AC = Edge('AC', A, C)
		BC = Edge('BC', B, C)

		G.add_edges_from([AB, AC, BC], ['red', 'blue', 'red'])

		self.assertEqual(G.coverage, 1) # 1 - 1 + 1
		self.assertEqual(G.color[AB], 'red')
		self.assertEqual(G.color[AC], 'blue')
		self.assertEqual(G.color[BC], 'red')
		self.assertIn(AB, G.nodes[A]['out_edges'])
		self.assertNotIn(BC, G.nodes[A]['in_edges'])

	def test_copy(self):
		G = RedBlueDiGraph()

		A = Node('A')
		B = Node('B')
		C = Node('C')
		D = Node('D')
		AB = Edge('AB', A, B)
		AC = Edge('AC', A, C)
		BC = Edge('BC', B, C)
		CD = Edge('CD', C, D)

		G.add_edges_from([AB, AC, BC], ['red', 'blue', 'red'])

		H = G.copy()
		H.add_edge(CD)

		# check nothing got added to G
		self.assertNotIn(D, G.nodes)
		self.assertNotIn(CD, G.edges)
		self.assertNotIn(CD, G.nodes[C]['out_edges'])

		# check old things are a part of H
		self.assertIn(A, H.nodes)
		self.assertIn(AC, H.nodes[C]['in_edges'])

