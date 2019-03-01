import random
import TesasSemble.graph as graph

# TODO implement graph sampling techniques

def i_sample_edges(Graph, i):
	edge_list = [edge for edge in Graph.edges if Graph.color[edge] == 'red']
	random.shuffle(edge_list)
	sampled_edges = edge_list[:i]
	H = graph.RedBlueDiGraph()
	H.add_edges_from(sampled_edges)
	return H

def initial_subgraph(G):
    '''Pick a random connected subgraph.'''
    pass

def modify_one_edge(H, G):
    # decide if add or remove
    decision = random.choice(['add', 'remove'])
    tmp_H = H.copy()
    if len(tmp_H.edges) != 0:
        if decision == 'add':
            neighbor_edges = []
            if len(G.edges) != len(tmp_H.edges):
                for edge in G.edges:
                    if edge not in H.edges and ((edge.node_a in tmp_H.nodes) or (edge.node_b in tmp_H.nodes)):
                        neighbor_edges.append(edge)
                if len(neighbor_edges) is not 0:
                    new_edge = random.choice(neighbor_edges)
                    tmp_H.add_edge(new_edge, color=G.color[new_edge])
        if decision == 'remove':
            removed_edge = random.choice(tmp_H.edges)
            tmp_H.remove_edge(removed_edge)
    else:
        # If H.edges is empty, initialize it again with one random edge from G.
        neighbor_edges = []
        neighbor_edges.extend(G.edges)
        tmp_H.add_edge(random.choice(neighbor_edges))
return tmp_H

def fast_k_neighbor_sampler(H, G, k):
    '''
    This function returns a k-adjacent subgraph of H.
    '''
    if k == 0:
        return H
    H_prime = modify_one_edge(H, G)
    return fast_k_neighbor_sampler(H_prime,G, k - 1)

