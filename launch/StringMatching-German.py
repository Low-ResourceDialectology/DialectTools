# Based on bidictionaries: Find string matches in aligned words and output all + frequencies in separat files
# 
# Authors: Christian "Doofnase" Schuler, 
###############################################################################

""" Transform Standard German text data into varietie text data """

import argparse
import csv
import json
import os
import unicodedata
import shutil
import sys
import pandas as pd
import glob # For reading multiple txt files and write them into a single file in one go
import re # Regular expressions for replacing strings in files
import pathlib
#from pathlib import Path # Alternative approach for replacing strings in-place
from difflib import SequenceMatcher  
#import Levenshtein 


parser = argparse.ArgumentParser(description='Match (sub-)strings in aligned words with each other')
parser.add_argument('--source', type=str, help='source language')
parser.add_argument('--target', type=str, help='aligned target language')
parser.add_argument('--src-lang', type=str, help='source language code')
parser.add_argument('--trg-lang', type=str, help='aligned target language code')
parser.add_argument('--clean-dir', type=str, help='input directory of prepared files')
parser.add_argument('--exp-dir', type=str, help='output directory for experiment files')
#parser.add_argument('--files', type=str, help='different filenames (temporary fix to include other data)')

# Example:
"""
source="bar"
target="deu"
src-lang="Bavarian"
trg-lang="German"
clean-dir="/media/AllBlue/LanguageData/CLEAN"
exp-dir="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-Sock-${TARGET}L-DBLI-0001"
"""
args = parser.parse_args()

# TODO: Input arguments for more versatility
src_l = args.source
trg_l = args.target
#date_of_experiment = '20240528'
clean_dir = f'{args.clean_dir}/{args.src_lang}' # f'/media/AllBlue/LanguageData/PREP/opustools/{src_l}-{trg_l}/{date_of_experiment}'
down_dir = f'/media/AllBlue/LanguageData/DOWNLOAD/handmade/ChatGPT-German-Morphemes'
# src_train = f'{clean_dir}/train.{src_l}'
# trg_train = f'{clean_dir}/train.{trg_l}'
# #testdev_dir = f'/media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001'
# src_dev =  f'{clean_dir}/dev.{src_l}'
# trg_dev =  f'{clean_dir}/dev.{trg_l}'
# src_test =  f'{clean_dir}/test.{src_l}'
# trg_test =  f'{clean_dir}/test.{trg_l}'
#experiment_dir = "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-barL-SYNT-mult-Opus-0001/Perturbed/Large" # NOTE: Switch here and at bottom of script
experiment_dir = args.exp_dir #"/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-barL-SYNT-mult-Opus-0001/Perturbed/Medium"
# src_train_out = f'{experiment_dir}/train.{src_l}'
# trg_train_out = f'{experiment_dir}/train.{trg_l}'
# src_dev_out =  f'{experiment_dir}/dev.{src_l}'
# trg_dev_out =  f'{experiment_dir}/dev.{trg_l}'
# src_test_out =  f'{experiment_dir}/test.{src_l}'
# trg_test_out =  f'{experiment_dir}/test.{trg_l}'


"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def normalize_text(text):
    """Normalize text using Unicode NFC normalization."""
    #return unicodedata.normalize('NFC', text)
    #return unicodedata.normalize('NFKC', text)
    return unicodedata.normalize('NFKD', text)

# Read text file
def read_text(input_file):
    input_text = []
    with open(f'{input_file}', 'r', encoding='utf-8') as in_file:
        for text_line in in_file.readlines():
            normalized_string = normalize_text(text_line.strip())
            input_text.append(normalized_string)
    return input_text

