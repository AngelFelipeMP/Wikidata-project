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


def get_ref_tamplete(page_title):
    page_title = page_title.replace(' ', '_')
    
    # Replace with the specific Wikipedia article edit URL
    edit_url = f'https://en.wikipedia.org/w/index.php?title={page_title}&action=edit'

    # Fetch the content of the edit page
    response = requests.get(edit_url)
    print(response.text)
        

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

def get_ref_list(page_title):
    """
    Get references from the given Wikipedia page.
    """
    params = {
        'action': 'parse',
        'format': 'json',
        'page': page_title,
        'prop': 'text'
    }

    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()
    
    print(data['parse']['text']['*'])
        
        
if __name__ == "__main__":
    page_title = 'Cultural history'
    get_ref_list(page_title)