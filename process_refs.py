#Pip install wikiciteparser
import pandas as pd
from config import *
from icecream import ic
from tqdm import tqdm

import mwparserfromhell
from wikiciteparser.parser import parse_citation_template

def unwind_dict(d):
    """
    Unwind a dictionary with lists as values.
    """
    try:
        new_dict = {}
        for k, v in d.items():
            if isinstance(v, list):
                for i, item in enumerate(v, start=1):
                    new_dict[k+'_'+str(i)] = item['first'] + ' ' + item['last']
            elif isinstance(v, dict):
                for k2, v2 in v.items():
                    new_dict[k2] = v2
            else:
                new_dict[k] = v
        return new_dict
                
    except:
        return {}
    
def process_ref(page_ref_list):
    # get attributes fron the reference
    for j, (page, ref) in enumerate(tqdm(page_ref_list, desc="Processing")):
        wikicode = mwparserfromhell.parse(ref)
        tpl = wikicode.filter_templates()[0]
        parsed = parse_citation_template(tpl)
        
        # process discto to a plan dict
        unwind_parsed = unwind_dict(parsed)
        
        # add originary page and reference
        combined_dict = {**{'Page':page, 'Reference':ref}, **unwind_parsed}
        
        # create a dataframe from the dict
        if j==0:
            df = pd.DataFrame([combined_dict])
        else:
            new_df = pd.DataFrame([combined_dict])
            df = pd.concat([df, new_df])
    return df

if __name__ == "__main__":
    #Load graph from a  csv file
    df = pd.read_csv(LOGS_PATH + '/' + 'references_official.csv')
    page_ref_list = list(zip(df['Page Title'], df['Reference']))
    
    # Process the references
    df_processed = process_ref(page_ref_list)
    
    # change the order of the columns
    columns_df_processed = df_processed.columns
    start_columns = ['Page','Reference','Title','URL','Date','Periodical','PublicationPlace','PublisherName','Chapter','Pages','Issue','Volume','Edition','Series','ArchiveURL','CitationClass','BIBCODE','DOI','SSRN','ISBN','ISSN','PMC','PMID']
    columns_df_processed = [ col for col in columns_df_processed if col not in start_columns]
    columns_df_processed = start_columns + columns_df_processed
    df_processed = df_processed[columns_df_processed]
    
    # save the processed references
    df_processed.to_csv(LOGS_PATH + '/' + 'references-processed.csv', index=False)
    tqdm.write('Done!')
    

    