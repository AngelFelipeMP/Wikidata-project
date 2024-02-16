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

def unwind_dict(d):
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
    
def parser(page_ref_list):
    # get attributes fron the reference
    for j, (page, ref) in enumerate(tqdm(page_ref_list, desc="PARSING")):
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

def parse_templates(df): ##CHECK
    df_true_template = df[df['template'].notnull() & (df['template'] != '')] ##CHECK
    page_ref_list = list(zip(df_true_template['page'], df_true_template['Reference']))
    df_processed = parser(page_ref_list) ##CHECK
    
    df_merge = pd.merge(df, df_processed, on='template', how='left') ##CHECK

    center_columns = ['Title','URL','Date','Periodical','PublicationPlace','PublisherName','Chapter','Pages','Issue',
                    'Volume','Edition','Series','ArchiveURL','CitationClass','BIBCODE','DOI','SSRN','ISBN','ISSN','PMC','PMID']
    return df_merge[df.columns + center_columns + [col for col in df_processed.columns if col not in center_columns]] ##CHECK


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