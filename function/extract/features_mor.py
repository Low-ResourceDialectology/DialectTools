# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Extracting linguistic features (morphological)
#   Input: Bidictionary in csv format
#   Output: json file

import argparse
from collections import defaultdict
import csv
import glob
import json
import logging
import os
import unicodedata
import pathlib
from difflib import SequenceMatcher  

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


# Read perturbation rules
def read_bidict(dict_file):
    """ Read bidict from single file and keep alternative pairs for each entry (key) """
    bidict = {}
    word_counter = 0
    # Introduce an index in order to keep words with more than one possible alignments
    with open(dict_file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            bidict[str(word_counter)] = {}
            bidict[str(word_counter)]["pair"] = f'{normalize_text(row[1].strip())}-{normalize_text(row[0].strip())}'
            word_counter = word_counter + 1

    print(f'Bidict entries: {len(bidict.keys())}')
    return bidict


# Write output json file
def write_to_json(out_path, out_file, output_dictionary):
    # Serializing json and write to file
    json_object = json.dumps(output_dictionary, indent=4, ensure_ascii=False)
    try:
        with open(f'{out_path}/{out_file}-mor.json', "w") as json_file:
            json_file.write(json_object)
    except Exception as e:
        logging.error(f"Error writing data to {out_path}/{out_file}.json: {e}")


# Detect matching strings based on similarity metric
def find_subword_matches(word1, word2):     
	matcher = SequenceMatcher(None, word1, word2)     
	matches = []     
	for block in matcher.get_matching_blocks():         
		if block.size > 0:             
			matches.append(word1[block.a:block.a+block.size])   
	return matches  
# Example usage matches = find_subword_matches("leute", "leit") print(matches)  # ['le', 't']




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split sentences from CSV files into subsets.")
    parser.add_argument("-i","--input_dir", type=str, help="Directory containing files with text content.")
    parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")
    parser.add_argument("-s","--src_lang", type=str, help="Language code of source language, part of file naming.")
    parser.add_argument("-a","--src_name", type=str, help="Language name of source language, part of file naming.")
    parser.add_argument("-t","--trg_lang", type=str, help="Language code of target language, part of file naming.") # TODO: Make optional
    parser.add_argument("-b","--trg_name", type=str, help="Language name of target language, part of file naming.") # TODO: Make optional

    args = parser.parse_args()
    dir_maker(args.output_dir)

    dict_files = glob.glob(f'{args.input_dir}/*', recursive = False)
    for dict_file in dict_files:
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
                    # NOTE: This also removes the match from other positions in the word!
                    #src_word_without_match = src_word.replace(match,'')
                    #trg_word_without_match = trg_word.replace(match,'')
                    # NOTE: This only removes the match at the desired position!
                    src_word_without_match = src_word[len(match):]
                    trg_word_without_match = trg_word[len(match):]
                    
                    bidict[key]["no-prefix"] = f'{src_word_without_match}-{trg_word_without_match}'
                    bidict[key]["prefix"] = prefixes

            # If word ends with one of its matches, consider it to be a suffix
            suffixes = ""
            for match in current_matches:
                if (src_word.endswith(match)) and (trg_word.endswith(match)):
                    suffixes = match
                    # Additionally add the word without the matching suffix
                    #src_word_without_match = src_word.replace(match,'')
                    #trg_word_without_match = trg_word.replace(match,'')
                    src_word_without_match = src_word[:-len(match)]
                    trg_word_without_match = trg_word[:-len(match)]
                    
                    bidict[key]["no-suffix"] = f'{src_word_without_match}-{trg_word_without_match}'
                    bidict[key]["suffix"] = suffixes

            # NOTE: Why though? # Whenever the word-pair has not matching characters in front of suffix, but also a prefix, this has to be removed
            # if ("no-suffix" in bidict[key]) and (len(bidict[key]["prefix"]) > 0):
            #     src_word_without_match = bidict[key]["no-suffix"].split('-')[0].replace(bidict[key]["prefix"],'')
            #     trg_word_without_match = bidict[key]["no-suffix"].split('-')[1].replace(bidict[key]["prefix"],'')
            #     bidict[key]["no-suffix"] = f'{src_word_without_match}-{trg_word_without_match}'
            # # Whenever the word-pair has not matching characters in front of suffix, but also a prefix, this has to be removed
            # if ("no-prefix" in bidict[key]) and (len(bidict[key]["suffix"]) > 0):
            #     src_word_without_match = bidict[key]["no-prefix"].split('-')[0].replace(bidict[key]["suffix"],'')
            #     trg_word_without_match = bidict[key]["no-prefix"].split('-')[1].replace(bidict[key]["suffix"],'')
            #     bidict[key]["no-prefix"] = f'{src_word_without_match}-{trg_word_without_match}'

            if ("no-suffix" in bidict[key]) and (len(bidict[key]["prefix"]) > 0):
                 src_word_without_match = bidict[key]["no-suffix"].split('-')[0].replace(bidict[key]["prefix"],'')
                 trg_word_without_match = bidict[key]["no-suffix"].split('-')[1].replace(bidict[key]["prefix"],'')
                 bidict[key]["no-fix"] = f'{src_word_without_match}-{trg_word_without_match}'

        # TODO: Access infixes in the middle of the word too!
        # NOTE: The code below would result in infixes which do NOT match between words-
        #       The prefixes and suffices from above DO match though. → This would just lead to confusion and chaos!!
        # Identify infixes
        # for key in bidict.keys():
        #     # Whenever the word-pair has equal entries for "no-prefix" and "no-suffix", then we found an infix
        #     if ("no-suffix" in bidict[key]) and ("no-prefix" in bidict[key]):
        #         src_word_without_match = bidict[key]["no-suffix"].split('-')[0].replace(bidict[key]["prefix"],'')
        #         trg_word_without_match = bidict[key]["no-suffix"].split('-')[1].replace(bidict[key]["prefix"],'')
        #         bidict[key]["infix"] = bidict[key]["no-suffix"]
        #     # Whenever the word-pair has not matching characters in front of suffix, but also a prefix, this has to be removed
        #     if ("no-prefix" in bidict[key]) and (len(bidict[key]["suffix"]) > 0):
        #         src_word_without_match = bidict[key]["no-prefix"].split('-')[0].replace(bidict[key]["suffix"],'')
        #         trg_word_without_match = bidict[key]["no-prefix"].split('-')[1].replace(bidict[key]["suffix"],'')
        #         bidict[key]["no-prefix"] = f'{src_word_without_match}-{trg_word_without_match}'


        output_filename = os.path.basename(dict_file).split('.')[0]
        write_to_json(args.output_dir, output_filename, bidict)

    print(f'Morphological features have successfully been extracted and written to: {args.output_dir}.')