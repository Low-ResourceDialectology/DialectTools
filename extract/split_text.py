# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Takes text content from files and splits it into subsets for training.
#   Input: Two files with the same name, but different extension i.e. "Tatoeba-de-en.de" and "Tatoeba-de-en.en"
#   Output: Depending on chosen "proportions", n-many output files named either according to splits or train/dev/test
#   Idea: Optionally process only a single file with the same outcome for monolingual training approaches?

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

def parse_splits(splits_str):
    splits = [float(x) for x in splits_str.split(",")]
    if not np.isclose(sum(splits), 1.0):
        raise ValueError("Splits must sum to 1.0")
    return splits

def split_sentences(sentences, splits):
    split_indices = (np.cumsum(splits) * len(sentences)).astype(int)
    return np.split(sentences, split_indices[:-1])

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

# def read_sentences_from_file(arguments):
#     sentences = []
#     for filename in os.listdir(directory):
#         if filename.endswith(".csv"):
#             filepath = os.path.join(directory, filename)
#             df = pd.read_csv(filepath)
#             # Assuming sentences are in the second column (index 1)
#             sentences.extend(df.iloc[:, column].dropna().tolist())
#     return sentences

# def write_sentences_to_files(sentences_split, output_dir, splits, language, format):
#     splits_string = splits.replace(',0.','_').replace('0.','') # '0.5,0.3,0.2' → 5_3_2
#     output_dir = f'{output_dir}/{language}-{splits_string}'
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     if format == "txt":
#         for i, sentences in enumerate(sentences_split):
#             output_file = os.path.join(output_dir, f"split_{i + 1}.txt")
#             with open(output_file, 'w') as f:
#                 for sentence in sentences:
#                     f.write(f"{sentence}\n")

# def write_to_txt(out_path, out_file, out_ext, out_data):
#     try:
#         with open(f'{out_path}/{out_file}.{out_ext}', 'w', newline='', encoding='utf-8') as txt_file:
#             pass
#     except Exception as e:
#         logging.error(f"Error writing data to {out_path}/{out_file}.json: {e}")

# TODO: Write a proper function
# def write_to_csv(out_path, out_file, out_data, header, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL):
#     try:
#         with open(f'{out_path}/{out_file}.csv', 'w', newline='', encoding='utf-8') as csv_file:
#             csv_writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
#             # Header
#             csv_writer.writerow(header) # ['Title', 'Text', 'Dialect', 'Sub-Dialect', 'Sub-Sub-Dialect']
#             for out_row in out_data:
#                 csv_writer.writerow(out_row)
#     except Exception as e:
#         logging.error(f"Error writing data to {out_path}/{out_file}.csv: {e}")

# TODO: Write a proper function
# def write_to_json(out_path, out_file, out_data):
#     try:
#         with open(f'{out_path}/{out_file}.json', 'w', newline='', encoding='utf-8') as json_file:
#             pass
#     except Exception as e:
#         logging.error(f"Error writing data to {out_path}/{out_file}.json: {e}")

