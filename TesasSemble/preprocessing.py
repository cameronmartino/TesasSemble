import numpy as np
from Bio import SeqIO
from TesasSemble.graph import *
from TesasSemble.graph_components import *
from TesasSemble.base import _BaseRedBlueFastq

class RBFG(_BaseRedBlueFastq):
    
    """

    This function takes multiple fastq files 
    generated over conditions and builds red-blue
    graphs for each one. The format is sklearn style.

    Parameters
    ----------
    
    .__init__(k)
    ----------
    
    k: int - the k-mer length to use: default: 21

    .fit(conditions)
    ----------
    
    conditions - list of strings - paths to fastq files
    
    
    .condition_graph(cond)
    ----------
    
    cond - string - paths to fastq, must be in conditions
    
    .leftout_rest_graph(cond)
    ----------
    
    cond - string - paths to fastq, must be in conditions
    
    .node_map()
    ----------
    
    None
    
    
    Returns
    -------

    .condition_graph(cond)
    ----------
    
    G: of TesasSemble.graph type Red edges are of cond.
    
    .leftout_rest_graph(cond)
    ----------
    
    Edges of all graphs not including cond
    
    .node_map()
    ----------
    
    dict - fasta format of node id and then seq.

    Raises
    ------
    
    ValueError - if condition_graph(cond) not 
                 in fit conditions

    References
    ----------
    .. [1] http://fastg.sourceforge.net/
    
    Examples
    --------

    >>> from TesasSemble.preprocessing import RBFG

    example fastgs in tests/data/fastq_test
    - a fist sample S1.fastq
    - a second sample S2.fastq
    
    >>> g1 = 'tests/data/fastg_test/S0.fastq'
    >>> g2 = 'tests/data/fastg_test/S1.fastq'
    >>> G_RdBu = RBFG.fit([g1,g2])
    
    Now we can get the conditional graphs for each.
    
    >>> G1_RdBu  = G_RdBu.condition_graph(g1)
    >>> G2_RdBu  = G_RdBu.condition_graph(g2)
    
    Alternatively you can fit_transform for one condition
    
    >>> G1_RdBu_single, node_map = RBFG().fit_single([g1,g2],g1)
    >>> G2_RdBu_single, node_map = RBFG().fit_single([g1,g2], g2, nodes = node_map)

    Now we can also map each node back to it's kmer.
    
    >>> node_fasta = G_RdBu.node_map()
    
    """

    def __init__(self, k=21):
        
        #k-1-mers
        self.k = k
        
        return
    
    def fit(self, conditions):
        
        self.conditions = conditions
        
        # generate edges 
        self.edges = {r:debruijn([str(fasta.seq) for fasta \
                             in SeqIO.parse(open(r),
                                            'fasta')],self.k) 
                      for r in self.conditions}
        
        # set of nodes 
        nodes = set([z for r,x in self.edges.items() 
                     for y in x 
                     for z in y])
        self.nodes = {n:i for i,n in enumerate(nodes)}
        
        #print(self.nodes['AATACTGATGAGTCTACATT'])
        
        # remove seq from id_name and add int ID
        self.edges = {k:[(self.nodes[v_[0]],
                          self.nodes[v_[1]]) 
                      for v_ in v] 
                      for k,v in self.edges.items()}
        
        # get leave-one-out graphs
        self.generate_rest()
        
        # generate RdBu graphs
        self.generate_conditions()
        
        return self
        
    def fit_single(self, conditions, cond, nodes = {}):
        
        self.conditions = conditions
        
        # check cond is in conditions
        if cond not in self.conditions:
            raise ValueError('Condition is not in input ',
                             'conditions: must be one of '\
                             +' '.join(self.conditions))
        
        # generate edges 
        self.edges = {r:debruijn([str(fasta.seq) for fasta \
                             in SeqIO.parse(open(r),
                                            'fasta')],self.k) 
                      for r in self.conditions}
        
        # set of nodes 
        if len(nodes) == 0:
            nodes = set([z for r,x in self.edges.items() 
                         for y in x 
                         for z in y])
            self.nodes = {n:i for i,n in enumerate(nodes)}
        else:
            new_nodes = set([z for r,x in self.edges.items() 
                             for y in x 
                             for z in y])
            new_nodes = new_nodes - set(nodes.keys())
            self.nodes = {**nodes,**{n:np.max(nodes.values())+i 
                          for i,n in enumerate(new_nodes)}}
                
        # remove seq from id_name and add int ID
        self.edges = {k:[(self.nodes[v_[0]],
                          self.nodes[v_[1]]) 
                      for v_ in v] 
                      for k,v in self.edges.items()}
        
        # get leave-one-out rest graph
        self.generate_rest_one(cond)
        
        # return  RdBu graph for condition
        self.conditional_graph(cond)
        return self.gtmp, self.nodes
        
    def generate_rest(self):
        
        # first get rest graphs for each condition
        self.rest_leftout = {}
        for cond in self.conditions:
            rest = [v for k,v in self.edges.items() if k!=cond]
            self.rest_leftout[cond] = list(set([r_ for res in rest 
                                                for r_ in res]))        
        return 
    
    def generate_rest_one(self, cond):
        
        # first get rest graphs for each condition
        self.rest_leftout = {}
        rest = [v for k,v in self.edges.items() if k!=cond]
        self.rest_leftout[cond] = list(set([r_ for res in rest 
                                            for r_ in res]))        
        return 

    def generate_conditions(self):
        
        self.cond_graphs = {}
        for cond_ in self.conditions:
            self.conditional_graph(cond_)
            self.cond_graphs[cond_] = self.gtmp
 
        return 

    def conditional_graph(self,cond):
        
        # get sub edges 
        cond_tmp = self.edges[cond]
        rest_tmp = self.rest_leftout[cond]
        # graph to fill 
        GRdBu = RedBlueDiGraph()
        # set nodes and edges 
        nodes_G_tmp = {}
        edge_G_tmp = {}
        for i,n in enumerate(set(cond_tmp+rest_tmp)):
            nodes_G_tmp[n[0]] = Node(n[0])
            nodes_G_tmp[n[1]] = Node(n[1])
            edge_G_tmp['-'.join([str(n[0]),
                                str(n[1])])] = Edge('-'.join([str(n[0]),
                                                              str(n[1])]), 
                                                   nodes_G_tmp[n[0]], 
                                                   nodes_G_tmp[n[1]])
        # build graph Red edges
        GRdBu.add_edges_from([edge_G_tmp[str(n[0])+'-'+str(n[1])] 
                              for n in cond_tmp],
                              ['red']*len(cond_tmp))

        # build graph blue edges (only one blue edge per node)
        blue = list(set(rest_tmp)-set(cond_tmp))
        GRdBu.add_edges_from([edge_G_tmp[str(n[0])+'-'+str(n[1])] 
                              for n in blue],
                              ['blue']*len(blue))
        self.gtmp =  GRdBu.copy()
        return
      
def debruijn(seqs,k):
    # debruijn helper
    kmers = []
    for seq in seqs:
        for f in range(len(seq)+1-k):
            kmers.append((seq[f:f+k][:-1],seq[f:f+k][1:]))
    return kmers

