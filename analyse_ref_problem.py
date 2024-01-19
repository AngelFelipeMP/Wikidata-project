from config import *
import pandas as pd
from icecream import ic
import numpy as np
from references_old import save_to_csv as save_to_csv_ref_list
from extract_refs import save_to_csv as save_to_csv_ref_template
def get_unique_items(file, column):
    df= pd.read_csv(LOGS_PATH + '/' + file, usecols=[column])
    df = df.dropna() 
    return df[column].unique()

if __name__ == "__main__":
    
    wike_pages = get_unique_items(file='Wikipedia-links-plus-QID-27-Oct-2023-final-list-14-Nov-2023.csv',
                                    column='Page')
    ref_list = get_unique_items(file='references_sent_Amanda_18-11-2023.csv',
                                    column='Page Title')
    ref_template = get_unique_items(file='References-processed-v2.csv',
                                    column='Page')
    missing_items_ref_list = np.setdiff1d(wike_pages[:1000], ref_list)
    missing_items_ref_template = np.setdiff1d(wike_pages[:1000], ref_template)
    
    # Save the array to a CSV file
    np.savetxt(LOGS_PATH + "/missing_items_ref_list.csv", missing_items_ref_list, delimiter=",", fmt="%s")
    np.savetxt(LOGS_PATH + "/missing_items_ref_template.csv", missing_items_ref_template, delimiter=",", fmt="%s")
    
    df_not_found_wp_ref_list = pd.read_csv(LOGS_PATH + '/' + 'references_sent_Amanda_18-11-2023.csv')
    df_not_found_wp_ref_list = df_not_found_wp_ref_list[df_not_found_wp_ref_list['Reference'].str.contains('NOT-FOUND-PAGE')]
    np.savetxt(LOGS_PATH + "/NOT-FOUND-PAGE_ref_list.csv", df_not_found_wp_ref_list['Page Title'].unique(), delimiter=",", fmt="%s")
    save_to_csv_ref_list(df_not_found_wp_ref_list['Page Title'].unique(), filename='NOT-FOUND-PAGE_ref_list_try_to_find.csv')
    
    
    # #Load graph from a  csv file
    # df = pd.read_csv(LOGS_PATH + '/' + 'Wikipedia-links-plus-QID-27-Oct-2023-final-list-14-Nov-2023.csv',
    #                     usecols=['Page'])
    # df = df.dropna()  
    # df = df.iloc[:1000]
    # df = df[df['Page'].isin(missing_items_ref_list)]
    # save_to_csv_ref_list(df['Page'].unique()[:1000], filename='missing_wp_ref_list.csv')
    
    
    ##DEBUG: Investigate Why I am geting NOT-FOUND-PAGE
    ##TODO: Why ref_template is missing many fereences? 