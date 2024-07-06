# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Based on previously (newly) classify sentences from wikidump data based the dialect-tag-candidates,
# extract and filter the sentences for further processing

import argparse
import os
import glob
import json
import pathlib

"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def extract_sentences_from_json(json_dir, output_dir):
    json_files = glob.glob(f'{json_dir}/*.json')

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        file_name = os.path.basename(json_file).replace('.json', '.txt')
        output_file_path = os.path.join(output_dir, file_name)
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for sentence in data.keys():
                f.write(f"{sentence}\n")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Extract sentences from JSON files and write to TXT files.")
    # parser.add_argument("-i", "--input_dir", type=str, help="Directory containing JSON files with sentences.")
    # parser.add_argument("-o", "--output_dir", type=str, help="Directory to save the output TXT files.")

    # args = parser.parse_args()
    # dir_maker(args.output_dir)
    input_gold_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagcorrect/bar'
    output_gold_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/bar'
    dir_maker(output_gold_dir)
    extract_sentences_from_json(input_gold_dir, output_gold_dir)

    input_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagnew/bar'
    output_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/silver/bar'
    dir_maker(output_silver_dir)
    extract_sentences_from_json(input_silver_dir, output_silver_dir)


    #print(f"Processed JSON files from {input_dir} and saved text files to {output_gold_dir} and to {output_silver_dir}")




