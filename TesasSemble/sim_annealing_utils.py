def modify_one_edge(H):
    # decide if add or remove
    pass

def k_adj(H, k):
    if k == 0:
        return H

    H_prime = modify_one_edge(H)

    return k_adj(H_prime, k-1)