from config import *
import pandas as pd
from icecream import ic
from tqdm import tqdm
from datetime import datetime
from wikiciteparser.parser import parse_citation_template
import mwparserfromhell
import json
import csv
import sys
import os

def ref_extractor(source_text):
    pass
    return refs

def parse_templates(df):
    pass

def count_ref_types(df):
    values=()
    for type in ['mix', 'template', 'text']:
        values = values + ((df_refs_parsed.loc[:, ['ref_type']] == type).sum(),)
    return values + (len(df),)
    

if __name__ == "__main__":
    ref_columns = ['page', 'ref_type', 'ref_extracted', 'template', 'ref_no_template']
    df_refs = pd.DataFrame([], columns=ref_columns)
    
    count_ref_columns = ['page','mix_num_refs','template_num_refs','text_num_refs', 'total_num_refs']
    df_ref_number = pd.DataFrame([],   columns=count_ref_columns)
    
    
    for file_name in tqdm(os.listdir(WIKI_PAGES + '_test'), desc='EXTRACT-REFS', position=0): ##DEBUG
        if file_name.endswith(".json"):
            with open(WIKI_PAGES + '_test' + '/' + file_name, 'r', encoding='utf-8') as file: ##DEBUG
                json_wiki_page = json.load(file)
            
            refs = ref_extractor(json_wiki_page['source'])
            refs = [(json_wiki_page['title'],) + ref for ref in refs] ##Remove if classs
            
            df_new_ref = pd.DataFrame(refs, columns=df_refs.columns)
            df_new_ref_unique = df_new_ref.drop_duplicates(subset='template', keep='first')
            df_refs_parsed = parse_templates(df_new_ref_unique)
            df_refs = df_refs.append(df_refs_parsed, ignore_index=True)
            
            ref_number = count_ref_types(df_refs_parsed)
            page_ref_number = [(json_wiki_page['title'],) + values  for values in ref_number] ##Remove if classs
            df_ref_number = df_ref_number.append(page_ref_number, ignore_index=True)
            
            
    df_refs.to_csv(LOGS_PATH + '/' + 'wikipedia_references' + '.csv', index=False)
    df_ref_number.to_csv(LOGS_PATH + '/' + 'wikipedia_number_of_references' + '.csv', index=False)