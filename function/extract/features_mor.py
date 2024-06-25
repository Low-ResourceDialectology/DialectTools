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


# Read linguistic features (aligned across language pair)
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
            bidict[str(word_counter)]["pair"] = f'{normalize_text(row[0].strip())}-{normalize_text(row[1].strip())}'
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
    parser.add_argument("-c","--context_length", type=str, help="The number of characters to consider as context around the sub-word-units.")

    args = parser.parse_args()
    # TODO: Proper argument types 
    context_length_str = str(args.context_length)
    context_length_int = int(args.context_length)

    dir_maker(args.output_dir)
    dir_maker(f'{args.output_dir}/frequencies')

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

            # If word begins with one of its matches, consider it to be a "matching_prefix"
            matching_prefix = ""
            for match in current_matches:
                if (src_word.startswith(match)) and (trg_word.startswith(match)):
                    matching_prefix = match
                    bidict[key]["matching_prefix"] = matching_prefix

                    # Additionally add the word without the matching prefix
                    src_word_without_match = src_word[len(match):]
                    trg_word_without_match = trg_word[len(match):]
                    bidict[key]["no_prefix"] = f'{src_word_without_match}-{trg_word_without_match}'
                    
                    limiting_length = len(match)-context_length_int
                    src_word_without_match = src_word[limiting_length:]
                    trg_word_without_match = trg_word[limiting_length:]
                    bidict[key][f"no_prefix_{context_length_str}"] = f'{src_word_without_match}-{trg_word_without_match}'

            # If word ends with one of its matches, consider it to be a "matching_suffix"
            matching_suffix = ""
            for match in current_matches:
                if (src_word.endswith(match)) and (trg_word.endswith(match)):
                    matching_suffix = match
                    bidict[key]["matching_suffix"] = matching_suffix

                    # Additionally add the word without the matching suffix
                    src_word_without_match = src_word[:-len(match)]
                    trg_word_without_match = trg_word[:-len(match)]
                    bidict[key]["no_suffix"] = f'{src_word_without_match}-{trg_word_without_match}'
                    
                    limiting_length = len(match)-context_length_int
                    src_word_without_match = src_word[:-limiting_length]
                    trg_word_without_match = trg_word[:-limiting_length]
                    bidict[key][f"no_suffix_{context_length_str}"] = f'{src_word_without_match}-{trg_word_without_match}'

            # NOTE: Why though? # Whenever the word-pair has not matching characters in front of the matching_suffix, but also a matching_prefix, this has to be removed
            # if ("no-suffix" in bidict[key]) and (len(bidict[key]["prefix"]) > 0):
            #     src_word_without_match = bidict[key]["no-suffix"].split('-')[0].replace(bidict[key]["prefix"],'')
            #     trg_word_without_match = bidict[key]["no-suffix"].split('-')[1].replace(bidict[key]["prefix"],'')
            #     bidict[key]["no-suffix"] = f'{src_word_without_match}-{trg_word_without_match}'
            # # Whenever the word-pair has not matching characters in front of suffix, but also a prefix, this has to be removed
            # if ("no-prefix" in bidict[key]) and (len(bidict[key]["suffix"]) > 0):
            #     src_word_without_match = bidict[key]["no-prefix"].split('-')[0].replace(bidict[key]["suffix"],'')
            #     trg_word_without_match = bidict[key]["no-prefix"].split('-')[1].replace(bidict[key]["suffix"],'')
            #     bidict[key]["no-prefix"] = f'{src_word_without_match}-{trg_word_without_match}'

            # For matching prefix and matching suffix in the same pair, we remove both to look for "infixes"
            if ("matching_suffix" in bidict[key]) and ("matching_prefix" in bidict[key]):
                # Remove the matching prefix ignoring the context_length
                limiting_length = len(bidict[key]["matching_prefix"])
                src_word_without_matching_prefix = bidict[key]["pair"].split('-')[0][limiting_length:]
                trg_word_without_matching_prefix = bidict[key]["pair"].split('-')[1][limiting_length:]
                # Remove the matching suffix ignoring the context_length
                limiting_length = len(bidict[key]["matching_suffix"])
                src_word_without_matching_prefix_suffix = src_word_without_matching_prefix[:-limiting_length]
                trg_word_without_matching_prefix_suffix = trg_word_without_matching_prefix[:-limiting_length]
                bidict[key][f"infix"] = f'{src_word_without_matching_prefix_suffix}-{trg_word_without_matching_prefix_suffix}'

            # Again, now considering the context_length
            if ("matching_suffix" in bidict[key]) and ("matching_prefix" in bidict[key]):
                # Remove the matching prefix minus the context_length
                limiting_length = len(bidict[key]["matching_prefix"])-context_length_int
                src_word_without_matching_prefix = bidict[key]["pair"].split('-')[0][limiting_length:]
                trg_word_without_matching_prefix = bidict[key]["pair"].split('-')[1][limiting_length:]
                # Remove the matching suffix minus the context_length
                limiting_length = len(bidict[key]["matching_suffix"])-context_length_int
                src_word_without_matching_prefix_suffix = src_word_without_matching_prefix[:-limiting_length]
                trg_word_without_matching_prefix_suffix = trg_word_without_matching_prefix[:-limiting_length]
                bidict[key][f"infix_{context_length_str}"] = f'{src_word_without_matching_prefix_suffix}-{trg_word_without_matching_prefix_suffix}'

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



        # Count frequencies for the string matches
        # NOTE: Above "no-prefix" denoted the word without a matching prefix, 
        #       which now translates to a suffix-"candidate" (depending on the length of the word, this might result in weird output) 
        infix_freq = {}
        infix_freq_context = {}
        prefix_freq = {}
        prefix_freq_context = {}
        suffix_freq = {}
        suffix_freq_context = {}
        for key in bidict.keys():
            if ("infix" in bidict[key]): 
                pair = bidict[key]["infix"]
                if pair in infix_freq:
                    infix_freq[pair] = infix_freq[pair] + 1
                else:
                    infix_freq[pair] = 1
            
            if (f"infix_{context_length_str}" in bidict[key]): 
                pair = bidict[key][f"infix_{context_length_str}"]
                if pair in infix_freq_context:
                    infix_freq_context[pair] = infix_freq_context[pair] + 1
                else:
                    infix_freq_context[pair] = 1
            
            if ("no_prefix" in bidict[key]): 
                pair = bidict[key]["no_prefix"]
                if pair in suffix_freq:
                    suffix_freq[pair] = suffix_freq[pair] + 1
                else:
                    suffix_freq[pair] = 1
            
            if (f"no_prefix_{context_length_str}" in bidict[key]): 
                pair = bidict[key][f"no_prefix_{context_length_str}"]
                if pair in suffix_freq_context:
                    suffix_freq_context[pair] = suffix_freq_context[pair] + 1
                else:
                    suffix_freq_context[pair] = 1

            if ("no_suffix" in bidict[key]): 
                pair = bidict[key]["no_suffix"]
                if pair in prefix_freq:
                    prefix_freq[pair] = prefix_freq[pair] + 1
                else:
                    prefix_freq[pair] = 1
            
            if (f"no_suffix_{context_length_str}" in bidict[key]): 
                pair = bidict[key][f"no_suffix_{context_length_str}"]
                if pair in prefix_freq_context:
                    prefix_freq_context[pair] = prefix_freq_context[pair] + 1
                else:
                    prefix_freq_context[pair] = 1

        # Save dictionaries to file without sorting to better track the processes
        json_object = json.dumps(infix_freq, indent=4, ensure_ascii=False)
        with open(f'{args.output_dir}/frequencies/{output_filename}-infixes.json', "w") as outfile:
            outfile.write(json_object)
        json_object = json.dumps(infix_freq_context, indent=4, ensure_ascii=False)
        with open(f'{args.output_dir}/frequencies/{output_filename}-infixes_{context_length_str}.json', "w") as outfile:
            outfile.write(json_object)
            
        json_object = json.dumps(prefix_freq, indent=4, ensure_ascii=False)
        with open(f'{args.output_dir}/frequencies/{output_filename}-prefixes.json', "w") as outfile:
            outfile.write(json_object)
        json_object = json.dumps(prefix_freq_context, indent=4, ensure_ascii=False)
        with open(f'{args.output_dir}/frequencies/{output_filename}-prefixes_{context_length_str}.json', "w") as outfile:
            outfile.write(json_object)

        json_object = json.dumps(suffix_freq, indent=4, ensure_ascii=False)
        with open(f'{args.output_dir}/frequencies/{output_filename}-suffixes.json', "w") as outfile:
            outfile.write(json_object)
        json_object = json.dumps(suffix_freq_context, indent=4, ensure_ascii=False)
        with open(f'{args.output_dir}/frequencies/{output_filename}-suffixes_{context_length_str}.json', "w") as outfile:
            outfile.write(json_object)
            
        # Sort frequency dictionaries in descending order
        # sorted_infix_freq = sorted(infix_freq.items(), key=lambda x:x[1], reverse=True)
        # infix_freq_dict = dict(sorted_infix_freq)
        # sorted_infix_freq_context = sorted(infix_freq_context.items(), key=lambda x:x[1], reverse=True)
        # infix_freq_dict_context = dict(sorted_infix_freq_context)

        # sorted_prefix_freq = sorted(prefix_freq.items(), key=lambda x:x[1], reverse=True)
        # prefix_freq_dict = dict(sorted_prefix_freq)
        # sorted_prefix_freq_context = sorted(prefix_freq_context.items(), key=lambda x:x[1], reverse=True)
        # prefix_freq_dict_context = dict(sorted_prefix_freq_context)

        # sorted_suffix_freq = sorted(suffix_freq.items(), key=lambda x:x[1], reverse=True)
        # suffix_freq_dict = dict(sorted_suffix_freq)
        # sorted_suffix_freq_context = sorted(suffix_freq_context.items(), key=lambda x:x[1], reverse=True)
        # suffix_freq_dict_context = dict(sorted_suffix_freq_context)

        # Serializing json and write to file
        # json_object = json.dumps(infix_freq_dict, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-infixes.json', "w") as outfile:
        #     outfile.write(json_object)
        # json_object = json.dumps(infix_freq_dict_context, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-infixes_{context_length_str}.json', "w") as outfile:
        #     outfile.write(json_object)
            
        # json_object = json.dumps(prefix_freq_dict, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-prefixes.json', "w") as outfile:
        #     outfile.write(json_object)
        # json_object = json.dumps(prefix_freq_dict_context, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-prefixes_{context_length_str}.json', "w") as outfile:
        #     outfile.write(json_object)

        # json_object = json.dumps(suffix_freq_dict, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-suffixes.json', "w") as outfile:
        #     outfile.write(json_object)
        # json_object = json.dumps(suffix_freq_dict_context, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-suffixes_{context_length_str}.json', "w") as outfile:
        #     outfile.write(json_object)
        
        # json_object = json.dumps(match_freq_dict, indent=4, ensure_ascii=False)
        # with open(f'{args.output_dir}/frequencies/{output_filename}-matches.json', "w") as outfile:
        #     outfile.write(json_object)
        

    print(f'Morphological features have successfully been extracted and written to: {args.output_dir}.')