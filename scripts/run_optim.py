import os
import argparse
import pickle
import json
from TesasSemble.preprocessing import GraphConstructor
from TesasSemble import optim
from TesasSemble import optim_utils
from TesasSemble.contig_assembly import contig_assembly

parser = argparse.ArgumentParser(description="Optimize a subgraph of the fastg's passed to this script")

parser.add_argument("--files", '-f', dest='files', nargs='+', help='file paths for all fastq files')
parser.add_argument("--num-initial-edges", '-e', dest='num_initial_edges', type=int, default=20)
parser.add_argument("--k", '-k', dest='k', type=int, default=1, help='k for k-neighbors')
parser.add_argument("--alpha", '-a', dest='alpha', type=float, default=0.5)
parser.add_argument("--optim-type", '-o', dest='optim_type', required=True)
parser.add_argument("--output-dir", '-d', dest='output_dir', required=True, help="directory that output can be written to", default=os.curdir)
parser.add_argument("--read-length", '-r', dest='read_length', required=True, help="length of reads in fastqs", type=int)
parser.add_argument("--num-iter", "-n", dest='num_iter', type=int, default=100)
parser.add_argument("--temperature", "-T", dest='temperature', type=float, default=40)
parser.add_argument("--gamma", "-g", dest='gamma', type=float, default=0.85)
parser.add_argument("--initialization", "-i", dest='initialization', type=str, default='number')
parser.add_argument("--function", "-fn", dest='function', type=str, default='original')

args = parser.parse_args()

def main(args):
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    Graphs = GraphConstructor(k=args.read_length)
    Graphs.fit(args.files)
    node_map = Graphs.node_map()
    node_map_file = os.path.join(args.output_dir, 'node_map.js')
    with open(node_map_file, 'w') as fp:
        json.dump(node_map, fp)
    for i, graph in enumerate(args.files):
        G_RdBu = Graphs.condition_graph(graph)
        print('Starting optimization for condition {}. Graph size: {} edges'.format(i, len(G_RdBu.edges)))
        #print([len(path) for path in G_RdBu.maximal_non_branching_paths()])
        best_subgraph, best_subgraph_score = single_condition_best_graph(G_RdBu, args)
        paths = best_subgraph.maximal_non_branching_paths()
        print('Condition {} finished. Score: {}. Path Lengths: {}'.format(i, best_subgraph_score, 
            [len(path) for path in paths]))

        #graph_pickle_file = os.path.join(args.output_dir, 'graph_{}.p'.format(i))
        #with open(graph_pickle_file, 'wb') as fp:
        #   pickle.dump(best_subgraph, fp)

        contigs = contig_assembly(best_subgraph, node_map)
        contig_file = os.path.join(args.output_dir, 'contigs_{}.txt'.format(i))
        with open(contig_file, 'w') as fp:
            fp.write('\n'.join(contigs))
        print('Contigs written to file {}'.format(contig_file))

    return True


def single_condition_best_graph(G, args):
    """ 
    input: graph to optimize, and argparse object
    output: returns best_subgraph, best_subgraph_score for one trial of the randomized algorithm chose
    """
    if args.initialization != 'fraction':
        initial_subgraph = optim_utils.i_sample_edges(G, args.num_initial_edges)
    else:
        initial_subgraph = optim_utils.graph_from_fraction_edges(G, percentage=args.num_initial_edges)

    best_subgraph, best_subgraph_score = run_optim(initial_subgraph, G, args)
    return best_subgraph, best_subgraph_score


def run_optim(initial_subgraph, G, args):
    if args.optim_type == 'randomized':
        return optim.randomized_optimal_subgraph(initial_subgraph, G, args.k, args.alpha)
    elif args.optim_type == 'simulated_annealing':
        return optim.simulated_annealing(initial_subgraph,
                                         G,
                                         args.alpha,
                                         n=args.num_iter,
                                         T=args.temperature,
                                         gamma=args.gamma,
                                         k_neighbors=args.k,
                                         objective_fn=args.function)
    else:
        raise NotImplementedError('Optimization type not implemented')


main(args)

