import unittest
from TesasSemble.graph import *
from TesasSemble.graph_components import *
from TesasSemble.optim import *
from TesasSemble.optim_utils import *

class TestGraphClass(unittest.TestCase):

	def setup_small_diamond_graph(self):
		self.G = RedBlueDiGraph()

		self.A = Node('A')
		self.B = Node('B')
		self.C = Node('C')
		self.D = Node('D')
		self.E = Node('E')
		self.F = Node('F')
		self.G_ = Node('G')
		self.H = Node('H')
		self.I = Node('I')
		self.J = Node('J')

		self.AC = Edge('AC', self.A, self.C)
		self.BC = Edge('BC', self.B, self.C)
		self.CD = Edge('CD', self.C, self.D)
		self.CF = Edge('CF', self.C, self.F)
		self.DE = Edge('DE', self.D, self.E)
		self.FE = Edge('FE', self.F, self.E)
		self.EG = Edge('EG', self.E, self.G_)
		self.EH = Edge('EH', self.E, self.H)
		self.IJ = Edge('IJ', self.I, self.J)
		self.JI = Edge('JI', self.J, self.I)

		edge_list = [self.AC, self.BC, self.CD, self.CF, self.DE, self.FE, self.EG, self.EH, self.IJ, self.JI]
		colors 	  = ['blue',  'red',   'red',   'blue',  'red',   'blue',  'red',   'blue',  'red',   'red'  ]
		self.G.add_edges_from(edge_list, colors)

		self.sub = RedBlueDiGraph()
		self.sub.add_edges_from([self.AC], ['blue'])

	def teardown_small_diamond_graph(self):
		del self.G
		del self.sub

		del self.A
		del self.B
		del self.C
		del self.D
		del self.E
		del self.F
		del self.G_
		del self.H
		del self.I
		del self.J

		del self.AC 
		del self.BC 
		del self.CD 
		del self.CF 
		del self.DE 
		del self.FE 
		del self.EG 
		del self.EH 
		del self.IJ 
		del self.JI 


	def test_randomized_optimal_subgraph(self):
		self.setup_small_diamond_graph()
		
		approximate_subgraph, best_score = \
				randomized_optimal_subgraph(self.sub, self.G, 2, 0.5)

		# TODO more thorough check of equivalence of subgraph
		self.assertEqual(4, len(approximate_subgraph.edges))

		self.teardown_small_diamond_graph()



