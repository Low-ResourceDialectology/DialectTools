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
        print(f'Rulebook entries for lex: {len(json_data.keys())}')
        return json_data


def read_text(input_file):
    input_text = []
    with open(f'{input_file}', 'r', encoding='utf-8') as in_file:
        for text_line in in_file.readlines():
            normalized_string = normalize_text(text_line.strip())
            input_text.append(normalized_string)
    return input_text


def replace_funny_characters(text):
    """Replace long 's' character (ſ) with standard 's'."""
    return text.replace('ſ', 's').replace('ı', 'i')


def normalize_text(text):
    """Normalize text using Unicode NFC normalization."""
    return unicodedata.normalize('NFKD', text)


# NOTE: Moved the preprocessing of replacement dictionaries out of the multi-replace-function for better performance
def preprocess_replacement_dictionary(replacements, ignore_case=False):
    """
    Given a dictionary of replacement rules and a flag if case shall be ignored, it returns the clean replacement rules and mode.
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :param bool ignore_case: whether the match should be case insensitive
    """

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
    rep_escaped = list(map(re.escape, rep_sorted)) # Convert the map object to a list

    # Return the escaped, sorted keys and the regex mode
    return rep_escaped, replacements, re_mode


def multireplace(string, replacements, replacement_dict, replacement_type, replacement_mode):
    """
    Given a string and preprocessed replacement information, it returns the replaced string.
    :param str string: string to execute replacements on
    :param list replacements: list of sorted replacement keys (escaped)
    :param dict replacement_dict: original replacement dictionary {value to find: value to replace}
    :param str replacement_type: type of replacement: "PREFIX", "SUFFIX", or "INFIX"
    :param int replacement_mode: regex mode (case insensitive or not)
    :rtype: str
    """
    if not replacements:
        return string

    # Normalize the input string
    string = normalize_text(string)
    string = replace_funny_characters(string)

    if replacement_type == "PREFIX":
        pattern = re.compile(r'\b(' + '|'.join(replacements) + ')', replacement_mode)
    elif replacement_type == "SUFFIX":
        pattern = re.compile(r'(' + '|'.join(replacements) + r')\b', replacement_mode)
    elif replacement_type == "INFIX":
        pattern = re.compile(r'(?<!\b)(' + '|'.join(replacements) + r')(?!\b)', replacement_mode)
    else:
        raise ValueError("Invalid replacement_type provided!")

    def normalize_old(s):
        return s.lower() if replacement_mode == re.IGNORECASE else s

    return pattern.sub(lambda match: replacement_dict[normalize_old(normalize_text(match.group(0)))], string)


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
    parser.add_argument("-f","--feature_validity", type=str, help="Quality level of the feature sources: guess, reason, authentic.")


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

    dict_files = glob.glob(f'{args.input_dir}/*.json', recursive = False)

    # NOTE: Processing steps for feature_validity = "guess"
    if args.feature_validity == "guess":
        # Processing rules with a context length of 0
        for dict_file in dict_files:
            if dict_file.endswith("-prefixes_0.json"):
                #dict_file = f'{args.input_dir}/*-prefixes_0.json'
                rulebook_prefixes = read_perturbation_rules(dict_file)
            if dict_file.endswith("-suffixes_0.json"):
                #dict_file = f'{args.input_dir}/*-suffixes_0.json'
                rulebook_suffixes = read_perturbation_rules(dict_file)
            if dict_file.endswith("-infixes_0.json"):
                #dict_file = f'{args.input_dir}/*-infixes_0.json'
                rulebook_infixes = read_perturbation_rules(dict_file)


    # NOTE: Processing steps for feature_validity = "reason"
    if args.feature_validity == "reason":
        # Processing replacement-rules with a context length of 1 #TODO: Make the context_length variable
        for dict_file in dict_files:
            if dict_file.endswith("-prefixes_1.json"):
                #dict_file = f'{args.input_dir}/*-prefixes_1.json'
                rulebook_prefixes = read_perturbation_rules(dict_file)
            if dict_file.endswith("-suffixes_1.json"):
                #dict_file = f'{args.input_dir}/*-suffixes_1.json'
                rulebook_suffixes = read_perturbation_rules(dict_file)
            if dict_file.endswith("-infixes_1.json"):
                #dict_file = f'{args.input_dir}/*-infixes_1.json'
                rulebook_infixes = read_perturbation_rules(dict_file)
        
    # Preprocess the replacement rules
    prefix_keys, preprocessed_prefixes, re_mode_prefixes = preprocess_replacement_dictionary(rulebook_prefixes, ignore_case=True)
    suffix_keys, preprocessed_suffixes, re_mode_suffixes = preprocess_replacement_dictionary(rulebook_suffixes, ignore_case=True)
    infix_keys, preprocessed_infixes, re_mode_infixes = preprocess_replacement_dictionary(rulebook_infixes, ignore_case=True)


    # Select correct text files to perturb
    text_files = glob.glob(f'{args.data_dir}/*.{source_language_code}', recursive = False)

    # Read input text and perturb line by line
    for text_file in text_files:
        out_text_file_name = os.path.basename(text_file)
        out_text_file = f'{args.output_dir}/{out_text_file_name}'
        #print(f'Processing file: {text_file}')
        # Open the output file to write text lines to
        with open(out_text_file, 'w') as out_file:
        
            # Open the input file with text lines
            with open(text_file, 'r') as in_file:

                # Iterate over each line in the input file
                for input_line in in_file:
                
                    # Apply the replacements
                    perturbed_line = multireplace(input_line, prefix_keys, preprocessed_prefixes, "PREFIX", re_mode_prefixes).replace('\n','')
                    perturbed_line = multireplace(perturbed_line, suffix_keys, preprocessed_suffixes, "SUFFIX", re_mode_suffixes)
                    perturbed_line = multireplace(perturbed_line, infix_keys, preprocessed_infixes, "INFIX", re_mode_infixes)

                    # Write text line to out file
                    out_file.write(f'{perturbed_line}\n')
        #print(f'Applied morphological replacements, writing to: \n{args.output_dir}/{out_text_file_name}')


        # NOTE: Old version (pre-27.06.2024)
        # # Read input text and perturb line by line
        # for text_file in text_files:
        #     out_text_file_name = os.path.basename(text_file)
        #     out_text_file = f'{args.output_dir}/{out_text_file_name}'
        #     print(f'Processing file: {text_file}')
        #     # Open the output file to write text lines to
        #     with open(out_text_file, 'w') as out_file:
            
        #         # Open the input file with text lines
        #         with open(text_file, 'r') as in_file:

        #             # Iterate over each line in the input file
        #             for input_line in in_file:
        #             # Read line-by-line
        #             #input_line = in_file.readline()
                    
        #                 # Replace text units in text line
        #                 perturbed_line = multireplace(input_line, rulebook, ignore_case=True).replace('\n','') #, word_boundary=' ')
        #                 #print(f'Perturbed: {perturbed_line}')
        #                 # Write text line to out file
        #                 out_file.write(f'{perturbed_line}\n')
        #     print(f'Applied morphological replacements, writing to: \n{args.output_dir}/{out_text_file_name}')
    

    # NOTE: Processing steps for feature_validity = "authentic"
    if args.feature_validity == "authentic":
        print(f'Feature validity level "authentic" not yet implemented.')
    
    print(f'End of script for morphological replacement application.')
    #print(f'Morphological perturbations have successfully been applied and written to: {args.output_dir}.')
