import argparse
from TesasSemble.fastg_graph import fastgs_to_red_blue
from TesasSemble import optim
from TesasSemble import optim_utils

parser = argparse.ArgumentParser(description="Optimize a subgraph of the fastg's passed to this script")

parser.add_argument("--graphs", '-g', dest='graphs', nargs=2)
parser.add_argument("--num-initial-edges", '-n', dest='num_initial_edges', type=int, default=20)

parser.add_argument("--k", '-k', dest='k', type=int, default=1)
parser.add_argument("--alpha", '-a', dest='alpha', type=float, default=0.5)
parser.add_argument("--optim-type", '-o', dest='optim_type', required=True)

args = parser.parse_args()

def main(args):
	""" 
	input: argparse object
	output: returns best_subgraph, best_subgraph_score for one trial of the randomized algorithm chose
	"""
	G = fastgs_to_red_blue(args.graphs[0], args.graphs[1])
	initial_subgraph = optim_utils.i_sample_edges(G, args.num_initial_edges)
	best_subgraph, best_subgraph_score = run_optim(initial_subgraph, G, args)
	return best_subgraph, best_subgraph_score

def run_optim(intial_subgraph, G, args):
	if args.optim_type == 'randomized':
		return optim.randomized_optimal_subgraph(initial_subgraph, G, args.k, args.alpha)
	elif args.optim_type == 'simmulated_annealing':
		return optim.simulated_annealing(initial_subgraph,
										 G,
										 args.alpha,
										 k_neighbors=args.k)
	else:
		raise NotImplementedError('Optimization type not implemented')


main(args)

