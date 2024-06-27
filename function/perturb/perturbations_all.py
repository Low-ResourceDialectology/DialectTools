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
        print(f'Rulebook entries for mor: {len(data.keys())}')
        return data


def replace_funny_characters(text):
#def replace_long_s_with_s(text):
    """Replace long 's' character (ſ) with standard 's'."""
    return text.replace('ſ', 's').replace('ı', 'i')


def normalize_text(text):
    """Normalize text using Unicode NFC normalization."""
    return unicodedata.normalize('NFKD', text)


def multireplace_words(string, replacements, ignore_case=False, word_boundary=False):
    """
    Given a string and a replacement map, it returns the replaced string.
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :param bool ignore_case: whether the match should be case insensitive
    :param bool word_boundary: whether to replace entire words only
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
    rep_escaped = list(map(re.escape, replacements.keys()))

    # Create a big OR regex that matches any of the substrings to replace
    if word_boundary:
        pattern = re.compile(r'\b(' + '|'.join(rep_escaped) + r')\b', re_mode)
    else:
        pattern = re.compile("|".join(rep_escaped), re_mode)

    # Marking replaced words with special characters
    def replace_func(match):
        key = normalize_old(normalize_text(match.group(0)))
        possible_replacements = replacements[key]
        replacement = random.choice(possible_replacements) if isinstance(possible_replacements, list) else possible_replacements
        return '@@@' + replacement

    return pattern.sub(replace_func, string)


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


def multireplace_substrings(string, replacements, rep_escaped, replacement_type, replacement_mode):
#def multireplace_substrings(string, replacements, replacement_dict, replacement_type, replacement_mode):
    
    #string, replacements, replacement_type, ignore_case=False):
    #(string, replacements, replacement_dict, replacement_type, replacement_mode):
    """
    Replace substrings in a string according to their position (prefix, suffix, infix).
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :param str replacement_type: type of replacement: "PREFIX", "SUFFIX", or "INFIX"
    :param bool ignore_case: whether the match should be case insensitive
    :rtype: str
    """
    if not replacements:
        return string

    string = normalize_text(string)
    string = replace_funny_characters(string)

    if replacement_type == "PREFIX":
        pattern = re.compile(r'\b(' + '|'.join(rep_escaped) + ')', replacement_mode)
    elif replacement_type == "SUFFIX":
        pattern = re.compile(r'(' + '|'.join(rep_escaped) + r')\b', replacement_mode)
    elif replacement_type == "INFIX":
        pattern = re.compile(r'(?<!\b)(' + '|'.join(rep_escaped) + r')(?!\b)', replacement_mode)
    else:
        raise ValueError("Invalid replacement_type provided!")

    def replace_func(match):
        if match.group(0).startswith('@@'):
            return match.group(0)
        key = normalize_text(match.group(0))
        return replacements[key]

    return pattern.sub(replace_func, string)

    # def normalize_old(s):
    #     return s.lower() if replacement_mode == re.IGNORECASE else s

    # def replace_func(match):
    #     if match.group(0).startswith('@@'):
    #         return match.group(0)
    #     key = normalize_old(normalize_text(match.group(0)))
    #     possible_replacements = replacements[key]
    #     return random.choice(possible_replacements) if isinstance(possible_replacements, list) else possible_replacements

    # return pattern.sub(replace_func, string)
# return pattern.sub(lambda match: replacement_dict[normalize_old(normalize_text(match.group(0)))], string)

# def multireplace_substrings(string, replacements, replacement_type, ignore_case=False):
#     """
#     Replace substrings in a string according to their position (prefix, suffix, infix).
#     :param str string: string to execute replacements on
#     :param dict replacements: replacement dictionary {value to find: value to replace}
#     :param str replacement_type: type of replacement: "PREFIX", "SUFFIX", or "INFIX"
#     :param bool ignore_case: whether the match should be case insensitive
#     :rtype: str
#     """
#     if not replacements:
#         return string

#     string = normalize_text(string)
#     string = replace_funny_characters(string)

