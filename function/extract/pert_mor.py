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
    dir_maker(f'{args.output_dir}')

    dict_files = glob.glob(f'{args.input_dir}/*-mor.json', recursive = False)
    for dict_file in dict_files:
        #bidict = read_bidict(dict_file)
        with open(f'{dict_file}', 'r') as f:
            data = json.load(f)
        replacements = {}
        # "a-u": 301,
        # "ie-y": 291,
        # "a-o": 284,
        #for key_pair in bidict.keys():  # "a-u"
        for pair, freq in data.items():
            if len(pair.split('-')[0]) > 0:
                src = pair.split('-')[0]
            else:
                src = ""
            if len(pair.split('-')[1] > 0):
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
        
        output_filename = os.path.basename(dict_file).split('.')[0]
        write_to_json(args.output_dir, output_filename, replacements)
        
        #bidict = read_bidict(dict_file)
        #print(f'DEBUG: {dict_file}')
        # for key in bidict.keys():
        #     new_id = bidict[key]["pair"]
        #     src_word = new_id.split('-')[0]
        #     trg_word = new_id.split('-')[1]
            
        #     # Find matching strings
        #     current_matches = find_subword_matches(src_word, trg_word)
        #     bidict[key]["matches"] = current_matches

        #     # If word begins with one of its matches, consider it to be a prefix
        #     prefixes = ""
        #     for match in current_matches:
        #         if (src_word.startswith(match)) and (trg_word.startswith(match)):
        #             prefixes = match
        #             bidict[key]["prefix"] = prefixes
        #             # Additionally add the word without the matching prefix
        #             # NOTE: This also removes the match from other positions in the word!
        #             #src_word_without_match = src_word.replace(match,'')
        #             #trg_word_without_match = trg_word.replace(match,'')
        #             # NOTE: This only removes the match at the desired position!
                    
        #             src_word_without_match = src_word[len(match):]
        #             trg_word_without_match = trg_word[len(match):]
        #             bidict[key]["no-prefix"] = f'{src_word_without_match}-{trg_word_without_match}'
                    
        #             limiting_length = len(match)-1
        #             src_word_without_match = src_word[limiting_length:]
        #             trg_word_without_match = trg_word[limiting_length:]
        #             bidict[key]["no-prefix+1"] = f'{src_word_without_match}-{trg_word_without_match}'

        #     # If word ends with one of its matches, consider it to be a suffix
        #     suffixes = ""
        #     for match in current_matches:
        #         if (src_word.endswith(match)) and (trg_word.endswith(match)):
        #             suffixes = match
        #             bidict[key]["suffix"] = suffixes
        #             # Additionally add the word without the matching suffix
        #             #src_word_without_match = src_word.replace(match,'')
        #             #trg_word_without_match = trg_word.replace(match,'')
        #             src_word_without_match = src_word[:-len(match)]
        #             trg_word_without_match = trg_word[:-len(match)]
        #             bidict[key]["no-suffix"] = f'{src_word_without_match}-{trg_word_without_match}'
                    
        #             limiting_length = len(match)-1
        #             src_word_without_match = src_word[:-limiting_length]
        #             trg_word_without_match = trg_word[:-limiting_length]
        #             bidict[key]["no-suffix+1"] = f'{src_word_without_match}-{trg_word_without_match}'

        #     # NOTE: Why though? # Whenever the word-pair has not matching characters in front of suffix, but also a prefix, this has to be removed
        #     # if ("no-suffix" in bidict[key]) and (len(bidict[key]["prefix"]) > 0):
        #     #     src_word_without_match = bidict[key]["no-suffix"].split('-')[0].replace(bidict[key]["prefix"],'')
        #     #     trg_word_without_match = bidict[key]["no-suffix"].split('-')[1].replace(bidict[key]["prefix"],'')
        #     #     bidict[key]["no-suffix"] = f'{src_word_without_match}-{trg_word_without_match}'
        #     # # Whenever the word-pair has not matching characters in front of suffix, but also a prefix, this has to be removed
        #     # if ("no-prefix" in bidict[key]) and (len(bidict[key]["suffix"]) > 0):
        #     #     src_word_without_match = bidict[key]["no-prefix"].split('-')[0].replace(bidict[key]["suffix"],'')
        #     #     trg_word_without_match = bidict[key]["no-prefix"].split('-')[1].replace(bidict[key]["suffix"],'')
        #     #     bidict[key]["no-prefix"] = f'{src_word_without_match}-{trg_word_without_match}'

        #     if ("no-suffix" in bidict[key]) and ("prefix" in bidict[key]):
        #         # Same issue with repeating matches messing up the replacement as above
        #         #src_word_without_match = bidict[key]["no-suffix"].split('-')[0].replace(bidict[key]["prefix"],'')
        #         #trg_word_without_match = bidict[key]["no-suffix"].split('-')[1].replace(bidict[key]["prefix"],'')
        #         limiting_length = len(bidict[key]["prefix"])
        #         src_word_without_match = bidict[key]["no-suffix"].split('-')[0][limiting_length:]
        #         trg_word_without_match = bidict[key]["no-suffix"].split('-')[1][limiting_length:]
        #         bidict[key]["no-fix"] = f'{src_word_without_match}-{trg_word_without_match}'

        # # TODO: Access infixes in the middle of the word too!
        # # NOTE: The code below would result in infixes which do NOT match between words-
        # #       The prefixes and suffices from above DO match though. → This would just lead to confusion and chaos!!
        # # Identify infixes
        # # for key in bidict.keys():
        # #     # Whenever the word-pair has equal entries for "no-prefix" and "no-suffix", then we found an infix
        # #     if ("no-suffix" in bidict[key]) and ("no-prefix" in bidict[key]):
        # #         src_word_without_match = bidict[key]["no-suffix"].split('-')[0].replace(bidict[key]["prefix"],'')
        # #         trg_word_without_match = bidict[key]["no-suffix"].split('-')[1].replace(bidict[key]["prefix"],'')
        # #         bidict[key]["infix"] = bidict[key]["no-suffix"]
        # #     # Whenever the word-pair has not matching characters in front of suffix, but also a prefix, this has to be removed
        # #     if ("no-prefix" in bidict[key]) and (len(bidict[key]["suffix"]) > 0):
        # #         src_word_without_match = bidict[key]["no-prefix"].split('-')[0].replace(bidict[key]["suffix"],'')
        # #         trg_word_without_match = bidict[key]["no-prefix"].split('-')[1].replace(bidict[key]["suffix"],'')
        # #         bidict[key]["no-prefix"] = f'{src_word_without_match}-{trg_word_without_match}'

        # output_filename = os.path.basename(dict_file).split('.')[0]
        # write_to_json(args.output_dir, output_filename, bidict)



        # Count frequencies for the string matches
        #prefix_freq = {}
        #suffix_freq = {}
        #match_freq = {}
        # no_fix_freq = {}
        # no_prefix_freq = {}
        # no_suffix_freq = {}
        # no_prefix_freq_1 = {}
        # no_suffix_freq_1 = {}
        # for key in bidict.keys():
        #     if ("no-fix" in bidict[key]): 
        #         pair = bidict[key]["no-fix"]
        #         if pair in no_fix_freq:
        #             no_fix_freq[pair] = no_fix_freq[pair] + 1
        #         else:
        #             no_fix_freq[pair] = 1
            
        #     if ("no-prefix" in bidict[key]): 
        #         pair = bidict[key]["no-prefix"]
        #         if pair in no_prefix_freq:
        #             no_prefix_freq[pair] = no_prefix_freq[pair] + 1
        #         else:
        #             no_prefix_freq[pair] = 1
            
        #     if ("no-suffix" in bidict[key]): 
        #         pair = bidict[key]["no-suffix"]
        #         if pair in no_suffix_freq:
        #             no_suffix_freq[pair] = no_suffix_freq[pair] + 1
        #         else:
        #             no_suffix_freq[pair] = 1
            
        #     if ("no-prefix+1" in bidict[key]): 
        #         pair = bidict[key]["no-prefix+1"]
        #         if pair in no_prefix_freq_1:
        #             no_prefix_freq_1[pair] = no_prefix_freq_1[pair] + 1
        #         else:
        #             no_prefix_freq_1[pair] = 1

        #     if ("no-suffix+1" in bidict[key]): 
        #         pair = bidict[key]["no-suffix+1"]
        #         if pair in no_suffix_freq_1:
        #             no_suffix_freq_1[pair] = no_suffix_freq_1[pair] + 1
        #         else:
        #             no_suffix_freq_1[pair] = 1

        #     # if (len(bidict[key]["matches"]) > 0):
        #     #     for match in bidict[key]["matches"]:
        #     #         if match in match_freq:
        #     #             match_freq[match] = match_freq[match] + 1
        #     #         else:
        #     #             match_freq[match] = 1
            
        # # Sort frequency dictionaries in descending order
        # sorted_no_fix_freq = sorted(no_fix_freq.items(), key=lambda x:x[1], reverse=True)
        # fix_freq_dict = dict(sorted_no_fix_freq)

        # sorted_no_prefix_freq = sorted(no_prefix_freq.items(), key=lambda x:x[1], reverse=True)
        # prefix_freq_dict = dict(sorted_no_prefix_freq)
        # sorted_no_suffix_freq = sorted(no_suffix_freq.items(), key=lambda x:x[1], reverse=True)
        # suffix_freq_dict = dict(sorted_no_suffix_freq)

        # sorted_no_prefix_freq_1 = sorted(no_prefix_freq_1.items(), key=lambda x:x[1], reverse=True)
        # prefix_freq_dict_1 = dict(sorted_no_prefix_freq_1)
        # sorted_no_suffix_freq_1 = sorted(no_suffix_freq_1.items(), key=lambda x:x[1], reverse=True)
        # suffix_freq_dict_1 = dict(sorted_no_suffix_freq_1)
        
        # # sorted_match_freq = sorted(match_freq.items(), key=lambda x:x[1], reverse=True)
        # # match_freq_dict = dict(sorted_match_freq)
        # # sorted_no_prefix_freq = sorted(no_prefix_freq.items(), key=lambda x:x[1], reverse=True)
        # # no_prefix_freq_dict = dict(sorted_no_prefix_freq)
        # # sorted_no_suffix_freq = sorted(no_suffix_freq.items(), key=lambda x:x[1], reverse=True)
        # # no_suffix_freq_dict = dict(sorted_no_suffix_freq)

        # # Serializing json and write to file
        # json_object = json.dumps(fix_freq_dict, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-fixes.json', "w") as outfile:
        #     outfile.write(json_object)
            
        # json_object = json.dumps(prefix_freq_dict, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-prefixes.json', "w") as outfile:
        #     outfile.write(json_object)
        # json_object = json.dumps(suffix_freq_dict, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-suffixes.json', "w") as outfile:
        #     outfile.write(json_object)

        # json_object = json.dumps(prefix_freq_dict_1, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-prefixes_1.json', "w") as outfile:
        #     outfile.write(json_object)
        # json_object = json.dumps(suffix_freq_dict_1, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-suffixes_1.json', "w") as outfile:
        #     outfile.write(json_object)
        
        # json_object = json.dumps(match_freq_dict, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-matches.json', "w") as outfile:
        #     outfile.write(json_object)
        

    print(f'Morphological replacements have successfully been extracted and written to: {args.output_dir}.')