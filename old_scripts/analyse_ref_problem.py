from config import *
import pandas as pd
from icecream import ic
import numpy as np
from references_old import save_to_csv as save_to_csv_ref_list
from extract_refs import save_to_csv as save_to_csv_ref_template

import requests
import re
import csv
import html

def get_unique_items(file, column):
    df= pd.read_csv(LOGS_PATH + '/' + file, usecols=[column])
    df = df.dropna() 
    return df[column].unique()

if __name__ == "__main__":
    
    ### Get unique values from the three files
    wike_pages = get_unique_items(file='Wikipedia-links-plus-QID-27-Oct-2023-final-list-14-Nov-2023.csv',
                                    column='Page')
    ref_list = get_unique_items(file='references_sent_Amanda_18-11-2023.csv',
                                    column='Page Title')
    ref_template = get_unique_items(file='References-processed-v2.csv',
                                    column='Page')
    
    ### fetch the missing items ref list and ref template
    missing_items_ref_list = np.setdiff1d(wike_pages[:1000], ref_list)
    missing_items_ref_template = np.setdiff1d(wike_pages[:1000], ref_template)
    # # Save the array to a CSV file
    # np.savetxt(LOGS_PATH + "/missing_items_ref_list.csv", missing_items_ref_list, delimiter=",", fmt="%s")
    # np.savetxt(LOGS_PATH + "/missing_items_ref_template.csv", missing_items_ref_template, delimiter=",", fmt="%s")
    
    # ### fetch the NOT-FOUND-PAGE ref list wp and file trying to get the references
    # df_not_found_wp_ref_list = pd.read_csv(LOGS_PATH + '/' + 'references_sent_Amanda_18-11-2023.csv')
    # df_not_found_wp_ref_list = df_not_found_wp_ref_list[df_not_found_wp_ref_list['Reference'].str.contains('NOT-FOUND-PAGE')]
    # np.savetxt(LOGS_PATH + "/NOT-FOUND-PAGE_ref_list.csv", df_not_found_wp_ref_list['Page Title'].unique(), delimiter=",", fmt="%s")
    # save_to_csv_ref_list(df_not_found_wp_ref_list['Page Title'].unique(), filename='NOT-FOUND-PAGE_ref_list_try_to_find.csv')
    
    # ##COMMENT: I may remove the code below
    # ##Check how the code would performer after fix references_old.py
    # df = pd.read_csv(LOGS_PATH + '/' + 'Wikipedia-links-plus-QID-27-Oct-2023-final-list-14-Nov-2023.csv',
    #                     usecols=['Page'])
    # df = df.dropna()  
    # df = df.iloc[:1000]
    # df = df[df['Page'].isin(missing_items_ref_list)]
    # save_to_csv_ref_list(df['Page'].unique()[:1000], filename='missing_wp_ref_list.csv')
    
    path_file = LOGS_PATH + '/Reference_extration_problem_analyses/missing_wp_ref_template_unknown_reason.csv'
    path_folder = LOGS_PATH + '/Reference_extration_problem_analyses/ref_list_unknown_missing'
    df = pd.read_csv(path_file, usecols=['Page Title'])
    
    for page_title in df['Page Title'].unique():
        page_title = page_title.replace(' ', '_')
        
        # Replace with the specific Wikipedia article edit URL
        edit_url = f'https://en.wikipedia.org/w/index.php?title={page_title}&action=edit'

        # Fetch the content of the edit page
        response = requests.get(edit_url)
        edit_page_content = html.unescape(response.text)
        with open(path_folder + '/' + page_title + '_html_to_inspect.txt', 'w') as f:
            f.write(edit_page_content)
            
        print(f'Page {page_title} saved')
        
    print('Done')