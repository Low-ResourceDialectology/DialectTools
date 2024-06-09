# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Reads and aggregates cross-lingually aligned wordlists from .json and .csv files.

import argparse
from collections import defaultdict
import csv
import json
import logging
import numpy as np
import matplotlib as plt
import os
import pandas as pd
import pprint
import random
import sys


def read_csv_to_dict(file_path):
    word_dict = {}

    # Open the CSV file
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Read the header row to get the language names
        languages = next(csv_reader)
        # Remove leading and trailing empty spaces
        languages = [lang.strip() for lang in languages]
        
        # Initialize the word dictionary for each language
        for language in languages:
            if language not in word_dict:
                word_dict[language.strip()] = {}
        
        # Read each row and add words to the dictionary
        for row in csv_reader:
            for i, word in enumerate(row):
                if not word:  # Skip empty strings
                    continue
                lang = languages[i]
                word = word.strip()
                if word not in word_dict[lang]:
                    word_dict[lang][word] = {}
                
                # Add translations
                for j, trans in enumerate(row):
                    if not trans:  # Skip empty strings
                        continue
                    trans = trans.strip()
                    if i != j:
                        target_lang = languages[j]
                        if target_lang not in word_dict[lang][word]:
                            word_dict[lang][word][target_lang] = []
                        
                        if trans not in word_dict[lang][word][target_lang]:
                            word_dict[lang][word][target_lang].append(trans)
    
    return word_dict

