import sim_annealing_utils

def simulated_annealing(G, T = 40, Tmin = 0, iterations = 100, gamma = 0.5):
    '''Simulated Annealing to perform optimization of subgraph H of G.'''
    while T > Tmin:




        T = gamma * T
