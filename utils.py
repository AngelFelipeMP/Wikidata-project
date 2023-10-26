# Data manipulation
import pandas as pd
import random
from icecream import install
install()
from icecream import ic

# Wikipedia API
import wikipedia as wp
from wikipedia.exceptions import DisambiguationError, PageError

# Plotting
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

# Configuration
import config

########################### CRIATING GRAPH ###########################

class RelationshipGenerator():
    """Generates relationships between terms, based on wikipedia links"""
    def __init__(self):
        """Links are directional, start + end, they should also have a weight"""
        self.links = [] # [start, end, weight]

    def scan(self, start=None, repeat=0):
        ##TODO: check if the start exist and/or get the correct title
        """Start scanning from a specific word, or from internal database
        
        Args:
            start (str): the term to start searching from, can be None to let
                algorithm decide where to start
            repeat (int): the number of times to repeat the scan
        """
        while repeat >= 0:

            ##DEBUG
            # should check if start page exists
            # and haven't already scanned
            # if start in [l[0] for l in self.links]:
            if start is not None:
                if start.lower() in [l[0].lower() for l in self.links]:
                    raise Exception("Already scanned")

            term_search = True if start is not None else False

            # If a start isn't defined, we should find one
            if start is None: 
                start = self.find_starting_point()

            # Scan the starting point specified for links
            print(f"Scanning page {start}...")
            try:
                # Fetch the page through the Wikipedia API
                page = wp.page(start)
                ##DEBUG
                start = page.title
                links  = clean_links(list(set(page.links))[-5:])
                ##TODO add a fuction that remove non exiting pages and grab the write title
                # links = list(set(page.links))
                # ignore some uninteresting terms
                links = [l for l in links if not self.ignore_term(l)]


                # Add links to database
                link_weights = []
                for link in links:
                    weight = self.weight_link(page, link)
                    link_weights.append(weight)
                
                link_weights = [w / max(link_weights) for w in link_weights]

                ##DEBUG
                # total_nodes_before_interation = set([n[1] for n in self.links])
                total_nodes_before_interation = set([l[1] for l in self.links] + [l[0] for l in self.links])
                for i, link in enumerate(links):
                    ##DEBUG
                    # self.links.append([start, link.lower(), link_weights[i] + 2 * int(term_search)]) # 3 works pretty well
                    self.links.append([start, link, link_weights[i] + 2 * int(term_search)]) # 3 works pretty well

                # Print some data to the user on progress
                explored_nodes = set([l[0] for l in self.links])
                explored_nodes_count = len(explored_nodes)
                ##TODO fix how we caculate total_nodels
                # total_nodes = set([l[1] for l in self.links])
                total_nodes = set([l[1] for l in self.links] + [l[0] for l in self.links]) 
                total_nodes_count = len(total_nodes)
                # ##DEBUG
                # new_nodes = [l.lower() for l in links if l not in total_nodes]
                new_nodes = [l for l in links if l not in total_nodes_before_interation]
                new_nodes_count = len(new_nodes)
                print(f"New nodes added: {new_nodes_count}, Total Nodes: {total_nodes_count}, Explored Nodes: {explored_nodes_count}")

            except (DisambiguationError, PageError):
                # This happens if the page has disambiguation or doesn't exist
                # We just ignore the page for now, could improve this
                self.links.append([start, "DISAMBIGUATION", 0])

            repeat -= 1
            start = None
        
    def find_starting_point(self):
        """Find the best place to start when no input is given"""
        # Need some links to work with.
        if len(self.links) == 0:
            raise Exception("Unable to start, no start defined or existing links")
                
        # Get top terms
        res = self.rank_terms()
        sorted_links = list(zip(res.index, res.values))
        all_starts = set([l[0] for l in self.links])

        # Remove identifiers (these are on many Wikipedia pages)
        all_starts = [l for l in all_starts if '(identifier)' not in l]
        
        # print(sorted_links[:10])
        # Iterate over the top links, until we find a new one
        for i in range(len(sorted_links)):
            if sorted_links[i][0] not in all_starts and len(sorted_links[i][0]) > 0:
                return sorted_links[i][0]
        
        # no link found
        raise Exception("No starting point found within links")
        return

    @staticmethod
    def weight_link(page, link):
        """Weight an outgoing link for a given source page
        
        Args:
            page (obj): 
            link (str): the outgoing link of interest
        
        Returns:
            (float): the weight, between 0 and 1
        """
        weight = 0.1
        
        link_counts = page.content.lower().count(link.lower())
        weight += link_counts
        
        if link.lower() in page.summary.lower():
            weight += 3
        
        return weight


    def get_database(self):
        return sorted(self.links, key=lambda x: -x[2])


    def rank_terms(self, with_start=False):
        # We can use graph theory here!
        # tws = [l[1:] for l in self.links]
        df = pd.DataFrame(self.links, columns=["start", "end", "weight"])

        if with_start:
            df = df.append(df.rename(columns={"end": "start", "start":"end"}))
        
        return df.groupby("end").weight.sum().sort_values(ascending=False)
    
    def get_key_terms(self, n=20):
        return "'" + "', '".join([t for t in self.rank_terms().head(n).index.tolist() if "(identifier)" not in t]) + "'"

    @staticmethod
    def ignore_term(term):
        """List of terms to ignore"""
        if "(identifier)" in term or term == "doi":
            return True
        return False

