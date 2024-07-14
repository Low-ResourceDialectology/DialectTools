# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Get word frequency dictionaries for all files from an input directory

import argparse
import os
import csv
import sys
import collections
import json
import shutil

def process_csv_file(file_path):
    word_freq = collections.Counter()
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            if len(row) > 1:
                sentence = row[1]
                words = sentence.split()
                word_freq.update(words)
    
    return word_freq

def process_txt_file(file_path):
    word_freq = collections.Counter()
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        lines = [line for line in file]
        for line in lines:
            if ' ' in line:
                words = line.split()
                word_freq.update(words)
    
    return word_freq

def save_word_freq(word_freq, output_path):
    sorted_word_freq = sorted(word_freq.items(), key=lambda x:x[1], reverse=True)
    word_freq = dict(sorted_word_freq)

    with open(output_path, mode='w', encoding='utf-8') as file:
        json.dump(word_freq, file, indent=4, ensure_ascii=False)

def main(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            word_freq = process_csv_file(file_path)
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0].replace('new-','').replace('correct-','').replace('-file','')}.json")
            save_word_freq(word_freq, output_path)
            print(f"Processed {filename} and saved word frequency to {output_path}")
        elif filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            word_freq = process_txt_file(file_path)
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0].replace('new-','').replace('correct-','').replace('-file','')}.json")
            save_word_freq(word_freq, output_path)
            print(f"Processed {filename} and saved word frequency to {output_path}")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Get word frequency dictionaries')
    # parser.add_argument('-i','--input-dir', type=str, help='input directory')
    # parser.add_argument('-o','--output-dir', type=str, help='output directory')

    # args = parser.parse_args()
    
    # if os.path.isdir(args.input_dir):
    #     main(args.input_dir, args.output_dir)
    # else:
    #     print(f"The provided path '{args.input_dir}' is not a valid directory.")


    # NOTE: Second run based on the newly-tagged (silver) wikidump article data
    input_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/silver'
    output_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/silver'
    main(input_silver_dir, output_silver_dir)
    
    # NOTE: And also for the "golden" texts for consistency
    input_gold_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/gold'
    output_gold_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/gold'
    main(input_gold_dir, output_gold_dir)

    # NOTE: Should now be taken care of by an earlier executed script.
        # # NOTE: Additionally the "golden default Bavarian" based on the assumption, that "untagged articles" denote the "default Bavarian" variant
        # # NOTE: Only single file, not directory-based processing!
        # input_gold_default_file_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar/'
        # input_gold_default_filename = 'UNKNOWN.txt'
        # output_gold_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/gold'

        # # Get word frequencies for the "gold default variant"
        # input_file_path = os.path.join(input_gold_default_file_dir, input_gold_default_filename)
        # word_freq = process_txt_file(input_file_path)
        # output_freq_path = os.path.join(output_gold_dir, "Bavarian.json")
        # save_word_freq(word_freq, output_freq_path)

        # # Also move the text file of the "gold default variant" to the "informed" output directory
        # shutil.copy(input_file_path, f'{output_gold_dir}/Bavarian.txt')

        # print(f"Processed {input_gold_default_filename} and saved word frequency and original text file to {output_gold_dir}")

