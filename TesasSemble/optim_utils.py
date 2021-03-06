import random
import TesasSemble.graph as graph

# TODO implement graph sampling techniques


def i_sample_edges(Graph, i):
    edge_list = [edge for edge in Graph.edges if Graph.color[edge] == 'red']
    random.shuffle(edge_list)
    sampled_edges = edge_list[:i]
    H = graph.RedBlueDiGraph()
    H.add_edges_from(sampled_edges, [Graph.color[edge] for edge in sampled_edges])
    return H


def graph_from_fraction_edges(Graph, percentage = 20):
    edge_list = [edge for edge in Graph.edges if Graph.color[edge] == 'red']
    random.shuffle(edge_list)
    H = graph.RedBlueDiGraph()

    min_number = int(percentage * len(edge_list) / 100)
    if min_number < 1:
        min_number = 1

    new_edge = edge_list.pop(0)
    add_more = True
    while (len(H.edges) < min_number) and (len(edge_list) != 0) and (add_more == True):
        H.add_edge(new_edge, color=Graph.color[new_edge])
        add_more = False
        for edge in edge_list:
            if edge not in H.edges and ((edge.node_a in H.nodes) or (edge.node_b in H.nodes)):
                new_edge = edge
                edge_list.remove(edge)
                random.shuffle(edge_list)
                add_more = True
                break
    return H


def modify_one_edge(H, G):
    # decide if add or remove
    decision = random.choice(['add', 'remove'])
    tmp_H = H.copy()
    if len(tmp_H.edges) != 0:
        if decision == 'add':
            neighbor_edges = []
            if len(G.edges) > len(tmp_H.edges):
                for edge in G.edges:
                    if edge not in H.edges and (
                        (edge.node_a in tmp_H.nodes) or (
                            edge.node_b in tmp_H.nodes)):
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
        new_edge = random.choice(neighbor_edges)
        tmp_H.add_edge(new_edge, color=G.color[new_edge])
    return tmp_H


def fast_k_neighbor_sampler(H, G, k):
    '''
    This function returns a k-adjacent subgraph of H.
    '''
    if k == 0:
        return H
    H_prime = modify_one_edge(H, G)
    return fast_k_neighbor_sampler(H_prime, G, k - 1)
