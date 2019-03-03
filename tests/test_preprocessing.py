import os
import unittest
from TesasSemble.preprocessing import GraphConstructor,debruijn

class Testpreprocessing(unittest.TestCase):
	def setUp(self):
		# files
		path_ = '/'.join(os.path.realpath("__file__").split('/')[:-1])
		self.g1 = os.path.join(path_,'tests/data/fastq_test/S0.fastq')
		self.g2 = os.path.join(path_,'tests/data/fastq_test/S1.fastq')
		self.g3 = os.path.join(path_,'tests/data/fastq_test/S2.fastq')
		# seq test
		self.seq_truth = [('CGA', 'GAT'),('GAT', 'ATA'),
						  ('ATA', 'TAT'),('TAT', 'ATA'),
						  ('AGC', 'GCC'),('GCC', 'CCT'),
						  ('CCT', 'CTC'),('CTC', 'TCT')]
		self.test = ['CGATATA','AGCCTCT']

		pass

	def test_GraphConstructor(self):

		# all fit 
		G_RdBu = GraphConstructor().fit([self.g1,self.g2,self.g3])
		G1_RdBu = G_RdBu.condition_graph(self.g1)
		G2_RdBu = G_RdBu.condition_graph(self.g2)
		G3_RdBu = G_RdBu.condition_graph(self.g3)
		# single
		G1_RdBu_single, node_map = GraphConstructor().fit_single([self.g1,self.g2,self.g3],self.g1)
		G2_RdBu_single, node_map = GraphConstructor().fit_single([self.g1,self.g2,self.g3],self.g2, nodes=node_map)
		G3_RdBu_single, node_map = GraphConstructor().fit_single([self.g1,self.g2,self.g3],self.g3, nodes=node_map)
		# tests 
		self.assertEqual(G1_RdBu == G2_RdBu, False)
		self.assertEqual(G1_RdBu_single == G2_RdBu_single, False)
		self.assertEqual(G1_RdBu.calculate_coverage(), G1_RdBu_single.calculate_coverage())
		self.assertEqual(G2_RdBu.calculate_coverage(), G2_RdBu_single.calculate_coverage())
		self.assertEqual(G1_RdBu.calculate_coverage(), G3_RdBu.calculate_coverage())
		self.assertEqual(G1_RdBu_single.calculate_coverage(),G3_RdBu_single.calculate_coverage())
		self.assertEqual(G1_RdBu.calculate_coverage(), G1_RdBu_single.calculate_coverage())

	def test_debruijn(self):

		self.assertListEqual(sorted(self.seq_truth),
				       		 sorted(debruijn(self.test,4)))

