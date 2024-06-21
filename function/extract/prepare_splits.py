# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Takes various splits (train,dev,test) from separate files (sorted by data source (i.e. Tatoeba)) and combines them into final sets for training.
#   Input: Two (or more) files with the same name, but different extension i.e. "Tatoeba-de-en-dev.de" and "Tatoeba-de-en-dev.en"
#   Output: One file per split: train/dev/test
#   Idea: Optionally process more than two aligned languages at once?

import os
import argparse
from collections import defaultdict

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def remove_existing_output_files(output_path, substrings, extensions):
    for substring in substrings:
        for ext in extensions:
            output_file_name = f"{substring}{ext}"
            output_file_path = os.path.join(output_path, output_file_name)
            if os.path.exists(output_file_path):
                os.remove(output_file_path)

def group_files_by_substring_and_pair(input_path, substrings):
    groups = defaultdict(list)
    extensions = set()

    for file_name in os.listdir(input_path):
        for substring in substrings:
            if substring in file_name:
                base_name, ext = os.path.splitext(file_name)
                groups[base_name].append((file_name, ext))
                extensions.add(ext)
                break
    
    return groups, extensions

def process_and_pool_files(input_path, output_path, substrings):
    groups, extensions = group_files_by_substring_and_pair(input_path, substrings)
    #print(f'Keys of groups: {groups.keys()}') # Debugging
    # Remove existing output files before processing
    remove_existing_output_files(output_path, substrings, extensions)
    
    for base_name, files in groups.items():
        if len(files) != 2:
            print(f"Warning: {base_name} does not have exactly 2 matching files. Skipping.")
            #print(f'{base_name} has: {files}') # Debugging
            continue

        file1, ext1 = files[0]
        file2, ext2 = files[1]

        # Extract substring for naming output files
        for substring in substrings:
            if substring in base_name:
                output_file1 = os.path.join(output_path, f"{substring}{ext1}")
                output_file2 = os.path.join(output_path, f"{substring}{ext2}")
                break
        input_file1 = os.path.join(input_path, file1)
        input_file2 = os.path.join(input_path, file2)

        with open(output_file1, 'a') as out1:
            with open(input_file1, 'r') as in1:
                out1.writelines(in1.readlines())
        with open(output_file2, 'a') as out2:
            with open(input_file2, 'r') as in2:
                out2.writelines(in2.readlines())

        #lines1 = read_file(os.path.join(input_path, file1))
        #lines2 = read_file(os.path.join(input_path, file2))

        # if len(lines1) != len(lines2):
        #     print(f"Warning: Line count mismatch in files {file1} and {file2}. Skipping.")
        #     continue

        #write_file(output_file1, lines1)
        #write_file(output_file2, lines2)

        print(f"Content processed for file pair: '{base_name}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Group files by substrings and extensions, pool their content while maintaining sentence alignment, and write to new files.")
    parser.add_argument("-i","--input_dir", type=str, help="Path to the directory containing text files")
    parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")
    parser.add_argument("-s","--substrings", type=str, help="List of substrings provided as a string to be parsed to group files by")

    args = parser.parse_args()
    print(f'INFO: Provided substrings for file grouping: {args.substrings}')
    substrings = [str(item) for item in args.substrings.split(',')]
    print(f'INFO: Parsed substrings for file grouping: {substrings}')
    try:
        os.makedirs(args.output_dir)
    except FileExistsError:
        # Directory already exists
        pass

    process_and_pool_files(args.input_dir, args.output_dir, substrings)
    print(f'Subsets have been successfully combined and written to: {args.output_dir}.')