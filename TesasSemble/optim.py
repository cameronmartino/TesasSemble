import TesasSemble.optim_utils as optim_utils
import TesasSemble.graph as graph

def randomized_optimal_subgraph(H, G, k, alpha):
    best_H = H 
    flag = True
    best_score = best_H.score(alpha)
    while best_H != H or flag:
        H = best_H
        H_score = H.score(alpha)
        for H_prime in H.neighbor_graphs(H, G, k):
            H_prime_score = H_prime.score(alpha)
            if H_prime_score > H_score:
                best_H = H_prime
                best_score = H_prime_score
        flag = False

    return best_H, best_score

