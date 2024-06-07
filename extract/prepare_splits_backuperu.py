# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Takes various splits (train,dev,test) from separate files (sorted by data source (i.e. Tatoeba)) and combines them into final sets for training.
#   Input: Two (or more) files with the same name, but different extension i.e. "Tatoeba-de-en-dev.de" and "Tatoeba-de-en-dev.en"
#   Output: One file per split: train/dev/test
#   Idea: Optionally process more than two aligned languages at once?

import argparse
from collections import defaultdict
import csv
import json
import logging
import numpy as np
import os
#import pandas as pd
import random
import sys


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_file(file_path, lines, mode='w'):
    with open(file_path, mode, encoding='utf-8') as f:
        f.writelines(lines)

def remove_existing_output_files(input_path, output_path, substrings, extensions):
    for substring in substrings:
        for ext in extensions:
            output_file_name = f"{substring}{ext}"
            output_file_path = os.path.join(output_path, output_file_name)
            if os.path.exists(output_file_path):
                os.remove(output_file_path)

def group_files_by_substring_and_extension(input_path, substrings):
    groups = defaultdict(lambda: defaultdict(list))
    extensions = set()
    
    for file_name in os.listdir(input_path):
        base_name, ext = os.path.splitext(file_name)
        for substring in substrings:
            if substring in base_name:
                groups[substring][ext].append(file_name)
                extensions.add(ext)
                break
    return groups, extensions

def process_and_pool_files(input_path, output_path, substrings):
    groups, extensions = group_files_by_substring_and_extension(input_path, substrings)

    # Remove existing output files
    remove_existing_output_files(input_path, output_path, substrings, extensions)
    
    for substring, ext_dict in groups.items():
        max_lines = max(len(read_file(os.path.join(input_path, file))) for files in ext_dict.values() for file in files)
        
        for i in range(max_lines):
            pooled_sentences = defaultdict(list)
            for ext, files in ext_dict.items():
                for file_name in files:
                    file_path = os.path.join(input_path, file_name)
                    lines = read_file(file_path)
                    if i < len(lines):
                        pooled_sentences[ext].append(lines[i])
            
            # Write the pooled content to a new output file for each extension
            for ext, sentences in pooled_sentences.items():
                output_file_name = f"{substring}_pooled{ext}"
                output_file_path = os.path.join(output_path, output_file_name)
                write_file(output_file_path, sentences, mode='a')
        
        print(f"Pooled content written for group '{substring}'")

    # for substring, ext_dict in groups.items():
    #     combined_lines = defaultdict(list)
    #     file_order = sorted(ext_dict.keys())
    #     for ext in file_order:
    #         files = ext_dict[ext]
    #         for file_name in files:
    #             file_path = os.path.join(input_path, file_name)
    #             lines = read_file(file_path)
    #             combined_lines[ext].append(lines)
    #     num_lines = len(combined_lines[file_order[0]][0])
    #     #NOTE: This makes no sense for more than one datasource! # Ensure all files have the same number of lines
    #     # for ext, lines_list in combined_lines.items():
    #     #     for lines in lines_list:
    #     #         assert len(lines) == num_lines, f"Line count mismatch in files for {substring} with extension {ext}"
    #     # Pool content and maintain sentence alignment
    #     for i in range(num_lines):
    #         pooled_sentences = []
    #         for ext in file_order:
    #             for lines in combined_lines[ext]:
    #                 pooled_sentences.append(lines[i])
    #         # Write the pooled content to a new output file for each extension
    #         for ext in file_order:
    #             output_file_name = f"{substring}{ext}"
    #             output_file_path = os.path.join(output_path, output_file_name)
    #             with open(output_file_path, 'a', encoding='utf-8') as f:
    #                 f.writelines(pooled_sentences[file_order.index(ext)::len(file_order)])
    #             print(f"Pooled content written to {output_file_path}")

# NOTE: Breaking the line-alignments across files!
# def process_and_pool_files(input_path, output_path, substrings):
#     groups = group_files_by_substring_and_extension(input_path, substrings)
#     for substring, ext_dict in groups.items():
#         for ext, files in ext_dict.items():
#             pooled_lines = []    
#             for file_name in files:
#                 file_path = os.path.join(input_path, file_name)
#                 lines = read_file(file_path)
#                 pooled_lines.extend(lines)
#             # Write the pooled content to a new output file
#             output_file_name = f"{substring}{ext}"
#             output_file_path = os.path.join(output_path, output_file_name)
#             write_file(output_file_path, pooled_lines)
#             print(f"Pooled content written to {output_file_path}")
 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Group files by substrings, pool their content, and write to new files.")
    parser.add_argument("-i","--input_dir", type=str, help="Path to the directory containing text files")
    parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")
    parser.add_argument("-s","--substrings", type=str, help="List of substrings provided as a string to be parsed to group files by")

    args = parser.parse_args()
    print(f'INFO: Provided substrings for file grouping: {args.substrings}')
    substrings = [str(item) for item in args.substrings.split(',')]
    print(f'INFO: Prased substrings for file grouping: {substrings}')
    try:
        os.makedirs(args.output_dir)
    except FileExistsError:
        # Directory already exists
        pass

    process_and_pool_files(args.input_dir, args.output_dir, substrings)

    print(f'Subsets have been successfully combined and written to: {args.output_dir}.')