import random

def initial_subgraph(G):
    '''Pick a random connected subgraph.'''
    pass


def modify_one_edge(G, H):
    # decide if add or remove
    decision = random.choice(['add', 'remove'])
    tmp_H = H.copy()    # TODO include a deep copy method for DiGraphs
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


def k_adjacent_subgraph(G, H, k, decision = 'one'):
    '''
    This function returns a k-adjacent subgraph of H.
    'decision' could be one at the time ('one') or uniformly pick among all k-adjacent graphs ('uniform').
    '''
    if k == 0:
        return H
    if decision == 'one':
        H_prime = modify_one_edge(G, H)
    elif decision == 'uniform':
        k_neighbors = []    # TODO implement George's method to generate all k-neighbors
        H_prime = random.choice(k_neighbors)
    else:
        return None
    k_adjacent_subgraph(G, H_prime, k-1, decision)