########################### LINKS VERIFICATION #######################
def clean_links(links):
    """
    i) Remove links that don't connect to a WP page
    ii) Get link title with correct case and spelling
    """
    links_cleaned = set()
    
    for l in tqdm(links):
        try:
            page = wp.page(l)
            links_cleaned.add(page.title)

        except (DisambiguationError, PageError):
            pass
        
    return list(links_cleaned)


########################### SIMPLIFY GRAPH ###########################

def simplify_graph(rg, max_nodes=1000, huge_data=False):
    """Simplify a graph which has many nodes
    
    Remove items with low total weights
    This is an alterantive to restricted_view in networkx.
    
    Args:
        rg (RelationshipGenerator): object containing knowledge graph
        max_nodes (float): the number of nodes to search, or percentage of nodes
            to keep
    
    Returns:
        (RelationshipGenerator): simplified knowledge graph
    """
    # Get most interesting terms.
    nodes = rg.rank_terms()

    # Get nodes to keep
    if max_nodes >= 1:
        keep_nodes = nodes.head(max_nodes).index.tolist()
    elif max_nodes >= 0:
        keep_nodes = nodes.head(int(max_nodes * len(nodes))).index.tolist()
    
    # Filter list of nodes so that there are no nodes outside those of interest
    filtered_links = list(filter(lambda x: x[1] in keep_nodes, rg.links))
    
    if huge_data:
        # Filter adequeted for huge graphs
        filtered_links = list(filter(lambda x: x[0] in keep_nodes, filtered_links))

    # Define a new object and define its dictionary
    ac = RelationshipGenerator()
    ac.links = filtered_links

    return ac



########################### PLOT GRAPH ###########################

def remove_self_references(l):
    return [i for i in l if i[0]!=i[1]]

def add_focus_point(links, focus="on me", focus_factor=3):
    for i, link in enumerate(links):
        if not (focus in link[0] or focus in link[1]):
            links[i] = [link[0], link[1], link[2] / focus_factor]
        else:
            links[i] = [link[0], link[1], link[2] * focus_factor]

    return links

def create_graph(rg, focus=None, figure_name="my_plot.png"):

    links = rg.links
    links = remove_self_references(links)
    if focus is not None:
        links = add_focus_point(links, focus)
    
    node_data = rg.rank_terms()
    nodes = node_data.index.tolist()
    node_weights = node_data.values.tolist()
    node_weights = [nw * 100 for nw in node_weights]
    nodelist = nodes


    G = nx.DiGraph() # MultiGraph()

    # G.add_node()
    G.add_nodes_from(nodes)

    # Add edges
    G.add_weighted_edges_from(links)
    
    pos = nx.spring_layout(G, k=1, seed=7)  # positions for all nodes - seed for reproducibility

    fig = plt.figure(figsize=(12,12))

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=nodelist,
        node_size=node_weights,
        node_color='lightblue',
        alpha=0.7
    )

    widths = nx.get_edge_attributes(G, 'weight')    
    nx.draw_networkx_edges(
        G, pos,
        edgelist = widths.keys(),
        width=list(widths.values()),
        edge_color='lightblue',
        alpha=0.6
    )

    nx.draw_networkx_labels(G, pos=pos,
                            labels=dict(zip(nodelist,nodelist)),
                            font_color='black')

    """nx.draw(
        G,
        nodelist=nodes,
        node_size=node_weights,
        with_labels=True,
    )
"""
    # plt.box(False)
    # plt.show()
    plt.savefig(config.LOGS_PATH + '/'+ figure_name)


########################### SUMMARIZATION ###########################

def simplified_plot(rg_links=[], topiz=["tests"], depth=20, max_size=20, huge_data=False):

    rg = RelationshipGenerator()
    
    if len(rg_links) > 0:
        rg.links = rg_links
    else:
        for topic in topics:
            rg.scan(topic)
            rg.scan(repeat=depth)

    print(f"Created {len(rg.links)} links with {rg.rank_terms().shape[0]} nodes.")

    ng = simplify_graph(rg=rg, max_nodes=max_size, huge_data=huge_data) 
    
    fig = create_graph(ng)

    plt.show()

    return rg