from config import *
import pandas as pd
from icecream import ic
from tqdm import tqdm
from datetime import datetime
import mwparserfromhell
from wikiciteparser.parser import parse_citation_template
import json
import csv
import sys
import os
import re

        
def ref_extractor(source_text):
    ref_list_tags, _, source_text_off_tags = extractor_ref_between_tags(source_text)
    ref_list_off_tags_only_templates, _, source_text_off_tags_templates = extractor_ref_template(source_text_off_tags)
    ref_list_only_ref_sections, _ = extractor_ref_sections(source_text_off_tags_templates)
    return ref_list_tags + ref_list_off_tags_only_templates + ref_list_only_ref_sections


# def extractor_ref_between_tags(text, start=1):
def extractor_ref_between_tags(text):
    text = text.replace("\n", " ")  ##COMMENT: I may remove it for the next code version  
    pattern = r'<ref[^/]*?>.*?/ref>'
    ref_list = re.findall(pattern, text, re.DOTALL)
    page_off_tags = re.sub(pattern, '', text)
    ref_list_off_no_ref_templates = remove_no_ref_templates(ref_list)
    return ref_list_off_no_ref_templates,len(ref_list_off_no_ref_templates), page_off_tags


def remove_no_ref_templates(ref_list, identifiers=True):
    ref_list_no_ref_templates = []
    pattern_citation = r'(\{\{ *(?!citation needed)citation|\{\{ *cite|\{\{ *wikicite|\{\{ *vcite|http://)' #{{Webarchive
    pattern_identifiers = r'(\{\{ *DOI|\{\{ *SSRN|\{\{ *ISBN|\{\{ *ISSN|\{\{ *PMC|\{\{ *PMID)'
    
    for ref in ref_list:
        wikicode = mwparserfromhell.parse(ref)
        templates = wikicode.filter_templates()
        if templates:
            for temp in templates:
                if re.search(pattern_citation, temp.__str__(), re.IGNORECASE):
                    ref_list_no_ref_templates.append(('template', ref.__str__(), temp.__str__()))
                elif identifiers:
                    if re.search(pattern_identifiers, temp.__str__(), re.IGNORECASE):
                        ref_list_no_ref_templates.append(('template', ref.__str__(), temp.__str__()))
        else:
            ref_list_no_ref_templates.append(('text',ref.__str__(), None))
    return ref_list_no_ref_templates
        
def extractor_ref_template(text):
    wikicode = mwparserfromhell.parse(text)
    templates = wikicode.filter_templates()
    templates_no_ref_templates_off = remove_no_ref_templates(list(templates), identifiers=False)
    # remove ref templates from source text
    for (_,ref_template, _)in templates_no_ref_templates_off:
        text = text.replace(ref_template, '')

    return templates_no_ref_templates_off,len(templates_no_ref_templates_off), text


def extractor_ref_sections(text):
    pattern = r'(?<!=)(==\s*(?:References?|Citations?|Sources?|Bibliograph(?:y|ies)|Notes?)\s*==.*?)(?=[^=]==\s*\w|$)'
    text_list = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
    ref_list = []
    pattern_text_ref = r'\*\s*\w.*?(?=\*|==)'
    for ref_section in text_list:
        for ref in re.findall(pattern_text_ref, ref_section, re.IGNORECASE):
            ref_list.append(('text', ref, None))
        
    return ref_list,len(ref_list)


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
    for j, (page, ref) in enumerate(page_ref_list):
        wikicode = mwparserfromhell.parse(ref)
        tpl = wikicode.filter_templates()[0]
        parsed = parse_citation_template(tpl)
        
        # process discto to a plan dict
        unwind_parsed = unwind_dict(parsed)
        
        # add originary page and reference
        # combined_dict = {**{'Page':page, 'Reference':ref}, **unwind_parsed} ##TODO: remove
        combined_dict = {**{'template':ref}, **unwind_parsed}
        
        # create a dataframe from the dict
        if j==0:
            df = pd.DataFrame([combined_dict])
        else:
            new_df = pd.DataFrame([combined_dict])
            df = pd.concat([df, new_df], ignore_index=True)
    return df

def parse_templates(df): ##CHECK
    df_true_template = df[df['template'].notnull() & (df['template'] != '')]
    page_ref_list = list(zip(df_true_template['page'], df_true_template['template']))
    
    if page_ref_list:
        df_processed = parser(page_ref_list)
        df_merge = pd.merge(df, df_processed, on='template', how='left')
    else:
        df_processed = pd.DataFrame()
        df_merge = df.copy()

    center_columns = ['Title','URL','Date','Periodical','PublicationPlace','PublisherName','Chapter','Pages','Issue',
                    'Volume','Edition','Series','ArchiveURL','CitationClass','BIBCODE','DOI','SSRN','ISBN','ISSN','PMC','PMID']
    
    #add missing columns to df_merge
    if not set(center_columns).issubset(set(df_merge.columns)):
        df_merge = add_missing_columns(df_merge, center_columns)
        
    # ic(df_merge.columns)
        
    return df_merge[list(df.columns) + center_columns + [col for col in df_processed.columns if col not in center_columns + ['template']]] ##CHECK

def add_missing_columns(df, cols):
    for col in cols:
        if col not in df.columns:
            df[col] = None 
    return df

def count_ref_types(df):
    values=()
    for type in ['template', 'text']:
        values = values + ((df.loc[:, ['ref_type']] == type).sum().iloc[0],)
    return values + (len(df),)
    

if __name__ == "__main__":
    ref_columns = ['page', 'ref_type', 'ref_extracted', 'template']
    df_refs = pd.DataFrame([], columns=ref_columns)
    
    count_ref_columns = ['page', 'template_num_refs','text_num_refs', 'total_num_refs']
    df_ref_number = pd.DataFrame([],   columns=count_ref_columns)
    
    # for file_name in tqdm(sorted(os.listdir(WIKI_PAGES + '_test')), desc='EXTRACT-REFS', position=0): ##DEBUG
    for file_name in tqdm(sorted(os.listdir(WIKI_PAGES)), desc='EXTRACT-REFS', position=0):
        if file_name.endswith(".json"):
            # with open(WIKI_PAGES + '_test' + '/' + file_name, 'r', encoding='utf-8') as file: ##DEBUG
            with open(WIKI_PAGES + '/' + file_name, 'r', encoding='utf-8') as file:
                json_wiki_page = json.load(file)
            
            tqdm.write(json_wiki_page['title']) ##DEBUG
            refs = ref_extractor(json_wiki_page['source'])
            refs = [(json_wiki_page['title'],) + ref for ref in refs] ##Remove if classs
                
            df_new_ref = pd.DataFrame(refs, columns=ref_columns)
            df_new_ref_unique = df_new_ref.drop_duplicates(subset='template', keep='first')
            df_refs_parsed = parse_templates(df_new_ref_unique)
            
            df_refs = add_missing_columns(df_refs, list(df_refs_parsed.columns))
            df_refs = pd.concat([df_refs, df_refs_parsed], ignore_index=True)
            ref_number = count_ref_types(df_refs_parsed)
            
            new_row_df_ref_number = pd.DataFrame([(json_wiki_page['title'],) + ref_number], columns=df_ref_number.columns)
            df_ref_number = pd.concat([df_ref_number, new_row_df_ref_number], ignore_index=True)
            
    df_refs.to_csv(LOGS_PATH + '/' + 'wikipedia_references' + '.csv', index=False)
    df_ref_number.to_csv(LOGS_PATH + '/' + 'wikipedia_number_of_references' + '.csv', index=False)