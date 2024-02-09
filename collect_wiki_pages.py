from config import *
import pandas as pd
from icecream import ic
from tqdm import tqdm
from datetime import datetime
import requests
import json
import csv
import sys
import os 

def wiki_web_crawler(wiki_pages):
        for page in tqdm(wiki_pages):
            page_title = page.replace(' ', '_')
            page_text = request_wiki_page(page_title)
            
            if "errorKey" not in page_text:
                save_wiki_page(page_title, page_text)
            
            
def save_wiki_page(page_title, page_text):
    with open(WIKI_PAGES + '/' + page_title + '.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(page_text, ensure_ascii=False, indent=4))

def save_not_fund_pages(page, error):
    with open(WIKI_PAGES + '/' + 'not_found_wiki_pages' + '.csv', 'a+', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([page, error])
    
def request_wiki_page(page_title):
    try:
        url = 'https://api.wikimedia.org/core/v1/wikipedia/en/page/' + page_title
        response = requests.get(url)
        wiki_json = response.json()
        
        if "errorKey" in wiki_json:
            save_not_fund_pages(page_title, wiki_json)
        return wiki_json
        
    except Exception as e:
        # Capture the error message
        error_type, error_value, error_traceback = sys.exc_info()
        error_message = f"{error_type.__name__}: {error_value}"
        error_message = str(e)
        save_not_fund_pages(page_title, error_message)
            
        return {"errorKey": None}
    
def rename_file_if_exists(filename):
    if os.path.exists(filename):
        # Get current date and hour
        current_datetime = datetime.now()
        date_hour_suffix = current_datetime.strftime("_%Y-%m-%d_%H-%M-%S")
        
        # Split the filename and extension
        base_filename, file_extension = os.path.splitext(filename)
        
        # Construct the new filename with date and hour suffix
        new_filename = base_filename + date_hour_suffix + file_extension
        
        # Rename the file
        os.rename(filename, new_filename)
        
def count_json_files(directory):
    # Initialize the count
    json_count = 0
    
    # Iterate over files in the directory
    for filename in os.listdir(directory):
        # Check if the file has a .json extension
        if filename.endswith(".json"):
            json_count += 1
    
    return json_count


if __name__ == "__main__":
    #Load graph from a  csv file and crawl the nodes (wikipedia pages)
    df = pd.read_csv(LOGS_PATH + '/' + 'links_plus_qids_official.csv', usecols=['end'])
    tqdm.write(f'Crawl Wikipedia Pages')
    wiki_web_crawler(df['end'].unique()[:1100])
    
    #Load not fund wiki pages from a csv file and crawl those pages
    for i in range(1,4):
        path_not_found_pages = WIKI_PAGES + '/' + 'not_found_wiki_pages' + '.csv'
        if os.path.exists(path_not_found_pages):
            tqdm.write(f'Trying to recover lost wikipedia pages: {i}')
            
            df = pd.read_csv(path_not_found_pages, usecols=[0], header=None)
            rename_file_if_exists(path_not_found_pages)
            
            wiki_web_crawler(df.iloc[:, 0].drop_duplicates())
        else:
            tqdm.write('All wikipedia pages were crawled')
            break
            
    # Print number of crawled Wikipedia pages
    json_count = count_json_files(WIKI_PAGES)
    print(f"Number of JSON files in the directory: {json_count} out of 1100")