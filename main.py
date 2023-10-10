# Data manipulation
import pandas as pd

# Plotting
import networkx as nx
import matplotlib.pyplot as plt

from utils import RelationshipGenerator, simplify_graph, create_graph, simplified_plot

import config
    
if __name__ == "__main__":
    
    #Create a relationship generator
    rg = RelationshipGenerator()
    rg.scan("Public Policy")
    rg.scan("Cultural policy")
    rg.scan("Economic Policy")
    rg.scan("Education policy")
    rg.scan("Energy policy")
    rg.scan("Environmental Policy")
    rg.scan("Foreign policy")
    rg.scan("Health Policy")
    rg.scan("Immigration policy")
    rg.scan("Social Policy")

    rg.scan(repeat=10) ##depth 
    
    # #Save graph in a  csv file
    df = pd.DataFrame(rg.links, columns=["start", "end", "weight"])
    df.to_csv(config.LOGS_PATH + '/' + 'links.csv', index=False)
    
    #Load graph from a  csv file
    df = pd.read_csv(config.LOGS_PATH + '/' + 'links.csv')
    rg = RelationshipGenerator()
    rg.links = df.values.tolist()
    
    #Overall graph information
    print(f"The graph has {rg.rank_terms().shape[0]} terms and {len(rg.links)} connections.")
    
    #Save simplified graph in a  csv file
    simplify_rg = simplify_graph(rg=rg, max_nodes=20, huge_data=False) 
    simplify_df = pd.DataFrame(simplify_rg.links, columns=["start", "end", "weight"])
    simplify_df.to_csv(config.LOGS_PATH + '/' + 'simplified_links.csv', index=False)
    
    #Plot graph
    create_graph(rg=simplify_rg, focus=None, figure_name='simplified_graph.png') 
    create_graph(rg=simplify_rg, focus='Public Policy', figure_name='simplified_graph_with_focus.png')
    
    
    # #Plot graph with simplified_plot function
    # tg = simplified_plot(rg_links=df.values.tolist(), topics=['Public Policy'], depth=1, max_size=20, huge_data=False)
    