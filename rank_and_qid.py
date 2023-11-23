# Data manipulation
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

# Wikipedia API
# import wikipedia as wp

# Configuration
import config
import requests
import icecream as ic

def get_wikidata_qid(page_title, language="en"):
    endpoint_url = f"https://{language}.wikipedia.org/w/api.php"

    params = {
        'action': 'query',
        'prop': 'pageprops',
        'titles': page_title,
        'format': 'json'
    }

    try:
        response = requests.get(endpoint_url, params=params)
        data = response.json()

        pages = data.get('query', {}).get('pages', {})
        for _, page_data in pages.items():
            return page_data.get('pageprops', {}).get('wikibase_item')
        
    except:
        return 'NOT-FOUND'
    
if __name__ == "__main__":

    df_graph = pd.read_csv(config.LOGS_PATH + '/' + 'links.csv')
    df_rank = df_graph.groupby('end').weight.sum().sort_values(ascending=False).reset_index()
    # df_rank['Qid'] = df_rank['end'].apply(lambda x: get_wikidata_qid(x))
    df_rank['Qid'] = df_rank['end'].progress_apply(lambda x: get_wikidata_qid(x))
    df_rank.to_csv(config.LOGS_PATH + '/' + 'links_plus_qids.csv', index=False)

    print('Finished!')
    
    
    
    
    
    
# def get_wikidata_qid(page_title, language="en"):
#     endpoint_url = f"https://{language}.wikipedia.org/w/api.php"

#     params = {
#         'action': 'query',
#         'prop': 'pageprops',
#         'titles': page_title,
#         'format': 'json'
#     }

#     response = requests.get(endpoint_url, params=params)
#     data = response.json()

#     pages = data.get('query', {}).get('pages', {})
#     for _, page_data in pages.items():
#         return page_data.get('pageprops', {}).get('wikibase_item')