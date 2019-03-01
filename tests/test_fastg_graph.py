import os
import unittest
from TesasSemble.fastg_graph import fastgs_to_red_blue 

class TestFastgGraph(unittest.TestCase):
	def setUp(self):
		pass

	def test_fastgs_to_red_blue(self):
		path_ = '/'.join(os.path.realpath("__file__").split('/')[:-1])
		g1 = os.path.join(path_,'tests/data/fastg_test/S1.fastg')
		g2 = os.path.join(path_,'tests/data/fastg_test/S2.fastg')
		Gtest = fastgs_to_red_blue(g1,g2)
		self.assertEqual(Gtest.score(.1),0.9)
		self.assertEqual(Gtest.score(1),0.0)
