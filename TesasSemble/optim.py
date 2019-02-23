import graph
import optim_utils

def randomized_optimal_subgraph(G, i, k, alpha):
    H = i_sample_edges(G, i)
    best_H = None
    best_score = 0
    while best_H != H:
        best_H = H
        H_score = H.score(alpha)
        for H_prime in H.neighbor_graphs(G, k):
            H_prime_score = H_prime.score(alpha)
            if H_prime_score > H_score:
                best_addition = H_prime
                best_score = H_prime_score
    return best_addition, best_score

