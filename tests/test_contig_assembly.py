import unittest

from TesasSemble.graph import *
from TesasSemble.graph_components import *
from TesasSemble.contig_assembly import contig_assembly

class TestContigAssembly(unittest.TestCase):

    def setup_small_diamond_graph(self):
        self.G_ = RedBlueDiGraph()

        self.A = Node(1)
        self.B = Node(2)
        self.C = Node(3)
        self.D = Node(4)
        self.E = Node(5)
        self.F = Node(6)
        self.G = Node(7)
        self.H = Node(8)
        self.I = Node(9)
        self.J = Node(10)

        self.AC = Edge('AC', self.A, self.C)
        self.BC = Edge('BC', self.B, self.C)
        self.CD = Edge('CD', self.C, self.D)
        self.CF = Edge('CF', self.C, self.F)
        self.DE = Edge('DE', self.D, self.E)
        self.FE = Edge('FE', self.F, self.E)
        self.EG = Edge('EG', self.E, self.G)
        self.EH = Edge('EH', self.E, self.H)
        self.IJ = Edge('IJ', self.I, self.J)
        #self.JI = Edge('JI', self.J, self.I)
        
        self.reads_map = {}
        self.reads_map[1] = 'ThisisthestringSpellLedbiePathNode1tothatOth'
        self.reads_map[2] = 'ThisisthestringSpellLedbiePathNode2tothatOtherN0de'
        self.reads_map[3] = 'tothatOtherN0de#bred3'
        self.reads_map[4] = '#bred3NowIwouldtellaninterestingstorybutIm'
        self.reads_map[5] = 'interestingstorybutImnotcreativeLikethat'
        self.reads_map[6] = '3anasweomeandin'
        self.reads_map[7] = 'stingstorybutImnotcreativeLikethatPerhapsThisflawwillbeMyUltimateATCGTFailure'
        self.reads_map[8] = 'ikethatAndYetPerhapsselfAwaritywillAllowmyselftosupersedethseeSHORTcomings'
        self.reads_map[9] = 'ThisStringShallBeastrnageMirroryStringAlsowithSomeNonRCNTssuchasAGGGTCCC'
        self.reads_map[10] = 'suchasAGGGTCCC___someinternalTexxtMakesoforACompleteeString' #____ThisStringShallBeastrnageMirroryStringAlsow'
        
        EC = ['ThisisthestringSpellLedbiePathNode1tothatOtherN0de#bred3',
                    'tothatOtherN0de#bred3NowIwouldtellaninterestingstorybutImnotcreativeLikethat',
                    'tothatOtherN0de#bred3anasweomeandinterestingstorybutImnotcreativeLikethat',
                    'ThisisthestringSpellLedbiePathNode2tothatOtherN0de#bred3',
                    'interestingstorybutImnotcreativeLikethatPerhapsThisflawwillbeMyUltimateATCGTFailure',
                    'interestingstorybutImnotcreativeLikethatAndYetPerhapsselfAwaritywillAllowmyselftosupersedethseeSHORTcomings',
              'ThisStringShallBeastrnageMirroryStringAlsowithSomeNonRCNTssuchasAGGGTCCC___someinternalTexxtMakesoforACompleteeString']

        self.expected_contigs = EC

        edge_list = [self.AC, self.BC, self.CD, self.CF, self.DE, self.FE, self.EG, self.EH, self.IJ] #, self.JI]
        colors 	  = ['blue',  'red',   'red',   'blue',  'red',   'blue',  'red',   'blue',  'red'] #,   'red'  ]
        self.G_.add_edges_from(edge_list, colors)


    def teardown_small_diamond_graph(self):
        del self.G_
        del self.sub
        del self.reads

        del self.A
        del self.B
        del self.C
        del self.D
        del self.E
        del self.F
        del self.G
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
        #del self.JI 

    def test_small_diamond_graph(self):
        self.setup_small_diamond_graph()

        contigs = contig_assembly(self.G_, self.reads_map)

        self.assertCountEqual(contigs,self.expected_contigs)

        self.teardown_small_diamond_graph

