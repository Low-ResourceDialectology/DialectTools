# Author: Christian "Doofnase" Schuler
#######################################
# Project: Untangling Language Data
# Sampling (a subset of the Bavarian wikidump) dialect text data for Tangle-Application

# NOTE: Usage:
# python3 2024SchuTang_barL-Wikidump-Input.py \
# --input_dirs /media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/gold /media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/silver \
# --output_dir /media/AllBlue/LanguageData/PROJECTS/2024SchuTang/input \
# --num_lines 1000 \
# --sampling_option equally
# python3 2024SchuTang_barL-Wikidump-Input.py --input_dirs /media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar --output_dir /media/AllBlue/LanguageData/PROJECTS/2024SchuTang/input --num_lines 1000 --sampling_option equally
# python3 2024SchuTang_barL-Wikidump-Input.py --input_dirs /media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar --output_dir /media/AllBlue/LanguageData/PROJECTS/2024SchuTang/input --num_lines 1000 --sampling_option proportionally

import os
import random
import argparse
import pathlib

# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def sample_lines_equally(files, num_lines_per_file):
    sampled_lines = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < num_lines_per_file:
                sampled_lines[file] = lines
            else:
                sampled_lines[file] = random.sample(lines, num_lines_per_file)
    return sampled_lines

def sample_lines_proportionally(files, num_lines_per_file):
    total_lines = len(files) * num_lines_per_file
    total_file_lines = {file: sum(1 for _ in open(file, 'r', encoding='utf-8')) for file in files}
    total_available_lines = sum(total_file_lines.values())
    sampled_lines = {}
    
    for file, num_lines in total_file_lines.items():
        proportion = num_lines / total_available_lines
        num_sample_lines = int(proportion * total_lines)
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < num_sample_lines:
                sampled_lines[file] = lines
            else:
                sampled_lines[file] = random.sample(lines, num_sample_lines)
    return sampled_lines

def save_sampled_lines(sampled_lines, output_dir, sampling_option):
    for file, lines in sampled_lines.items():
        file_dir = os.path.basename(os.path.dirname(file))
        file_basename = os.path.basename(file)
        file_name = f'{file_dir}/{sampling_option}/{file_basename}'
        #relative_path = os.path.relpath(file)
        output_file_path = os.path.join(output_dir, file_name)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

def main(input_dirs, output_dir, num_lines, sampling_option):
    dir_maker(output_dir)
    files = []
    for input_dir in input_dirs:
        for root, _, filenames in os.walk(input_dir):
            for filename in filenames:
                if filename.endswith('.txt'):
                    files.append(os.path.join(root, filename))

    if sampling_option == 'equally':
        sampled_lines = sample_lines_equally(files, num_lines)
    elif sampling_option == 'proportionally':
        sampled_lines = sample_lines_proportionally(files, num_lines)
    else:
        raise ValueError("Invalid sampling option. Choose either 'equally' or 'proportionally'.")

    save_sampled_lines(sampled_lines, output_dir, sampling_option)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample lines from text files in directories")
    parser.add_argument('--input_dirs', nargs='+', required=True, help="Input directories containing text files")
    parser.add_argument('--output_dir', required=True, help="Output directory to save sampled text files")
    parser.add_argument('--num_lines', type=int, required=True, help="Number of lines to sample from each file")
    parser.add_argument('--sampling_option', choices=['equally', 'proportionally'], required=True, help="Sampling option: 'equally' or 'proportionally'")

    args = parser.parse_args()

    main(args.input_dirs, args.output_dir, args.num_lines, args.sampling_option)