# TODO: Handle all parameters as dictionary entries instead of lists with indices
# def write_result_to_file(out_data, arguments):
#     """ Write result to file """
#     if arguments["out_type"] == 'txt':
#         write_to_txt(arguments["out_path"], arguments["out_file"], arguments["out_ext"], out_data)
#     elif arguments["out_type"] == 'csv':
#         # For csv, arguments shall be such that:
#         # arguments = [[header1, header2, header3, ...], delimiter, quotechar, quoting]
#         write_to_csv(arguments["out_path"], arguments["out_file"], out_data, arguments[0], arguments[1], arguments[2], arguments[3])
#     elif arguments["out_type"] == 'json':
#         write_to_json(arguments["out_path"], arguments["out_file"], out_data, arguments)
#     else:
#         print(f'Output format not recognized!')
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split sentences from input text files into subsets.")
    parser.add_argument("-i","--input_dir", type=str, help="Directory containing files with text content.")
    parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")
    parser.add_argument("-e","--output_extension", type=str, help="Extension and file format of the output files.")
    parser.add_argument("-s","--src_lang", type=str, help="Language code of source language, part of file naming.")
    parser.add_argument("-t","--trg_lang", type=str, help="Language code of target language, part of file naming.") # TODO: Make optional
    parser.add_argument("-m","--mode", type=str, help="Mode of processing for choosing filenaming-schema: 'default' = train,def,text 'cv' = cross-validation splits (more than 3 output files and different naming)")
    parser.add_argument("-p","--proportions", type=str, help="Comma-separated list of split-proportions (e.g., '0.8,0.1,0.1').")
    #parser.add_argument("--column", type=str, help="Column of CSV files from which to read sentences.") # NOTE: Required only for csv files

    args = parser.parse_args()
    
    try:
        os.makedirs(args.output_dir)
    except FileExistsError:
        # Directory already exists
        pass

    splits = parse_splits(args.proportions)
    splits_string = args.proportions.replace(',0.','_').replace('0.','') # '0.8,0.1,0.1' → 8_1_1
    arguments = {
        "in_dir":args.input_dir,
        "out_dir":args.output_dir,
        "out_ext":args.output_extension,
        "src_lang":args.src_lang,
        "trg_lang":args.trg_lang,
        "mode":args.mode,
        "splits":splits,
        "splits_string":splits_string
    }

    file_pairs = defaultdict(list)
    # Read filenames from input directory to find matching names to create (aligned) pairs
    for file_name in os.listdir(arguments["in_dir"]):
        base_name, ext = os.path.splitext(file_name)
        file_pairs[base_name].append(file_name)

    # Process each file-pair (read content, split into subsets, write to output)
    for base_name, files in file_pairs.items():
        lines1 = []
        lines2 = []
        if len(files) == 2:
            file1, file2 = files
            print(f'Working on files: {file1} \t {file2}')
            base1 = os.path.splitext(file1)[0]
            base2 = os.path.splitext(file2)[0]
            ext1 = os.path.splitext(file1)[1]
            ext2 = os.path.splitext(file2)[1]

            lines1 = read_file(os.path.join(arguments["in_dir"], file1))
            lines2 = read_file(os.path.join(arguments["in_dir"], file2))

            # Ensure both files have the same number of lines
            assert len(lines1) == len(lines2), f"Line count mismatch in files {file1} and {file2}"
            print(f'Line count of these  files {len(lines1)} and {len(lines2)}')

            # Shuffle lines
            combined = list(zip(lines1, lines2))
            random.shuffle(combined)
            lines1, lines2 = zip(*combined)

            # Split data
            src_lines = split_sentences(lines1, splits)
            trg_lines = split_sentences(lines2, splits)

            # Write to files
            if arguments["mode"] == "default":
                # Default-Mode → Train|Dev|Test sets
                write_file(os.path.join(arguments["out_dir"], f'{base1}-train{ext1}'), src_lines[0])
                write_file(os.path.join(arguments["out_dir"], f'{base1}-dev{ext1}'), src_lines[1])
                write_file(os.path.join(arguments["out_dir"], f'{base1}-test{ext1}'), src_lines[2])
                write_file(os.path.join(arguments["out_dir"], f'{base2}-train{ext2}'), trg_lines[0])
                write_file(os.path.join(arguments["out_dir"], f'{base2}-dev{ext2}'), trg_lines[1])
                write_file(os.path.join(arguments["out_dir"], f'{base2}-test{ext2}'), trg_lines[2])
            elif arguments["mode"] == "cv":
                # Cross-Validation-Mode → More than 3 sets
                print(f'Splitting for Cross-Validation has not been implemented yet: Try "default" instead.')
            else:
                print(f'No mode detected: Try "default" instead.')


    # sentences = read_sentences_from_file(input_files, arguments)
    # out_data = split_sentences(sentences, splits)
    # # out_data = resulting data to be saved
    # # arguments = dictionary with arguments such as "out_path", "out_file", "out_ext", "delimiter" (for csv), and more
    # write_result_to_file(out_data, arguments)

    print(f'Sentences have been successfully split and written to: {arguments["out_dir"]}.')