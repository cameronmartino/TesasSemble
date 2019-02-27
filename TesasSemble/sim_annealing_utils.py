import random

def initial_subgraph(G):
    '''Pick a random connected subgraph.'''
    pass


def modify_one_edge(G, H):
    # decide if add or remove
    decision = random.choice(['add', 'remove'])
    tmp_H = H.copy()
    if decision == 'add':
        neighbor_edges = []
        for edge in G.edges:
            if edge not in H.edges and (edge.node_a in tmp_H.nodes or edge.node_b in tmp_H.nodes):
                neighbor_edges.append(edge)
        new_edge = random.choice(neighbor_edges)
        tmp_H.add_edge(new_edge)
    if decision == 'remove':
        removed_edge = random.choice(tmp_H.edges)
        tmp_H.remove_edge(removed_edge)
    return tmp_H


def fast_k_neighbor_sampler(G, H, k):
    '''
    This function returns a k-adjacent subgraph of H.
    '''
    if k == 0:
        return H
    H_prime = modify_one_edge(G, H)
    fast_k_neighbor_sampler(G, H_prime, k - 1)