# -*- coding: utf8 -*-

# Cleaning the text of the split-up dialect subsets from the Wikipedia dump file

import argparse
import csv
import codecs
import glob
import json
import logging
import os
import re
import sys
import time
from tqdm import tqdm
from collections import defaultdict
from nltk.tokenize import word_tokenize
import stanza

parser = argparse.ArgumentParser(description='Clean Wikidumps')
parser.add_argument('--code', type=str, help='language code to process')
parser.add_argument('--input-dir', type=str, help='input directory')
parser.add_argument('--output-dir', type=str, help='output directory')
parser.add_argument('--log-dir', type=str, help='logging directory')

args = parser.parse_args()

# Configure logging
logging.basicConfig(filename=f'{args.log_dir}/processing_errors-wikidumps2clean.log', level=logging.ERROR)

nlp = stanza.Pipeline(lang='de', processors='tokenize')

""" Helper fucntion for text preprocessing """
def preprocess(text):
    # NOTE: Leave this step for later to better compare with DialectBLI data
    #text = str(text).lower()

    # remove line break character
    #text = text.rstrip(" \n")
    text = re.sub(r'\\n', '', text)

    # remove parenthesized texts
    text = re.sub(r"\(.*?\)", "", text)
    
    # remove brackets
    text = re.sub(r"\[.*?\]", "", text)

    # remove quotation marks
    text = re.sub(r'(\<|\>|"|“|”|„|»|«)*', "", text)

    # remove http websites
    text = re.sub(r"(https?:\/\/)[a-zA-Z1-9_.@?=#\/*]*", "", text)

    # remove other symbols
    text = re.sub(r"(\*|\+|@|#|:|;|{|})*", "", text)
    
    # remove parenthesis again
    text = text.replace("(", "").replace(")", "")

    # trim extra whitespace
    text = re.sub(r' {2,100}', "", text)

    return text


""" Helper function for segmenting articles into sentences """
def segment_sentences(text):
    
    doc = nlp(text)
    segmented_text = [sentence.text for sentence in doc.sentences]

    return segmented_text


# TODO: What happens when I tokenize a tokenized text again? How clever are modern tokenizers?
""" Helper function to tokenize texts """
def nltk_tokenize(text):
    tokenized = word_tokenize(text)
    if len(tokenized[-1]) != 1:
        tokenized.append(".")
    return " ".join(tokenized)


""" Helper function to re-encode text data to UTF-8 """
def reencode_to_utf8(text):
    try:
        if isinstance(text, str):
            # Decode Unicode escape sequences
            text = codecs.decode(text, 'unicode_escape')
            # Remove surrogate pairs
            text = re.sub(r'[\ud800-\udfff]', '', text)
            # Encode and decode to ensure UTF-8 encoding, replacing errors
            text = text.encode('utf-8', 'replace').decode('utf-8')        
            #return codecs.decode(text, 'unicode_escape').encode('utf-8').decode('utf-8')
        elif isinstance(text, list):
            print("Encoding-decoding of lists of strings still work-in-progress (and probably never needed(?))")
            encoded_text = []
            for word in text:
                word = codecs.decode(word, 'unicode_escape').encode('utf-8').decode('utf-8')
                #word.encode('utf-8').decode('utf-8')
                encoded_text.append(word)
            text = encoded_text
        else:
            print(f'Encoding-decoding not possible for: {text}')
        return text
    except Exception as e:
        logging.error(f"Error processing text: {text} - {e}")
        return str(text)


# Clean the content of all text files previously split-up 
def clean_splits(input_path, output_path):
    read_files = glob.glob(f'{input_path}/*')
    
    for f in tqdm(read_files, desc="Processing files"):
        basename = os.path.basename(f).split(".")[0]
        if os.path.exists(f'{output_path}/{basename}.csv'):
            print(f'Output file detected, skipping the processing of {f} for now.')
            continue
        out_data = []
        with open(f, "r", encoding='utf-8') as infile:
            # Read all articles
            current_articles = json.load(infile)
            # Prevent an empty dictionary from crashing the process with: TypeError: 'int' object is not subscriptable
            if len(current_articles) > 0:
                for key in tqdm(current_articles.keys(), desc="Processing Articles"):
                    article = current_articles[key]
                    try:
                        art_title = reencode_to_utf8(article["title"])
                    except Exception as e:
                        logging.error(f"Error processing article in file {f}: {article} - {e}")

                    art_text = article["text"]
                    art_dialect = article["dialect"].replace('[[','').replace(']]','')
                    art_subdialect = article["subdialect"].replace('[[','').replace(']]','')
                    art_subsubdialect = article["subsubdialect"].replace('[[','').replace(']]','')

                    try:
                        encoded_text = reencode_to_utf8(art_text)
                    except Exception as e:
                        logging.error(f"Error processing article in file {f}: {article} - {e}")
                    preprocessed_text = preprocess(encoded_text)
                    segmented_text = segment_sentences(preprocessed_text)

                    for sentence in segmented_text:
                        tokenized_sentence = nltk_tokenize(sentence)
                        current_entry = [art_title, tokenized_sentence, art_dialect, art_subdialect, art_subsubdialect]
                        out_data.append(current_entry)
                    
                    # NOTE: Dictionary less straight forward since each title can now have multiple sentences, requiring a new unique key schema
                    # current_entry = {
                    #     "title":art_title, 
                    #     "text":tokenized_text, 
                    #     "dialect":art_dialect, 
                    #     "subdialect":art_subdialect, 
                    #     "subsubdialect":art_subsubdialect }
                    # out_data[art_title] = current_entry
                    
        # with open(f'{output_path}/{basename}.bar', 'w') as out_file:
        #     for text_line in out_data:
        #         out_file.write(f'{text_line}\n')
        try:
            with open(f'{output_path}/{basename}.csv', 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                # Header
                csv_writer.writerow(['Title', 'Text', 'Dialect', 'Sub-Dialect', 'Sub-Sub-Dialect'])
                for out_row in out_data:
                    csv_writer.writerow(out_row)
        except Exception as e:
            logging.error(f"Error writing data to {output_path}/{basename}.csv: {e}")


def main():
    # Start the timer
    start_time = time.time()

    clean_splits(f'{args.input_dir}', f'{args.output_dir}')
    
    # Calculate and print the elapsed time
    elapsed_time = time.time() - start_time
    print(f'Data processing complete, check "{args.log_dir}/processing_errors-wikidumps2clean.log" for any errors.')
    print(f'Total time taken: {elapsed_time:.2f} seconds')

if __name__ == "__main__":
    main()