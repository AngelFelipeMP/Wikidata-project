# Wikipedia API
import wikipedia as wp
import csv
from bs4 import BeautifulSoup
from config import *
import pandas as pd
from icecream import ic
from tqdm import tqdm

def get_references(page_title):
    """
    Get references from the given Wikipedia page.
    """
    try:
        page = wp.page(page_title)
        soup = BeautifulSoup(page.html(), 'html.parser')
        # citations = soup.find_all('cite')
        citations = soup.find_all('li', id=lambda x: x and x.startswith('cite_note-'))
        
        if not citations:
            return ['NOT-FOUND-RERERENCES']
        return citations
    except:
        # print(f"References for {page_title} not found.")
        tqdm.write(f"References for {page_title} not found.")
        return ['NOT-FOUND-PAGE']
    


def save_to_csv(titles, filename='output.csv'):
    """
    Save the titles and references to a CSV.
    """
    with open(LOGS_PATH + '/' + filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Page Title", "Reference"])
        
        for title in tqdm(titles):
            references = get_references(title)
            for ref in references:
                writer.writerow([title, ref])
            # print(f"References for {title} saved.")
            tqdm.write(f"References for {title} saved.")

        # print(f"CSV file saved as {filename}")
        tqdm.write(f"CSV file saved as {filename}")
        
def has_duplicates(lst):
    return len(lst) != len(set(lst))


if __name__ == "__main__":
    #Load graph from a  csv file
    df = pd.read_csv(LOGS_PATH + '/' + 'Wikipedia-links-plus-QID-27-Oct-2023-final-list-14-Nov-2023.csv',
                        usecols=['Page'])
    df = df.dropna()  
    # all_unique_pages = pd.concat([df['start'].str.lower(), df['end'].str.lower()]).unique()
    ##COMMENT: get referenecs for the top 10 pages
    save_to_csv(df['Page'].unique()[:1000], filename='references_ref_list.csv')