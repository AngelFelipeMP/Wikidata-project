# Wikipedia API
import wikipedia as wp

#TODO: Check how to get the references from a page
#TODO: I should check the json retrived from the WIKI API
page = wp.page("Public Policy")
page.html()


import requests
import csv
from bs4 import BeautifulSoup
from config import *
import pandas as pd

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"


def get_references(page_title):
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

    if "parse" in data:
        # soup = BeautifulSoup(page.html(), 'html.parser')
        soup = BeautifulSoup(data["parse"]["text"]["*"], 'html.parser')

        # Extract all <cite> tags which hold citation data
        citations = soup.find_all('cite')
        return [cite.get_text(strip=True) for cite in citations]
    else:
        return []


def save_to_csv(titles, filename='output.csv'):
    """
    Save the titles and references to a CSV.
    """
    with open(LOGS_PATH + '/' + filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Page Title", "Reference"])
        
        for title in titles:
            references = get_references(title)
            for ref in references:
                writer.writerow([title, ref])
            print(f"References for {title} saved.")

        print(f"CSV file saved as {filename}")


if __name__ == "__main__":
    #Load graph from a  csv file
    df = pd.read_csv(LOGS_PATH + '/' + 'links.csv')
    print(df['start'].unique())
    save_to_csv(df['start'].unique()[:3], filename='references.csv')
