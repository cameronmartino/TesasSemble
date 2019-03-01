import TesasSemble.optim_utils as optim_utils
import TesasSemble.sim_annealing_utils as sa_utils
import math
import random

def simulated_annealing(H,
                        G,
                        alpha,
                        k_neighbors = 3,
                        T = 40,
                        Tmin = 0,
                        T_tol = 1e-5,
                        n = 100,
                        gamma = 0.85,
                        sampling_decision = 'fast'):
    '''Simulated Annealing to perform an optimization to obtain a subgraph H from graph G.'''

    best_H = H
    best_score = best_H.score(alpha)

    while T > Tmin + T_tol:
        for i in range(n):
            if sampling_decision == 'fast':
                new_H = sa_utils.fast_k_neighbor_sampler(best_H, G, k_neighbors)
            # TODO implement random sampling from adjacent_graph
            #elif sampling_decision == 'k_adjacent':
            #    new_H = best_H.adjacent_graph(best_H, G, k_neighbors)
            else:
                print('Invalid "sampling_decision"')
                return None

            new_H_score = new_H.score(alpha)
            delta = best_score - new_H_score
            prob = math.exp(-delta / T)
            if delta < 0:
                best_H = new_H
                best_score = new_H_score
                break
            elif random.random() < prob:
                best_H = new_H
                best_score = new_H_score
                break

        T = gamma * T   # Geometric decrease of temperature

    return best_H, best_score
