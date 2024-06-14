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
import unicodedata
import pathlib


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
    # Serializing json and write to file
    json_object = json.dumps(output_dictionary, indent=4, ensure_ascii=False)
    try:
        with open(f'{out_path}/{out_file}-lex.json', "w") as json_file:
            json_file.write(json_object)
    except Exception as e:
        logging.error(f"Error writing data to {out_path}/{out_file}.json: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split sentences from CSV files into subsets.")
    parser.add_argument("-i","--input_dir", type=str, help="Directory containing files with replacement rules.")
    parser.add_argument("-d","--data_dir", type=str, help="Directory containing files with text content.")
    parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")
    parser.add_argument("-s","--src_lang", type=str, help="Language code of source language, part of file naming.")
    parser.add_argument("-a","--src_name", type=str, help="Language name of source language, part of file naming.")
    parser.add_argument("-t","--trg_lang", type=str, help="Language code of target language, part of file naming.") # TODO: Make optional
    parser.add_argument("-b","--trg_name", type=str, help="Language name of target language, part of file naming.") # TODO: Make optional
    parser.add_argument("-m","--data_quality", type=str, help="Level of data quality for experiment: naive, clean, informed.")

    args = parser.parse_args()
    dir_maker(args.output_dir)

    replacement_rules = {}
    """
        { 
            "richtete": [
                "gege",
                "hett",
                "richtet"
            ], ...
        }
    """

    dict_files = glob.glob(f'{args.input_dir}/*-lex.json', recursive = False)
    for dict_file in dict_files:
        #bidict = read_bidict(dict_file)
        with open(f'{dict_file}', 'r') as f:
            replacement_rules = json.load(f)
        
        #for index in bidict.keys():  # "a-u"
        for src, trg in data.items():
            # if (len(src) < 1):  # Do not replace empty strings with new content!
            #     continue
            if replacements.get(src,False): 
                replacements[src].append(trg)
            else:
                replacements[src] = [trg]

        output_filename = os.path.basename(dict_file).split('.')[0]
        write_to_json(args.output_dir, output_filename, replacements)

    print(f'Lexicographic replacements have successfully been extracted and written to: {args.output_dir}.')