#     replacements = {normalize_text(key): val for key, val in replacements.items()}

#     if ignore_case:
#         def normalize_old(s):
#             return s.lower()
#         re_mode = re.IGNORECASE
#     else:
#         def normalize_old(s):
#             return s
#         re_mode = 0

#     replacements = {normalize_old(key): val for key, val in replacements.items()}
#     rep_escaped = list(map(re.escape, replacements.keys()))

#     if replacement_type == "PREFIX":
#         pattern = re.compile(r'\b(' + '|'.join(rep_escaped) + ')', re_mode)
#     elif replacement_type == "SUFFIX":
#         pattern = re.compile(r'(' + '|'.join(rep_escaped) + r')\b', re_mode)
#     elif replacement_type == "INFIX":
#         pattern = re.compile(r'(?<!\b)(' + '|'.join(rep_escaped) + r')(?!\b)', re_mode)
#     else:
#         raise ValueError('Invalid replacement_type')

#     def replace_func(match):
#         if match.group(0).startswith('@@'):
#             return match.group(0)
#         key = normalize_old(normalize_text(match.group(0)))
#         possible_replacements = replacements[key]
#         return random.choice(possible_replacements) if isinstance(possible_replacements, list) else possible_replacements

#     return pattern.sub(replace_func, string)


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
    parser.add_argument("-e","--data_file_extension", type=str, default="noname", help="Optional file extension for more flexibility during script call.")
    parser.add_argument("-f","--feature_validity", type=str, help="Quality level of the feature sources: guess, reason, authentic.")

    args = parser.parse_args()
    dir_maker(args.output_dir)

    print(args)

    if not args.data_file_extension == "noname":
        source_language_code = args.data_file_extension 
    elif args.src_lang == "deu":
        source_language_code = "de"
    elif args.src_lang == "eng":
        source_language_code = "en"
    else:
        source_language_code = args.src_lang

    # Lexicographic replacement rules as dictionary from json file.
    dict_files = glob.glob(f'{args.input_dir}/*-lex.json', recursive = False)
    for dict_file in dict_files:
        # TODO: Change to only use one of the dictionary-files and print warning if more than 1 exists

        # Read perturbation rules
        rulebook_lex = read_perturbation_rules(dict_file)

    # Morphological replacement rules as dictionaries from json files.
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


    # NOTE: Processing steps for feature_validity = "authentic"
    if args.feature_validity == "authentic":
        print(f'Feature validity level "authentic" not yet implemented.')


    # Select correct text files to perturb
    text_files = glob.glob(f'{args.data_dir}/*.{source_language_code}', recursive = False)
    #print(f'Text Files: \n {text_files}')

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

                    # Apply the word replacements
                    perturbed_line = multireplace_words(input_line, rulebook_lex, ignore_case=True, word_boundary=True)

                    # Preprocess replacement dictionaries for substrings
                    prefix_keys, re_mode_prefix, prefix_replacements = preprocess_replacement_dictionary(rulebook_prefixes, ignore_case=True)
                    suffix_keys, re_mode_suffix, suffix_replacements = preprocess_replacement_dictionary(rulebook_suffixes, ignore_case=True)
                    infix_keys, re_mode_infix, infix_replacements = preprocess_replacement_dictionary(rulebook_infixes, ignore_case=True)

                    # Apply the substring replacements
                    text = multireplace_substrings(perturbed_line, prefix_keys, prefix_replacements, "PREFIX", re_mode_prefix)
                    text = multireplace_substrings(perturbed_line, suffix_keys, suffix_replacements, "SUFFIX", re_mode_suffix)
                    text = multireplace_substrings(perturbed_line, infix_keys, infix_replacements, "INFIX", re_mode_infix).replace('\n','').replace('@@','')

                    # Write text line to out file
                    out_file.write(f'{perturbed_line}\n')
            #print(f'Applied lexicographic replacements, writing to: \n{args.output_dir}/{out_text_file_name}')
    #print(f'End of script for lexicographic replacement application.')

    