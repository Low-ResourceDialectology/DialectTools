# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Classify articles (from wikidumps) based on word-frequencies (from aggregated wordlists)
#   Input: Json files per pre-tagged language variety in wikidumps-data, json-file of aggregated wordlists
#   Output: (Sub-)Dialect-Tagged articles from wikidumps (as txt-files) 

import argparse
import glob
import json
import os
import pathlib


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


def write_articles_to_json(output_dir, articles):
    # Save the aggregated data back to a JSON file
    with open(f'{output_dir}/Bavarian_Tagged.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify articles and add (sub-)dialect-tags.")
    parser.add_argument("-i","--input_dir", type=str, help="Directory containing files articles from wikidumps.")
    parser.add_argument("-w","--wordlists_file", type=str, help="File with aggregated wordlists.")
    parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")

    args = parser.parse_args()
    dir_maker(args.output_dir)


    wordlists = read_wordlists_from_json(args.wordlists_file)

    articles = read_articles_from_json(args.input_dir)

    for article_id in articles.keys():
        article_text = articles[article_id]["text"]
        article_tags = inspect_and_tag_articles(article_text, wordlists)
        articles[article_id]["tags"] = article_tags

    write_articles_to_json(args.output_dir, articles)

