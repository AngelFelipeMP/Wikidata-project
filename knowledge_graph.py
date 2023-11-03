# Data manipulation
import pandas as pd
# Plotting
import networkx as nx
import matplotlib.pyplot as plt

import argparse
import config
from utils import RelationshipGenerator, simplify_graph, plot_graph, simplified_plot
import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wp", action='append', type=str, help="Enter Wikipedia page(s) to create your graph")
    parser.add_argument("--branch", type=int, default=False, help="Enter number of extra branchs")
    parser.add_argument("--path", type=str, default=False, help="Give full path to save files")
    parser.add_argument("--official", action='store_true', default=False, help="Create a graph using the offical Wikipedia project parameters")
    parser.add_argument("--plot", action='store_true', default=False, help="Generate a visualization of the graph")
    args = parser.parse_args()
    
    # verification: use official or given parameters
    if args.official and (args.branch or args.wp==[]):
        print('The flag --offical incompatible with --wp and --brach')
        exit(1)
    
    # verification: get path to save files
    if not args.path and args.official:
        files_path = config.LOGS_PATH + '/' + 'links.csv'
    elif not args.path:
        files_path = config.CODE_PATH + '/' + 'links.csv'
    else: 
        files_path = args.path
    
    # verification: get wp to start the graph
    if args.official:
        list_wp = config.START_WP
    elif args.wp:
        list_wp = list(set(args.wp))
    else:
        print('Add Wikipedia page title to start the graph using the flag --wp <PAGE TILE>')
        exit(1)
            
    # verification: number of interation for branching graph
    if args.official:
        n_branch = config.N_BRANCH
    elif args.branch:
        n_branch = args.branch 
    
    #Create a relationship generator
    rg = RelationshipGenerator(graph_path=files_path)
    for wp in list_wp:
        rg.scan(wp)
        
    #Brach the graph
    if args.official:
        rg.scan(repeat=config.N_BRANCH) ##depth
    elif args.branch:
        rg.scan(repeat=args.branch) ##depth
        
    #Overall graph information
    print(f"The graph has {rg.rank_terms().shape[0]} terms and {len(rg.links)} connections.")
        
    #Plot the simplified version of the graph
    if args.plot:
        #Load graph from a  csv file
        ng = simplify_graph(rg=rg, max_nodes=20)
        path_plot = '/'.join(files_path.split('/')[:-1]) + '/' + 'plot_simplified_graph.png'
        plot_graph(rg, figure_path=path_plot)