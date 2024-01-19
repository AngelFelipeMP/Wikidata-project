# Wikipedia API
#Pip install lxml
import wikipedia as wp
from bs4 import BeautifulSoup
from config import *
import pandas as pd
from icecream import ic
from tqdm import tqdm

import requests
import re
import csv
import html

def save_to_csv(titles, filename='output.csv'):
    """
    Save the titles and references to a CSV.
    """
    with open(LOGS_PATH + '/' + filename, 'w', newline='', encoding='utf-8') as file:
        # writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\')
        writer = csv.writer(file)
        writer.writerow(["Page Title", "Reference"])
        
        for title in tqdm(titles):
            references = get_ref(title)
            for ref in references:
                writer.writerow([title, ref])
            tqdm.write(f"References for {title} saved.")
        tqdm.write(f"CSV file saved as {filename}")
        
        
def get_ref(page_title):
    try:
        page_title = page_title.replace(' ', '_')
        
        # Replace with the specific Wikipedia article edit URL
        edit_url = f'https://en.wikipedia.org/w/index.php?title={page_title}&action=edit'

        # Fetch the content of the edit page
        response = requests.get(edit_url)
        edit_page_content = html.unescape(response.text)
        
        # Use regular expressions to find references in the specified format
        # pattern = r'<ref>.*?</ref>'
        # pattern = r'<ref(?:\sname="[^"]*")?>{{[Cc]it.*?}}</ref>'
        pattern = r'<ref(?:\sname="[^"]*")?>{{[Cc]it.*?}}'
        references = re.findall(pattern, edit_page_content, re.DOTALL)
        references = [ ref.replace("\n", "") for ref in references]
        
        if not references:
            return ['NOT-FOUND-RERERENCES']
        return references
    except:
        # print(f"References for {page_title} not found.")
        tqdm.write(f"References for {page_title} not found.")
        return ['NOT-FOUND-PAGE']

if __name__ == "__main__":
    #Load graph from a  csv file
    df = pd.read_csv(LOGS_PATH + '/' + 'Wikipedia-links-plus-QID-27-Oct-2023-final-list-14-Nov-2023.csv',
                        usecols=['Page'])
    df = df.dropna()  
    ##COMMENT: get referenecs for the top 1000 pages
    save_to_csv(df['Page'].unique()[:1000], filename='references_ref_list.csv')
