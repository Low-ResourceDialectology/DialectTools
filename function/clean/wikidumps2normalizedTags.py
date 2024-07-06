# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Normalize the present (sub-)dialect tags in the wikidump data
# NOTE: Hard-coded mapping for Bavarian and Alemannic → TODO: Take mapping from json-file as input for generalization to other languages 

import argparse
from collections import defaultdict
import csv
import glob
import json
import logging
import os
import pathlib
import random
import re # Regular expressions for replacing strings in files
import unicodedata
import shutil
import sys


"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def read_wordlists_from_json(wordlists_file):
    # Load the input JSON file
    with open(wordlists_file, 'r', encoding='utf-8') as f:
        wordlists = json.load(f)
        return wordlists
    

def read_articles_from_json(input_dir):
    articles = {}

    input_files = glob.glob(f'{input_dir}/*.json')
    for input_file in input_files:
        # Load the input JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
    
        for id, article in article_data.items():
            article_id = id
            article_dialect = article["dialect"]
            article_text = article["text"]
            
            articles[article_id] = {}
            articles[article_id]["text"] = article_text
            articles[article_id]["dialect"] = article_dialect
            #articles[article_id]["tags"] = []
    
    return articles
"""
File structures:

{
    "10070": {
        "dialect": "Nordbairisch",
        "subdialect": "westlichs Nordboarisch",
        "subsubdialect": "UNKNOWN",
        "id": "10070",
        "revid": "3045",
        "url": "https://bar.wikipedia.org/wiki?curid=10070",
        "title": "Landkroas Naimakk in da Owerpfolz",
        "text": "text_for_article_here"}, ...
}
"""


def inspect_and_tag_articles(article_text, wordlists):
    article_tags = []
    for dialect_name, wordlist in wordlists.items():
        for article_word in article_text:
            # Check for words, not substrings
            if f' {article_word} ' in wordlist:
                article_tags.append(dialect_name)
    return article_tags


def write_to_json(output_dir, dictionary):
    # Save the aggregated data back to a JSON file
    with open(f'{output_dir}/Bavarian_Tagged.json', 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify articles and add (sub-)dialect-tags.")
    parser.add_argument("-i","--input_dir", type=str, help="Directory containing files articles from wikidumps.")
    parser.add_argument("-w","--wordlists_file", type=str, help="File with aggregated wordlists.")
    parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")

    args = parser.parse_args()
    dir_maker(args.output_dir)

    # Bavarian Wikidump Dialect-Tag Normalization
    input_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-freqdicts/bar"
    output_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/aggregated-freqdicts/bar"
    aggregated_tags = ["Northern Bavarian", "Eastern Central Bavarian", "Western Central Bavarian", "Southern Bavarian"]

    # For aggregated dialect-tag 
    for aggregated_tag in aggregated_tags:

        noisy_tags = []
        if aggregated_tag == "Northern Bavarian":
            noisy_tags = ["Nordbairisch","Nordmittlboarisch","Nordmittelbairisch"]

        elif aggregated_tag == "Eastern Central Bavarian":
            noisy_tags = ["Ostmittlboarisch","Ostmittelbairisch","Ostmiddlboarisch"]

        elif aggregated_tag == "Western Central Bavarian":
            noisy_tags = ["Westmittelbairisch","Westmittlboarisch"]

        elif aggregated_tag == "Southern Bavarian":
            noisy_tags = ["Südmittelbairisch","Südmittelbayerisch","Südbairisch","ostsüdboarisch","Südostbayerisch","Siadostboarisch"]

        # Process the corresponding articles file-by-file
        # NOTE: Already got the freq-dicts by sub-dialect, working on them instead for now
        aggr_freq_dict = {}

        # Write aggregated frequency dictionary to output file
        #output_file = f'{args.output_dir}/{aggregated_tag}-freq.json'
        output_file = f'{output_dir_bar}/{aggregated_tag}-freq.json'

        write_to_json(output_file, aggr_freq_dict)

        """
        Halli und Hallo and Greetings my dear ChatGPT,
        I could really use your help right now!
        I have multiple files which hold frequency dictionaries 
        """