# Read perturbation rules
def read_bidict(dict_file):
    """ Read bidict from single file and keep alternative pairs for each entry (key) """
    bidict = {}
    word_counter = 0
    with open(dict_file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            bidict[str(word_counter)] = {}
            bidict[str(word_counter)]["pair"] = f'{normalize_text(row[1].strip())}-{normalize_text(row[0].strip())}'
            word_counter = word_counter + 1

    print(f'Bidict entries: {len(bidict.keys())}')
    return bidict

# Detect matching strings based on similarity metric
def find_subword_matches(word1, word2):     
	matcher = SequenceMatcher(None, word1, word2)     
	matches = []     
	for block in matcher.get_matching_blocks():         
		if block.size > 0:             
			matches.append(word1[block.a:block.a+block.size])   
	return matches  
# Example usage matches = find_subword_matches("leute", "leit") print(matches)  # ['le', 't']

###############################################################################
# Including human-annotated Bidictionaries for less noise, but also getting less volume.
# → Saved in the subdirectory /Perturbed/Medium/
dict_files = [f'{clean_dir}/2023ArteDial-{src_l}L-BiDi-{trg_l}L-0003.csv',f'{clean_dir}/2023ArteDial-{src_l}L-BiDi-{trg_l}L-0002.csv']
dict_files_large = [f'{clean_dir}/2023ArteDial-{src_l}L-BiDi-{trg_l}L-0003.csv',f'{clean_dir}/2023ArteDial-{src_l}L-BiDi-{trg_l}L-0002.csv',f'{clean_dir}/2023ArteDial-{src_l}L-BiDi-{trg_l}L-0001.csv',f'{down_dir}/2024SchuChat-{src_l}L-BiDi-{trg_l}L-0001.csv']
# NOTE: The large file (0001) contains a lot of noise that deteriorates the text content considerably
# NOTE: subwords = True | False decides about inclusion of subword replacement rules in addition to the bilexicon-based replacement rules 
dict_counter = 0
# if args.files == "ChatGPT":
#     dict_files_large = [f'{clean_dir}/2024SchuChat-{src_l}L-BiDi-{trg_l}L-0001.csv']
#     dict_counter = 3

for dict_file in dict_files_large:
    bidict = read_bidict(dict_file)

    for key in bidict.keys():
        new_id = bidict[key]["pair"]
        src_word = new_id.split('-')[0]
        trg_word = new_id.split('-')[1]
        
        # Find matching strings
        current_matches = find_subword_matches(src_word, trg_word)
        bidict[key]["matches"] = current_matches

        # If word begins with one of its matches, consider it to be a prefix
        prefixes = ""
        for match in current_matches:
            if (src_word.startswith(match)) and (trg_word.startswith(match)):
                prefixes = match
                # Additionally add the word without the matching prefix
                src_word_without_match = src_word.replace(match,'')
                trg_word_without_match = trg_word.replace(match,'')
                bidict[key]["no-prefix"] = f'{src_word_without_match}-{trg_word_without_match}'
            bidict[key]["prefix"] = prefixes

        # If word ends with one of its matches, consider it to be a suffix
        suffixes = ""
        for match in current_matches:
            if (src_word.endswith(match)) and (trg_word.endswith(match)):
                suffixes = match
                # Additionally add the word without the matching suffix
                src_word_without_match = src_word.replace(match,'')
                trg_word_without_match = trg_word.replace(match,'')
                bidict[key]["no-suffix"] = f'{src_word_without_match}-{trg_word_without_match}'
            bidict[key]["suffix"] = suffixes

        # Whenever the word-pair has not matching characters in front of suffix, but also a prefix, this has to be removed
        if ("no-suffix" in bidict[key]) and (len(bidict[key]["prefix"]) > 0):
            src_word_without_match = bidict[key]["no-suffix"].split('-')[0].replace(bidict[key]["prefix"],'')
            trg_word_without_match = bidict[key]["no-suffix"].split('-')[1].replace(bidict[key]["prefix"],'')
            bidict[key]["no-suffix"] = f'{src_word_without_match}-{trg_word_without_match}'
        # Whenever the word-pair has not matching characters in front of suffix, but also a prefix, this has to be removed
        if ("no-prefix" in bidict[key]) and (len(bidict[key]["suffix"]) > 0):
            src_word_without_match = bidict[key]["no-prefix"].split('-')[0].replace(bidict[key]["suffix"],'')
            trg_word_without_match = bidict[key]["no-prefix"].split('-')[1].replace(bidict[key]["suffix"],'')
            bidict[key]["no-prefix"] = f'{src_word_without_match}-{trg_word_without_match}'


    # Count frequencies for the string matches
    prefix_freq = {}
    suffix_freq = {}
    match_freq = {}
    no_prefix_freq = {}
    no_suffix_freq = {}
    for key in bidict.keys():
        if ("prefix" in bidict[key] and len(bidict[key]["prefix"]) > 0): 
            prefix = bidict[key]["prefix"]
            if prefix in prefix_freq:
                prefix_freq[prefix] = prefix_freq[prefix] + 1
            else:
                prefix_freq[prefix] = 1
        if ("suffix" in bidict[key] and len(bidict[key]["suffix"]) > 0): 
            suffix = bidict[key]["suffix"]
            if suffix in suffix_freq:
                suffix_freq[suffix] = suffix_freq[suffix] + 1
            else:
                suffix_freq[suffix] = 1
        if (len(bidict[key]["matches"]) > 0):
            for match in bidict[key]["matches"]:
                if match in match_freq:
                    match_freq[match] = match_freq[match] + 1
                else:
                    match_freq[match] = 1
        if ("no-prefix" in bidict[key]): 
            no_prefix = bidict[key]["no-prefix"]
            if no_prefix in no_prefix_freq:
                no_prefix_freq[no_prefix] = no_prefix_freq[no_prefix] + 1
            else:
                no_prefix_freq[no_prefix] = 1
        if ("no-suffix" in bidict[key]): 
            no_suffix = bidict[key]["no-suffix"]
            if no_suffix in no_suffix_freq:
                no_suffix_freq[no_suffix] = no_suffix_freq[no_suffix] + 1
            else:
                no_suffix_freq[no_suffix] = 1
    # Sort frequency dictionaries in descending order
    sorted_prefix_freq = sorted(prefix_freq.items(), key=lambda x:x[1], reverse=True)
    prefix_freq_dict = dict(sorted_prefix_freq)
    sorted_suffix_freq = sorted(suffix_freq.items(), key=lambda x:x[1], reverse=True)
    suffix_freq_dict = dict(sorted_suffix_freq)
    sorted_match_freq = sorted(match_freq.items(), key=lambda x:x[1], reverse=True)
    match_freq_dict = dict(sorted_match_freq)
    sorted_no_prefix_freq = sorted(no_prefix_freq.items(), key=lambda x:x[1], reverse=True)
    no_prefix_freq_dict = dict(sorted_no_prefix_freq)
    sorted_no_suffix_freq = sorted(no_suffix_freq.items(), key=lambda x:x[1], reverse=True)
    no_suffix_freq_dict = dict(sorted_no_suffix_freq)

    # Serializing json and write to file
    json_object = json.dumps(prefix_freq_dict, indent=4, ensure_ascii=False)
    with open(f'{experiment_dir}/prefixes-{src_l}-{trg_l}-{dict_counter}.json', "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(suffix_freq_dict, indent=4, ensure_ascii=False)
    with open(f'{experiment_dir}/suffixes-{src_l}-{trg_l}-{dict_counter}.json', "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(match_freq_dict, indent=4, ensure_ascii=False)
    with open(f'{experiment_dir}/matches-{src_l}-{trg_l}-{dict_counter}.json', "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(no_prefix_freq_dict, indent=4, ensure_ascii=False)
    with open(f'{experiment_dir}/no_prefixes-{src_l}-{trg_l}-{dict_counter}.json', "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(no_suffix_freq_dict, indent=4, ensure_ascii=False)
    with open(f'{experiment_dir}/no_suffixes-{src_l}-{trg_l}-{dict_counter}.json', "w") as outfile:
        outfile.write(json_object)

    json_object = json.dumps(bidict, indent=4, ensure_ascii=False)
    with open(f'{experiment_dir}/bidict-{src_l}-{trg_l}-{dict_counter}.json', "w") as outfile:
        outfile.write(json_object)
    dict_counter = dict_counter + 1






#file_names = ["test", "dev", "train", "other"]
# for file_name in file_names:
#     # Paths to corresponding files
#     src_in =  f'{clean_dir}/{file_name}.{src_l}'
#     trg_in =  f'{clean_dir}/{file_name}.{trg_l}'
#     src_out = f'{experiment_dir}/{file_name}.{src_l}' # Needed?
#     trg_out = f'{experiment_dir}/{file_name}.{trg_l}' # Needed?
#     file_out = f'{experiment_dir}/{file_name}.{src_l}{trg_l}' 
    # Output dictionary
    # out_dict = {}

    # # Read aligned words
    # src_in_text = read_text(src_in)
    # trg_in_text = read_text(trg_in)
    # counter = 0
    # for src_word, trg_word in zip(src_in_text, trg_in_text):
    #     counter = counter + 1 
    #     new_id = f'{src_word}-{src_word}'
    #     new_entry = {} 
    #     new_entry[new_id] = {}
    #     # Find matching strings
    #     current_matches = []
    #     new_entry[new_id]["matches"] = current_matches

    #     # If word begins with one of its matches, consider it to be a prefix
    #     prefixes = []
    #     for match in current_matches:
    #         if (src_word.startswith(match)) and (trg_word.startswith(match)):
    #             prefixes.append(match)
    #         new_entry[new_id]["prefix"] = prefixes

    #     # If word end with one of its matches, consider it to be a suffix
    #     suffixes = []
    #     for match in current_matches:
    #         if (src_word.endswith(match)) and (trg_word.endswith(match)):
    #             suffixes.append(match)
    #         new_entry[new_id]["suffix"] = suffixes

    #     # Save new entry to dictionary
    #     out_dict[str(counter)] = new_entry