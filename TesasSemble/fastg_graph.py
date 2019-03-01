from TesasSemble.graph import *
from TesasSemble.graph_components import *

def fastgs_to_red_blue(path_g1,path_g2):
    
    """

    This function takes two fastg assembly outputs. 
    Each input should be a seperate sample derived from 
    a seperate contiional variable, such as time. 

    Parameters
    ----------

    path_g1: str - a full path to fastg1
    path_g2: str - a full path to fastg2

    Returns
    -------
    G: of TesasSemble.graph type

    Raises
    ------
    ValueError

    None (TODO)

    References
    ----------
    .. [1] http://fastg.sourceforge.net/
    
    Examples
    --------

    >>> from TesasSemble.fastg_graph import fastgs_to_red_blue

    example fastgs in tests/data/fastg_test
    - a fist sample S1.fastg
    - a second sample S2.fastg
    
    they have a overlapping edge and each has a unque edge.

    >>> g1 = 'tests/data/fastg_test/S1.fastg'
    >>> g2 = 'tests/data/fastg_test/S1.fastg'
    >>> G = fastgs_to_red_blue(g1,g2)

    """
    adj_list_g1 = fastg_to_dict(path_g1)
    adj_list_g2 = fastg_to_dict(path_g2)
    

    ## shared red-and-blue edges 
    clean_string = lambda word: word.replace('>','').replace("'",'').replace(";",'')
    map_g1_g2 = [[clean_ids(x),clean_ids(y)] 
                 for x,v1 in read_fastg(path_g1).items() 
                 for y,v2 in read_fastg(path_g2).items() 
                 if v1==v2]
    #print(map_g1_g2)
    
    map_g1_g2_names = {x_:y_ for x,y in map_g1_g2 
                       for x_,y_ in zip(x.split(' '),
                                        y.split(' '))}
    ## make g1 only (red)
    g1_only = [x for x in adj_list_g1 
               if not any(x==y[0] for y in map_g1_g2)]
    ## make g2 only (blue)
    g2_only = [x for x in adj_list_g2 
               if not any(x==y[1] for y in map_g1_g2)]
    # map g2 nodes to g1 nodes
    g2_only = [' '.join([map_g1_g2_names[y] 
                         if y in map_g1_g2_names.keys() else y 
                         for y in x.split(' ')]) for x in g2_only]

    ## add both edges and nodes ##
    G = RedBlueDiGraph()

    # red and blue
    nodes_ = list(set([j for i,_ in map_g1_g2 
                         for j in i.split(' ')]))
    nodes_G = {id_:Node(id_) for i,id_ in enumerate(nodes_)}
    # add edges for both
    edges = {}
    for i,_ in map_g1_g2:
        edges_ = i.split(' ')
        for j in edges_[1:]:
            edges[str(edges_[0])+'_'+str(j)] = Edge(str(edges_[0])+'_'+str(j), 
                                                nodes_G[edges_[0]], nodes_G[j])
    G.add_edges_from(list(edges.values()),['red']*len(list(edges.values())))
    G.add_edges_from(list(edges.values()),['blue']*len(list(edges.values())))

    # red (g1) only
    edges = {}
    for i in g1_only:
        edges_ = i.split(' ')
        for j in edges_[1:]:
            edges[str(edges_[0])+'_'+str(j)] = Edge(str(edges_[0])+'_'+str(j), 
                                                nodes_G[edges_[0]], nodes_G[j])
    G.add_edges_from(list(edges.values()),['red']*len(list(edges.values())))

    # blue (g2) only
    edges = {}
    for i in g1_only:
        edges_ = i.split(' ')
        for j in edges_[1:]:
            edges[str(edges_[0])+'_'+str(j)] = Edge(str(edges_[0])+'_'+str(j), 
                                                nodes_G[edges_[0]], nodes_G[j])
    G.add_edges_from(list(edges.values()),['blue']*len(list(edges.values())))
    
    return G

def read_fastg(fastg_in):
    
    """
    Converts fastg file to dict with 
    headers in keys and seqs in edges.
    
    """
    
    lines = [line.rstrip('\n') for line in open(fastg_in)]
    fastg = {}
    for i in range(len(lines)):
        if '>' == lines[i][0]:
            if i>0:
                fastg[header_]=''.join(seq_)
            seq_ = []
            header_ = lines[i]
        else:
            seq_.append(lines[i])   

    return fastg

def clean_ids(head):
    
    
    """
    Cleans headers from fastg
    
    input is str form fastq
    output is str
    
    """
    
    clean_string = lambda word: word.replace('>','').replace("'",'').replace(";",'')
    if len(head.split(':'))>1:
        return clean_string(head.split(':')[0]).split('_')[1]+' '\
               +' '.join([clean_string(y).split('_')[1] 
                          for y in head.split(':')[1].split(',')]) 
    else:
        return clean_string(head.split(':')[0].split('_')[1])
    
def fastg_to_dict(fastg_in, remove_isolates=True):
    lines = [line.rstrip('\n') for line in open(fastg_in) if '>' in line.rstrip('\n')]
    clean_string = lambda word: word.replace('>','').replace("'",'').replace(";",'')
    adj = [clean_string(head.split(':')[0]).split('_')[1]+' '+' '.join([clean_string(y).split('_')[1] 
           for y in head.split(':')[1].split(',')]) 
           if len(head.split(':'))>1 else clean_string(head.split(':')[0]) for head in lines]
    if remove_isolates==True:
        adj=[adj_ for adj_ in adj if len(adj_.split(' '))>1]
    
    return adj
