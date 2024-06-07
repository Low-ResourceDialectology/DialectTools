# -*- coding: utf8 -*-

# Count text content and get statistics for them

# Use
"""
python3 /stats/text_counter.py --input-dir /media/AllBlue/LanguageData/CLEAN/wikidumps/clean \
    --log-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned/ --output-file als --mode all
python3 /stats/text_counter.py --input-dir /media/AllBlue/LanguageData/CLEAN/wikidumps/clean \
    --log-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned/ --output-file bar --mode all
    
python3 ./stats/text_counter.py --input-dir /media/AllBlue/LanguageData/CLEAN/Alemannic \
    --log-dir /media/AllBlue/LanguageData/LOGS/DialectBLI/ --output-file als --mode all
python3 ./stats/text_counter.py --input-dir /media/AllBlue/LanguageData/CLEAN/Bavarian \
    --log-dir /media/AllBlue/LanguageData/LOGS/DialectBLI/ --output-file bar --mode all
"""


import argparse
import json
import os
import sys

def count_text_content(file_path):
    """Counts the number of characters, words, and lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            num_chars = len(text)
            num_words = len(text.split())
            num_lines = len(text.splitlines())
        return num_chars, num_words, num_lines
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0, 0, 0

def process_directory(in_dir, log_dir, out_file, mode):
    """Processes all files in the given directory and logs text counts to a JSON file."""
    text_counts = {}
    
    for root, _, files in os.walk(in_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path).split(".")[0]
            num_chars, num_words, num_lines = count_text_content(file_path)
            text_counts[file_name] = {
                'lines': num_lines,
                'words': num_words,
                'characters': num_chars
            }
    #  Sort the text_counts dictionary by 'lines' in descending order
    sorted_text_counts = dict(sorted(text_counts.items(), key=lambda item: item[1]['lines'], reverse=True))

    # Write the counts to a JSON file
    output_file = os.path.join(log_dir, f'{out_file}.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(sorted_text_counts, json_file, ensure_ascii=False, indent=4)
        print(f"Text counts logged to {output_file}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python count_text_content.py <directory_path>")
    # else:
    #   directory_path = sys.argv[1]

    parser = argparse.ArgumentParser(description='Get text statistics')
    parser.add_argument('-i','--input-dir', type=str, help='input directory')
    parser.add_argument('-l','--log-dir', type=str, help='logging directory')
    parser.add_argument('-o','--output-file', type=str, help='output filename')
    parser.add_argument('-m','--mode', type=str, help='counting mode', default="all")

    args = parser.parse_args()
    
    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)
    if os.path.isdir(args.input_dir):
        process_directory(args.input_dir, args.log_dir, args.output_file, args.mode)
    else:
        print(f"The provided path '{args.input_dir}' is not a valid directory.")
