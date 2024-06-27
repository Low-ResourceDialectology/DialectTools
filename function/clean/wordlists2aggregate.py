# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Applying replacement rules (lexicographical)
#   Input: Dictionary with replacement rules in json format and text to perturb
#   Output: Perturbed text file

import argparse
from collections import defaultdict
import csv
import glob
import json
import logging
import os
import pathlib
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

def read_wordlist_from_json(input_file):
    # Load the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def aggregate_wordlists(in_wordlists):
    # Initialize an empty dictionary to store the aggregated data
    aggregated_data = defaultdict(lambda: defaultdict(list))

    # Iterate over each dictionary in the JSON file
    for language_level, dialects in in_wordlists.items():
    #for dialect_dict in in_wordlists.values():
        for dialect, words in dialects.items():
            # If the dialect is already in the aggregated dictionary, update its word list
            if dialect in aggregated_data:
                # Add new words to the existing word list and remove duplicates
                aggregated_data[dialect].update(words)
            else:
                # Add the dialect and its word list to the aggregated dictionary
                aggregated_data[dialect] = set(words)

    # Convert sets back to lists for JSON serialization
    for dialect in aggregated_data:
        aggregated_data[dialect] = list(aggregated_data[dialect])

    return aggregated_data
    
def clean_wordlists(wordlists):
    cleaned_lists = {}
    for dialect_name, words in wordlists.items():
        clean_words = []
        for word in words:

            # remove parenthesized texts
            word = re.sub(r"\(.*?\)", "", word)

            # remove brackets
            word = re.sub(r"\[.*?\]", "", word)

            # remove alternatives # TODO: Parse them into the list. Examples: "dieser, -e, -es etc." → "dieser", "diese", "dieses" and "töten, umbringen" → "töten", "umbringen"
            word = word.split(',')[0]

            # remove alternatives
            word = word.split(';')[0]

            # trim extra whitespace
            word = word.strip()

            # Handle alternative words such as: "klein/klaan/klëën" → "klein", "klaan", "klëën"
            if '/' in word:
                # Handle multi-word expressions containing a / symbol such as: du büsch/bisch → "du büsch", "du bisch"
                if ' ' in word:
                    first_part = word.split(' ')[0]
                    second_part = word.split(' ')[1].split('/')
                    for sub_word in second_part:
                        new_word = f'{first_part} {sub_word}'
                        clean_words.append(new_word)

                        # TODO: Also handle the reverse case AND mixed cases such as: "i bü/bi gsy" → "i bü gsy", "i bi gsy"
                else:
                    for new_word in word.split('/'):
                        clean_words.append(new_word)
            else:
                clean_words.append(word)

        cleaned_lists[dialect_name] = set(clean_words)

    # Convert sets back to lists for JSON serialization
    for dialect in cleaned_lists:
        cleaned_lists[dialect] = list(cleaned_lists[dialect])

    return cleaned_lists

def write_wordlist_to_json(output_file, aggregated_data):
    # Save the aggregated data back to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(aggregated_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split sentences from CSV files into subsets.")
    parser.add_argument("-i","--input_file", type=str, help="File with collected wordlists.")
    parser.add_argument("-o","--output_file", type=str, help="Output file with aggregated wordlists.")
    
    args = parser.parse_args()

    wordlists = read_wordlist_from_json(args.input_file)

    aggregated_data = aggregate_wordlists(wordlists)

    cleaned_data = clean_wordlists(aggregated_data)

    write_wordlist_to_json(args.output_file, cleaned_data)



