import config
import pandas as pd
from utils import RelationshipGenerator
import warnings
warnings.filterwarnings("ignore")


    
if __name__ == "__main__":
    #Load graph from a  csv file
    df = pd.read_csv(config.LOGS_PATH + '/' + 'links.csv')
    rg = RelationshipGenerator()
    rg.links = df.values.tolist()
    
    # add specific terms/wp pages
    # rg.scan("Public policy")
    # rg.scan("Cultural policy")
    # rg.scan("Economic policy")
    # rg.scan("Education policy")
    # rg.scan("Energy policy")
    # rg.scan("Environmental policy")
    # rg.scan("Foreign policy")
    # rg.scan("Health policy")
    # rg.scan("Immigration policy")
    # rg.scan("Social policy")

    # branching
    # rg.scan(repeat=10) ##depth
    rg.scan(repeat=8) ##depth 
    
    df = pd.DataFrame(rg.links, columns=["start", "end", "weight"])
    print(f'Number of mean nodes: {len(df["start"].unique())}')
    
    #Overall graph information
    print(f"The graph has {rg.rank_terms().shape[0]} terms and {len(rg.links)} connections.")