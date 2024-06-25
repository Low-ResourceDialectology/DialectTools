# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Extracting replacement rules (morphological)
#   Input: (Frequency) Dictionary with linguistic features in json format
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

""" Input files look like:
{
    "e-ä": 2009,
    "e-": 2008,
    "n-": 1814,
    "un-i": 1628,
    "-ch": 1427,
    "-e": 710,
    "e-i": 612,
    "t-d": 576, ...

"""

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


# Write output json file
def write_to_json(out_path, out_file, output_dictionary):
    # TODO: Sort by value
    #sorted_output_dictionary = sorted(output_dictionary.items(), key=lambda x:x:[1], reverse=True)
    #output_dictionary = dict(sorted_output_dictionary)
    
    # Serializing json and write to file
    json_object = json.dumps(output_dictionary, indent=4, ensure_ascii=False)
    try:
        with open(f'{out_path}/{out_file}.json', "w") as json_file:
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
    parser.add_argument("-m","--dict_direction", type=str, help="Switch the order in which the linguistic features are read.")
    parser.add_argument("-f","--feature_validity", type=str, help="Quality level of features to extract.")
    parser.add_argument("-e","--extraction_method", type=str, help="Method of how features were previously processed.")
    parser.add_argument("-n","--unit_frequency", type=str, help="Threshold for occurences, everything under this number will be excluded.")
    parser.add_argument("-l","--unit_length", type=str, help="Threshold for length of the subword-unit, everything not under this number, is excluded.")
    
    args = parser.parse_args()
    frequency_lower_limit = int(args.unit_frequency)
    length_upper_limit = int(args.unit_length)
    
    dir_maker(args.output_dir)
    dir_maker(f'{args.output_dir}')

    if args.feature_validity == "guess":
        global_replacements = {}
        dict_files = glob.glob(f'{args.input_dir}/*.json', recursive = False)
        for dict_file in dict_files:
            
            with open(f'{dict_file}', 'r') as f:
                data = json.load(f)
            replacements = {}

            # Inside the initial word lists, the dialect word was on position 0, while the standard word was on position 1
            # To process these such that the dialect side is the "source" side, use "LeftToRight"
            # For processing such that the standard side is the "source" side, use "RightToLeft" instead.
            if args.dict_direction == "LeftToRight":
                # "a-u": 301,
                # "ie-y": 291,
                # "a-o": 284,
                #for key_pair in bidict.keys():  # "a-u"
                for pair, freq in data.items():
                    if len(pair.split('-')[0]) > 0:
                        src = pair.split('-')[0]
                    else:
                        src = ""
                    if (len(pair.split('-')) > 1): # len(pair.split('-')[1] > 0)
                        trg = pair.split('-')[1]
                    else:
                        trg = ""
                
                    #src, trg = pair.split('-')
                    # NOTE: → ValueError
                    
                    # if (len(src) < 1):  # Do not replace empty strings with new content!
                    #     continue
                    # if replacements.get(src,False): 
                    #     replacements[src].append(trg)
                    # else:
                    #     replacements[src] = [trg]
                    if not src in replacements.keys():
                        replacements[src] = {}
                        replacements[src][trg] = freq
                    else:
                        replacements[src][trg] = freq
                    
                    # Filter for specific requirements to derive all replacement rules
                    if (len(src) < length_upper_limit) and (freq > frequency_lower_limit):
                        if not src in global_replacements.keys():
                            global_replacements[src] = {}
                            global_replacements[src][trg] = freq
                        else:
                            if not trg in global_replacements[src]:
                                global_replacements[src][trg] = freq
                            else:
                                global_replacements[src][trg] = global_replacements[src][trg] + freq
                                #print(f'INFO: Duplicate rule {src} - {trg} adding the value {freq} to {global_replacements[src][trg]}')
            
            elif args.dict_direction == "RightToLeft":
                for pair, freq in data.items():
                    if len(pair.split('-')[0]) > 0:
                        trg = pair.split('-')[0]
                    else:
                        trg = ""
                    if (len(pair.split('-')) > 1): # len(pair.split('-')[1] > 0)
                        src = pair.split('-')[1]
                    else:
                        src = ""
                
                    if not src in replacements.keys():
                        replacements[src] = {}
                        replacements[src][trg] = freq
                    else:
                        replacements[src][trg] = freq
                    
                    # Filter for specific requirements to derive all replacement rules
                    if (len(src) < length_upper_limit) and (freq > frequency_lower_limit):
                        if not src in global_replacements.keys():
                            global_replacements[src] = {}
                            global_replacements[src][trg] = freq
                        else:
                            if not trg in global_replacements[src]:
                                global_replacements[src][trg] = freq
                            else:
                                global_replacements[src][trg] = global_replacements[src][trg] + freq
                                #print(f'INFO: Duplicate rule {src} - {trg} adding the value {freq} to {global_replacements[src][trg]}')
            

            output_filename = os.path.basename(dict_file).split('.')[0]
            write_to_json(args.output_dir, output_filename, replacements)
        output_filename_inter = os.path.basename(dict_files[0]).split('.')[0] # 2023ArteDial-fixes
        output_filename = f'{output_filename_inter.split("-")[0]}-mor' # 2023ArteDial-mor
        write_to_json(args.output_dir, output_filename, global_replacements)

    # A more sophisticated approach to the aggregation of replacement rules
    if args.feature_validity == "reason":
        dict_files = glob.glob(f'{args.input_dir}/*.json', recursive = False)
        for dict_file in dict_files:
            output_name_part = os.path.basename(dict_file)[0].split('.')[0] # 2023ArteDial-infixes
            # if "prefix" in dict_file:
            #     # Process the plain prefix replacements (no context considered)
            #     pass
            # if "prefix_" in dict_file:
            #     # Process the prefix replacements (context considered)
            #     pass
            # if "suffix" in dict_file:
            #     # Process the plain suffix replacements (no context considered)
            #     pass
            # if "prefix_" in dict_file:
            #     # Process the suffix replacements (context considered)
            #     pass
            # if "infix" in dict_file:
            #     # Process the plain infix replacements (no context considered)
            #     pass
            # if "infix_" in dict_file:
            #     # Process the infix replacements (context considered)
            #     pass

            with open(f'{dict_file}', 'r') as f:
                data = json.load(f)
            replacements = {}

            # Inside the initial word lists, the dialect word was on position 0, while the standard word was on position 1
            # To process these such that the dialect side is the "source" side, use "LeftToRight"
            # For processing such that the standard side is the "source" side, use "RightToLeft" instead.
            if args.dict_direction == "LeftToRight":
                # "a-u": 301,
                # "ie-y": 291,
                # "a-o": 284,
                #for key_pair in bidict.keys():  # "a-u"
                for pair, freq in data.items():
                    if len(pair.split('-')[0]) > 0:
                        src = pair.split('-')[0]
                    else:
                        src = ""
                    if (len(pair.split('-')) > 1): # len(pair.split('-')[1] > 0)
                        trg = pair.split('-')[1]
                    else:
                        trg = ""

                    # Filter for specific requirements to derive all replacement rules
                    if (len(src) < length_upper_limit) and (freq > frequency_lower_limit):
                        if not src in replacements.keys():
                            replacements[src] = {}
                            replacements[src][trg] = freq
                        else:
                            replacements[src][trg] = freq
                            
            elif args.dict_direction == "RightToLeft":
                for pair, freq in data.items():
                    if len(pair.split('-')[0]) > 0:
                        trg = pair.split('-')[0]
                    else:
                        trg = ""
                    if (len(pair.split('-')) > 1): # len(pair.split('-')[1] > 0)
                        src = pair.split('-')[1]
                    else:
                        src = ""
                
                    # Filter for specific requirements to derive all replacement rules
                    if (len(src) < length_upper_limit) and (freq > frequency_lower_limit):
                        if not src in replacements.keys():
                            replacements[src] = {}
                            replacements[src][trg] = freq
                        else:
                            replacements[src][trg] = freq

            output_filename = os.path.basename(dict_file).split('.')[0]
            write_to_json(args.output_dir, output_filename, replacements)
        #output_filename_inter = os.path.basename(dict_files[0]).split('.')[0] # 2023ArteDial-fixes
        #output_filename = f'{output_filename_inter.split("-")[0]}-mor' # 2023ArteDial-mor
        #write_to_json(args.output_dir, output_filename, global_replacements)

    print(f'Morphological replacements have successfully been extracted and written to: {args.output_dir}.')