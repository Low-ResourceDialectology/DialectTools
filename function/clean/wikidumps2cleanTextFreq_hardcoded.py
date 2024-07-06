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
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_word_freq.json")
            save_word_freq(word_freq, output_path)
            print(f"Processed {filename} and saved word frequency to {output_path}")
        elif filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            word_freq = process_txt_file(file_path)
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_word_freq.json")
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


    # NOTE: First run based on pre-tagged wikidump article data
    # input_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar'
    # output_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq/bar'
    # main(input_dir, output_dir)

    # NOTE: Second run based on the newly-tagged wikidump article data
    input_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/silver/bar'
    output_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/silver/clean-text-freq/bar'
    main(input_silver_dir, output_silver_dir)
