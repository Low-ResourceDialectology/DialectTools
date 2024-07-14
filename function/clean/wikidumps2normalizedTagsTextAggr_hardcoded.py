# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Normalize the present (sub-)dialect tags in the wikidump data (now for the files containing the sentences)
# NOTE: Hard-coded mapping for Bavarian and Alemannic → TODO: Take mapping from json-file as input for generalization to other languages 

import argparse
from collections import defaultdict
import json
import pathlib


"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def read_sentences_from_files(file_paths):
    sentences = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            sentences.append(json.load(file))
    return sentences

def combine_sentences(dictionaries):
    combined_dict = defaultdict(int)
    for dictionary in dictionaries:
        for word, frequency in dictionary.items():
            combined_dict[word] += frequency
    return dict(combined_dict)

def save_combined_sentences(combined_dict, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=4)

# All in one for text sentences (modified from previous json version)
def read_and_combine_and_sentences(file_paths, output_file):
    with open(output_file, 'w') as outfile:
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as infile:
                for line in infile:
                    outfile.write(line)


if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="Normalize (sub-)dialect-tags and combine word frequencies.")
    #parser.add_argument("-i","--input_dir", type=str, help="Directory containing files articles from wikidumps.")
    #parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")

    #args = parser.parse_args()
    #dir_maker(args.output_dir)

    # Bavarian Wikidump Dialect-Tag Normalization

    # NOTE: First approach using the "old and noisy" word frequencies
    #input_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-freqdicts/bar"
    #output_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/aggregated-freqdicts/bar"

    # NOTE: Second approach using the "new and clean and lower-cased" word frequencies
    input_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar"
    output_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-aggr/bar"
    dir_maker(output_dir_bar)

    aggregated_tags = ["Bavarian", "Northern Bavarian", "Eastern Central Bavarian", "Western Central Bavarian", "Southern Bavarian"]

    # For aggregated dialect-tag 
    for aggregated_tag in aggregated_tags:

        noisy_tags = []
        noisy_tags_files = []
        if aggregated_tag == "Bavarian":
            noisy_tags = ["UNKNOWN","andere"]
        
        elif aggregated_tag == "Northern Bavarian":
            noisy_tags = ["Nordbairisch","Nordmittlboarisch","Nordmittelbairisch"]
            
        elif aggregated_tag == "Eastern Central Bavarian":
            noisy_tags = ["Ostmittlboarisch","Ostmittelbairisch","Ostmiddlboarisch"]
            
        elif aggregated_tag == "Western Central Bavarian":
            noisy_tags = ["Westmittelbairisch","Westmittlboarisch"]
            
        elif aggregated_tag == "Southern Bavarian":
            noisy_tags = ["Südmittelbairisch","Südmittelbayerisch","Südbairisch","ostsüdboarisch","Südostbayerisch","Siadostboarisch"]
            
        # Build file paths based on noisy tags
        for noisy_tag in noisy_tags:
            file_path = f'{input_dir_bar}/{noisy_tag}.txt'
            noisy_tags_files.append(file_path)

        # Process the corresponding articles file-by-file
        # NOTE: Already got the freq-dicts by sub-dialect, working on them instead for now
        # aggr_freq_dict = {}

        # Write aggregated frequency dictionary to output file
        #output_file = f'{args.output_dir}/{aggregated_tag}-freq.json'
        output_file = f'{output_dir_bar}/{aggregated_tag}.txt'

        # Read, combine and save the text data (sentences)
        #sentences = read_sentences_from_files(noisy_tags_files)
        #aggr_sents = combine_sentences(sentences)
        #save_combined_sentences(aggr_sents, output_file)
        read_and_combine_and_sentences(noisy_tags_files, output_file)
        
        

