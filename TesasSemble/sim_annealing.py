import sim_annealing_utils
import optim_utils
import math
import random

def simulated_annealing(G, alpha, k_neighbors = 3, T = 40, Tmin = 0, n = 100, gamma = 0.5, sampling_decision = 'one'):
    '''Simulated Annealing to perform an optimization to obtain a subgraph H from graph G.'''

    best_H = initial_subgraph(G)
    best_score = best_H.score(alpha)

    while T > Tmin:
        for i in range(n):
            H = k_adjacent_subgraph(G, best_H, k_neighbors, decision=sampling_decision)
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
