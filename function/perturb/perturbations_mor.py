# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Applying replacement rules (morphological)
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


def keep_highest_frequency(json_data):
    result = {}
    for key, sub_dict in json_data.items():
        # Find the sub-key with the highest frequency
        max_key = max(sub_dict, key=sub_dict.get)
        result[key] = max_key
    return result


def read_perturbation_rules(file_dir):
    with open(f'{file_dir}', 'r') as f:
        data = json.load(f)
        # NOTE: For the time being we exclude all possible replacements that do not have the highest frequency
        json_data = keep_highest_frequency(data)
        print(f'Rulebook entries: {len(json_data.keys())}')
        return json_data


# def read_perturbation_rules(handmade_file, dict_files, direction):
#     """ Read bidicts from multiple files and combine into one """
#     bidict = {}
#     if direction == 'language2variant':
#         with open(handmade_file,'r', encoding='utf-8') as in_f:
#             for line in in_f.readlines():
#                 variant, language = line.split(',')
#                 bidict[normalize_text(language.strip())] = normalize_text(variant.strip())
        
#         for dict_file in dict_files:
#             with open(dict_file, 'r', encoding='utf-8') as csv_file:
#                 csv_reader = csv.reader(csv_file)
#                 next(csv_reader, None)  # skip the headers
#                 for row in csv_reader:
#                     bidict[normalize_text(row[1].strip())] = normalize_text(row[0].strip())
                    
#     elif direction == 'variant2language':
#         with open(handmade_file,'r', encoding='utf-8') as in_f:
#             for line in in_f.readlines():
#                 variant, language = line.split(',')
#                 bidict[normalize_text(variant.strip())] = normalize_text(language.strip())
        
#         for dict_file in dict_files:
#             with open(dict_file, 'r', encoding='utf-8') as csv_file:
#                 csv_reader = csv.reader(csv_file)
#                 next(csv_reader, None)  # skip the headers
#                 for row in csv_reader:
#                     bidict[normalize_text(row[0].strip())] = normalize_text(row[1].strip())
    
#     print(f'Bidict entries for {direction}: {len(bidict.keys())}')
#     return bidict


def read_text(input_file):
    input_text = []
    with open(f'{input_file}', 'r', encoding='utf-8') as in_file:
        for text_line in in_file.readlines():
            normalized_string = normalize_text(text_line.strip())
            input_text.append(normalized_string)
    return input_text


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
    return pattern.sub(lambda match: replacements[normalize_old(normalize_text(match.group(0)))], string)


# def perturb(input_text, rulebook):
#     output_text = []
#     for text_line in input_text:
#         #print(text_line)
#         new_line = multireplace(text_line, rulebook, ignore_case=True)#, word_boundary=' ')
#         output_text.append(new_line)
#     return output_text


# def write_output(content, out_file):
#     with open(out_file, 'w') as out:
#         for line in content:
#             out.write(line+'\n')


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
    parser.add_argument("-n","--multi_perturb", type=str, default="", help="Level of data quality for experiment: naive, clean, informed.") # Optional flag for perturbing lexicographically perturbed data again, but this time morphologically
    parser.add_argument("-e","--data_file_extension", type=str, default="noname", help="Optional file extension for more flexibility during script call.")

    args = parser.parse_args()
    dir_maker(args.output_dir)

    if not args.data_file_extension == "noname":
        source_language_code = args.data_file_extension 
    elif args.src_lang == "deu":
        source_language_code = "de"
    elif args.src_lang == "eng":
        source_language_code = "en"
    else:
        source_language_code = args.src_lang

    #print(args)
    dict_files = glob.glob(f'{args.input_dir}/*-mor.json', recursive = False)
    for dict_file in dict_files:
        # TODO: Change to only use one of the dictionary-files and print warning if more than 1 exists

        # Read perturbation rules
        rulebook = read_perturbation_rules(dict_file)

        # Select correct text files to perturb
        text_files = glob.glob(f'{args.data_dir}/*.{source_language_code}', recursive = False)

        # Read input text and perturb line by line
        for text_file in text_files:
            out_text_file_name = os.path.basename(text_file)
            out_text_file = f'{args.output_dir}/{out_text_file_name}'
            print(f'Processing file: {text_file}')
            # Open the output file to write text lines to
            with open(out_text_file, 'w') as out_file:
            
                # Open the input file with text lines
                with open(text_file, 'r') as in_file:

                    # Iterate over each line in the input file
                    for input_line in in_file:
                    # Read line-by-line
                    #input_line = in_file.readline()
                    
                        # Replace text units in text line
                        perturbed_line = multireplace(input_line, rulebook, ignore_case=True).replace('\n','') #, word_boundary=' ')
                        #print(f'Perturbed: {perturbed_line}')
                        # Write text line to out file
                        out_file.write(f'{perturbed_line}\n')
            print(f'Applied morphological replacements, writing to: \n{args.output_dir}/{out_text_file_name}')
    print(f'End of script for morphological replacement application.')
    #print(f'Morphological perturbations have successfully been applied and written to: {args.output_dir}.')
