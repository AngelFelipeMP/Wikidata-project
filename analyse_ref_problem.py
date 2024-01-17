from config import *
import pandas as pd
from icecream import ic

def get_unique_items(file, column):
    df= pd.read_csv(LOGS_PATH + '/' + file, usecols=[column])
    return df[column].unique()

if __name__ == "__main__":
    
    wike_pages = get_unique_items(file='Wikipedia-links-plus-QID-27-Oct-2023-final-list-14-Nov-2023.csv',
                                    column='Page')
    
    ref_list = get_unique_items(file='references_sent_Amanda_18-11-2023.csv',
                                    column='Page Title')
    
    ref_template = get_unique_items(file='References-processed-v2.csv',
                                    column='Page')
    

    ic(len(wike_pages))
    ic(len(ref_list))
    ic(len(ref_template))