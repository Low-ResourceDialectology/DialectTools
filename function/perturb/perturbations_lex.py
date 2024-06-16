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
import random
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


def read_perturbation_rules(file_dir):
    with open(f'{file_dir}', 'r') as f:
        data = json.load(f)
        print(f'Rulebook entries: {len(data.keys())}')
        return data


def replace_funny_characters(text):
#def replace_long_s_with_s(text):
    """Replace long 's' character (ſ) with standard 's'."""
    return text.replace('ſ', 's').replace('ı', 'i')


def normalize_text(text):
    """Normalize text using Unicode NFC normalization."""
    #return unicodedata.normalize('NFC', text)
    #return unicodedata.normalize('NFKC', text)
    return unicodedata.normalize('NFKD', text)


def multireplace(string, replacements, ignore_case=False, word_boundary="NONE"):
    """
    Given a string and a replacement map, it returns the replaced string.
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :param bool ignore_case: whether the match should be case insensitive
    :rtype: str
    """
    if not replacements:
        # Edge case that'd produce a funny regex and cause a KeyError
        return string

    # Normalize the input string
    string = normalize_text(string)
    string = replace_funny_characters(string)

    # Normalize the keys in replacements
    replacements = {normalize_text(key): val for key, val in replacements.items()}

    # If case insensitive, we need to normalize the old string so that later a replacement
    # can be found. For instance with {"HEY": "lol"} we should match and find a replacement for "hey",
    # "HEY", "hEy", etc.
    if ignore_case:
        def normalize_old(s):
            return s.lower()

        re_mode = re.IGNORECASE

    else:
        def normalize_old(s):
            return s

        re_mode = 0

    # Apply normalization to the keys for case insensitivity
    replacements = {normalize_old(key): val for key, val in replacements.items()}

    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
    # 'hey ABC' and not 'hey ABc'
    rep_sorted = sorted(replacements, key=len, reverse=True)
    rep_escaped = map(re.escape, rep_sorted)
    
    # Default
    if word_boundary == "NONE":
        # Create a big OR regex that matches any of the substrings to replace
        pattern = re.compile("|".join(rep_escaped), re_mode)

    # TODO: Make it use the given input string as a boundary element → for now: empty space as boundary element
    else:
        pattern = re.compile(r" (" + "|".join(rep_escaped) + r") ", re_mode)
    
    # For each match, look up the new string in the replacements, being the key the normalized old string
    def replace_func(match):
        key = normalize_old(normalize_text(match.group(0)))
        possible_replacements = replacements[key]
        return random.choice(possible_replacements)
    
    return pattern.sub(replace_func, string)

    # NOTE: Previous version which could only handle unambiguous rules with a single option for replacement.
    # For each match, look up the new string in the replacements, being the key the normalized old string
    #return pattern.sub(lambda match: replacements[normalize_old(normalize_text(match.group(0)))], string)


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

    dict_files = glob.glob(f'{args.input_dir}/*-lex.json', recursive = False)
    for dict_file in dict_files:

        # Read perturbation rules
        rulebook = read_perturbation_rules(dict_file)

        # Select correct text files to perturb
        text_files = glob.glob(f'{args.data_dir}/*.{args.src_lang}', recursive = False)

        # Read input text and perturb line by line
        for text_file in text_files:
            out_text_file_name = os.path.basename(text_file)
            out_text_file = f'{args.output_dir}/{out_text_file_name}'
            
            # Open the output file to write text lines to
            with open(out_text_file, 'w') as out_file:
            
                # Open the input file with text lines
                with open(text_file, 'r') as in_file:
                    
                    # Iterate over each line in the input file
                    for input_line in in_file:
                    # Read line-by-line
                    #input_line = in_file.readline()

                        # Replace text units in text line
                        perturbed_line = multireplace(input_line, rulebook, ignore_case=True)#, word_boundary=' ')
                    
                        # Write text line to out file
                        out_file.write(f'{perturbed_line}\n')


    # dict_files = glob.glob(f'{args.input_dir}/*-lex.json', recursive = False)
    # for dict_file in dict_files:
    #     #bidict = read_bidict(dict_file)
    #     with open(f'{dict_file}', 'r') as f:
    #         replacement_rules = json.load(f)
        
    #     #for index in bidict.keys():  # "a-u"
    #     for src, trg in data.items():
    #         # if (len(src) < 1):  # Do not replace empty strings with new content!
    #         #     continue
    #         if replacements.get(src,False): 
    #             replacements[src].append(trg)
    #         else:
    #             replacements[src] = [trg]

    #     output_filename = os.path.basename(dict_file).split('.')[0]
    #     write_to_json(args.output_dir, output_filename, replacements)

    # print(f'Lexicographic replacements have successfully been extracted and written to: {args.output_dir}.')