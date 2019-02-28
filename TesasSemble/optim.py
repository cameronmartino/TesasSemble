import TesasSemble.optim_utils as optim_utils

def randomized_optimal_subgraph(G, i, k, alpha):
    H = optim_utils.i_sample_edges(G, i)
    best_H = None
    best_score = 0
    while best_H != H:
        best_H = H
        H_score = H.score(alpha)
        for H_prime in H.neighbor_graphs(H, G, k):
            H_prime_score = H_prime.score(alpha)
            if H_prime_score > H_score:
                best_H = H_prime
                best_score = H_prime_score
    return best_H, best_score

