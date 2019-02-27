from sim_annealing_utils import *
from optim_utils import *
import math
import random

def simulated_annealing(G,
                        alpha,
                        k_neighbors = 3,
                        T = 40,
                        Tmin = 0,
                        T_tol = 1e-5,
                        n = 100,
                        gamma = 0.5,
                        graph_percentage = 0.5,
                        sampling_decision = 'fast'):
    '''Simulated Annealing to perform an optimization to obtain a subgraph H from graph G.'''

    best_H = i_sample_edges(G, int(graph_percentage * len(G.edges)))
    best_score = best_H.score(alpha)

    while T > Tmin + T_tol:
        for i in range(n):
            if sampling_decision == 'fast':
                H = fast_k_neighbor_sampler(G, best_H, k_neighbors)
            elif sampling_decision == 'k_adjacent':
                #H = best_H.adjacent_graph(best_H, G, k_neighbors)
                H = fast_k_neighbor_sampler(G, best_H, k_neighbors)
            else:
                print('Invalid "sampling_decision"')
                return None

            H_score = H.score(alpha)
            delta = best_score - H_score
            prob = math.exp(-delta / T)
            if delta < 0:
                best_H = H
                best_score = H_score
                break
            elif random.random() < prob:
                best_H = H
                best_score = H_score
                break

        T = gamma * T   # Geometric decrease of temperature

    return best_H
