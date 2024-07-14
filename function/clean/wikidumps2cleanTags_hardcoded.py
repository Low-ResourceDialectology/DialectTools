# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Normalize the present (sub-)dialect tags in the wikidump data
# NOTE: Hard-coded mapping for Bavarian and Alemannic → TODO: Take mapping from json-file as input for generalization to other languages 

import argparse
from collections import defaultdict
import json
import os
import pathlib
import re


"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def read_dictionaries_from_files(file_paths):
    dictionaries = {}
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            dictionaries[file_path] = json.load(file)
    return dictionaries

def remove_non_german(dictionaries):
    # Regex to match words with only German characters (including umlauts and ß)
    # Bavarian Alphabet found at: https://www.omniglot.com/writing/bavarian.htm
    german_char_pattern = re.compile(r'^[a-zA-ZßÀàÂâÅåÃãĂăÄäÈèÉéÊêẼẽĔĕÎîÒòÓóÔôŎŏÖöÛûÜü\']+$')
    
    cleaned_dictionaries = {}
    for file_path, dictionary in dictionaries.items():
        cleaned_dictionary = {word: freq for word, freq in dictionary.items() if german_char_pattern.match(word)}
        cleaned_dictionaries[file_path] = cleaned_dictionary
    return cleaned_dictionaries

def remove_numbers(dictionaries):#
    # Regex to match words that do not contain any digits
    no_number_pattern = re.compile(r'^\D+$')
    
    cleaned_dictionaries = {}
    for file_path, dictionary in dictionaries.items():
        cleaned_dictionary = {word: freq for word, freq in dictionary.items() if no_number_pattern.match(word)}
        cleaned_dictionaries[file_path] = cleaned_dictionary
    return cleaned_dictionaries

def remove_problematic_entries(dictionaries):
    # Combined regex to match words that contain only valid German characters and do not contain numbers
    valid_german_word_pattern = re.compile(r'^[a-zA-ZßÀàÂâÅåÃãĂăÄäÈèÉéÊêẼẽĔĕÎîÒòÓóÔôŎŏÖöÛûÜü\']+$')
    
    cleaned_dictionaries = {}
    for file_path, dictionary in dictionaries.items():
        cleaned_dictionary = {word: freq for word, freq in dictionary.items() if valid_german_word_pattern.match(word)}
        cleaned_dictionaries[file_path] = cleaned_dictionary
    return cleaned_dictionaries

def find_common_words(dictionaries):
    common_words = set(dictionaries[list(dictionaries.keys())[0]].keys())
    for dictionary in dictionaries.values():
        common_words.intersection_update(dictionary.keys())
    return common_words

def create_combined_info(dictionaries, common_words):
    combined_info = {}
    for word in common_words:
        combined_info[word] = {}
        for file_path, dictionary in dictionaries.items():
            combined_info[word][os.path.basename(file_path)] = dictionary[word]
    return combined_info

def filter_dictionaries(dictionaries, common_words):
    filtered_dictionaries = {}
    for file_path, dictionary in dictionaries.items():
        filtered_dictionaries[file_path] = {word: freq for word, freq in dictionary.items() if word not in common_words}
    return filtered_dictionaries

def save_combined_info(combined_info, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(combined_info, file, ensure_ascii=False,indent=4)

def save_filtered_dictionaries(filtered_dictionaries, new_base_path):
    os.makedirs(new_base_path, exist_ok=True)
    for file_path, dictionary in filtered_dictionaries.items():
        new_file_path = os.path.join(new_base_path, os.path.basename(file_path))
        with open(new_file_path, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, ensure_ascii=False,indent=4)

if __name__ == "__main__":
    # NOTE: Second approach using the "new and clean and lower-cased" word frequencies
    # Bavarian Wikidump Dialect-Tag Normalization
    output_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean/bar"
    dir_maker(output_dir_bar)

    # List of file paths to your word-frequency dictionaries
    input_dir_bar="/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr/bar"

    aggregated_tags = ["Northern Bavarian", "Eastern Central Bavarian", "Western Central Bavarian", "Southern Bavarian"]
    aggregated_tags_files = []

    # Build file paths based on noisy tags
    for aggregated_tag in aggregated_tags:
        file_path = f'{input_dir_bar}/{aggregated_tag}-freq.json'
        aggregated_tags_files.append(file_path)

    combined_info_path = os.path.join(output_dir_bar, 'Bavarian.json')

    # Read the dictionaries
    dictionaries = read_dictionaries_from_files(aggregated_tags_files)

    # Clean the dictionaries
    dictionaries = remove_non_german(dictionaries)
    dictionaries = remove_numbers(dictionaries)
    dictionaries = remove_problematic_entries(dictionaries)  # Apply additional cleaning step
    # NOTE: I do not understand why this last call suddenly works, while the "remove_non_german" and "remove_numbers" did not manage to change any of the dictionary items...

    # Find common words
    common_words = find_common_words(dictionaries)

    # Create combined info dictionary
    combined_info = create_combined_info(dictionaries, common_words)

    # Filter out the common words from the original dictionaries
    filtered_dictionaries = filter_dictionaries(dictionaries, common_words)

    # Save the combined info dictionary
    save_combined_info(combined_info, combined_info_path)

    # Save the filtered dictionaries
    save_filtered_dictionaries(filtered_dictionaries, output_dir_bar)


        


#if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="Normalize (sub-)dialect-tags and combine word frequencies.")
    #parser.add_argument("-i","--input_dir", type=str, help="Directory containing files articles from wikidumps.")
    #parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")

    #args = parser.parse_args()
    #dir_maker(args.output_dir)

    # NOTE: First approach using the "old and noisy" word frequencies
    # Bavarian Wikidump Dialect-Tag Normalization
    # output_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/aggregated-freqdicts-clean/bar"
    # dir_maker(output_dir_bar)

    # # List of file paths to your word-frequency dictionaries
    # input_dir_bar="/media/AllBlue/LanguageData/CLEAN/wikidumps/aggregated-freqdicts/bar"