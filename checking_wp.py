# Wikipedia API
import wikipedia as wp
import config
import requests
from icecream import ic
from wikipedia.exceptions import DisambiguationError, PageError
import warnings
warnings.filterwarnings("ignore")


def get_wikidata_qid(page_title, language="en"):
    endpoint_url = f"https://{language}.wikipedia.org/w/api.php"

    params = {
        'action': 'query',
        'prop': 'pageprops',
        'titles': page_title,
        'format': 'json'
    }

    response = requests.get(endpoint_url, params=params)
    data = response.json()

    pages = data.get('query', {}).get('pages', {})
    for _, page_data in pages.items():
        return page_data.get('pageprops', {}).get('wikibase_item')
    
if __name__ == "__main__":
    title="public Policy"
    
    try:
        page = wp.page(title)
        ic(page.title)
        ic(type(list(page.links)))
    
    except (DisambiguationError, PageError):
        pass
    