def read_json_to_dict(file_path):
    word_dict = defaultdict(lambda: defaultdict(list))

    # Load the JSON file
    with open(file_path, mode='r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        
        # Iterate over the top-level keys (e.g., "BavarianDialects")
        for language_level, dialects in data.items():
            print(f'Language Level: {language_level}')

            # Iterate over the dialects and their word lists
            for dialect, words in dialects.items():
                #dialect = dialect.strip()
                #print(f'Dialect Level: {dialect} with {len(words)} many words')
                if dialect not in word_dict:
                    word_dict[dialect] = {}
                
                for i, word in enumerate(words):
                    word = word.strip()
                    #print(f'word: {word}')
                    if word not in word_dict[dialect]:
                        word_dict[dialect][word] = {}
                    # Add translations
                    for other_dialect, other_words in dialects.items():
                        if not len(other_words) == len(words): # Skip if differnt number of words (data not aligned!)
                            continue
                        #print(f'Other Dialect: {other_dialect} with {len(other_words)} many words')
                        #other_dialect = other_dialect.strip()
                        if other_dialect == dialect: # Skip if the same dialect
                            continue
                        if other_dialect not in word_dict[dialect][word]:
                            word_dict[dialect][word][other_dialect] = []
                        if not other_words[i]: # Skip empty entries
                            continue
                        if other_words[i] not in word_dict[dialect][word][other_dialect]:
                            word_dict[dialect][word][other_dialect].append(other_words[i])


                    #for other_dialect in dialects.keys():
                        #other_dialect = other_dialect.split()
                        #print(f'Compare with: {other_dialect} with {len(dialects[other_dialect])} many words')
                        # Only consider the other dialects
                        # if other_dialect == dialect:
                        #     continue
                        # print(f'dialects[other_dialect]: {data[dialect][other_dialect]}')
                        # trans = dialects[other_dialect][i]
                        # print(f'translation: {trans}')
                        # if not trans:  # Skip empty strings
                        #     continue
                        # trans = trans.strip()
                        # if other_dialect not in word_dict[dialect][word]:
                        #     word_dict[dialect][word][other_dialect] = []
                        
                        # if trans not in word_dict[dialect][word][other_dialect]:
                        #     word_dict[dialect][word][other_dialect].append(trans)

                    # if word:  # Skip empty strings
                    #     word_dict[language_level][i].append((dialect, word))
    
    return word_dict

# NOTE: Derpy version with indices
# def read_json_to_dict(file_path):
#     word_dict = defaultdict(lambda: defaultdict(list))

#     # Load the JSON file
#     with open(file_path, mode='r', encoding='utf-8') as jsonfile:
#         data = json.load(jsonfile)
        
#         # Iterate over the top-level keys (e.g., "BavarianDialects")
#         for language_level, dialects in data.items():
#             print(f'Language Level: {language_level}')
#             # Iterate over the dialects and their word lists
#             for dialect, words in dialects.items():
#                 print(f'Dialect Level: {dialect}')
#                 for i, word in enumerate(words):
#                     if word:  # Skip empty strings
#                         word_dict[language_level][i].append((dialect, word))
    
#     return word_dict


def parse_csv(new_data, word_dict):
    for language in new_data[0]:
        word_dict[language] = {}

def parse_json(new_data, word_dict):
    pass

def add_word(word_dict, language, word, translations):
    """
    Add a word and its translations to the word dictionary.
    
    :param word_dict: The main dictionary holding all words.
    :param language: The language of the word being added.
    :param word: The word being added.
    :param translations: A dictionary of translations, with keys as target languages and values as lists of translations.
    """
    if language not in word_dict:
        word_dict[language] = {}
    if word not in word_dict[language]:
        word_dict[language][word] = {}
    
    for target_lang, trans in translations.items():
        if target_lang not in word_dict[language][word]:
            word_dict[language][word][target_lang] = []
        
        # Ensure translations are stored as lists
        if isinstance(trans, str):
            trans = [trans]
        for t in trans:
            if t not in word_dict[language][word][target_lang]:
                word_dict[language][word][target_lang].append(t)
               

def save_wordlists_to_file(out_path, out_file, out_data):
    """ Creates a separate file for a language variety, holding all its words in a simple list """
    pass

def save_dictionary_to_file(out_path, out_file, out_data):
    """ Saves all words with their cross-lingual alignments to file """
    json_object = json.dumps(out_data, indent=4, ensure_ascii=False)
    try:
        with open(f'{out_path}/{out_file}.json', 'w', newline='', encoding='utf-8') as json_file:
            json_file.write(json_object)
    except Exception as e:
        logging.error(f"Error writing data to {out_path}/{out_file}.json: {e}")

def get_word_statistics():
    """ Information about the words and alignments processed """
    pass

def save_statistics_to_file():
    pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split sentences from CSV files into subsets.")
    parser.add_argument("-i","--input_dir", type=str, help="Directory containing files with text content.")
    parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")
    parser.add_argument("-f","--output_file", type=str, help="Name of output file.")
    #parser.add_argument("-l","--lists_output", type=str, help="To get a wordlist for each language.")
    #parser.add_argument("-d","--dict_output", type=str, help="To get a dictionary with all languages.")

    args = parser.parse_args()
    
    # Aggregate dictionary with words from languages
    word_dict = {}

    # TODO: Add directory processing, for now only one file
    # Process all files from input_dir
    #input_files = []
    # for input_file in input_files:
    #     if input_file.endswith('.csv'):
    #         wordlist = read_csv_to_dict(input_file)
    #         word_dict = parse_csv(wordlist, word_dict)
    #     elif input_file.endswith('.json'):
    #         wordlist = read_json_to_dict(input_file)
    #         word_dict = parse_json(wordlist, word_dict)
    #     else:
    #         print(f'File format not recognized!')
    input_file = args.input_dir
    if input_file.endswith('.csv'):
        word_dict = read_csv_to_dict(input_file)
    elif input_file.endswith('.json'):
        word_dict = read_json_to_dict(input_file)

    # Sorting words alphabetically within each language dictionary
    for language in word_dict:
        word_dict[language] = dict(sorted(word_dict[language].items()))

    # Print the word dictionary
    #pprint.pprint(word_dict)

    # if args.lists_output == True:
    #     for language in word_dict.keys():
    #         save_wordlists_to_file(args.output_dir, language, word_dict[language].keys())

    # if args.dict_output == True:
    save_dictionary_to_file(args.output_dir, args.output_file, word_dict)