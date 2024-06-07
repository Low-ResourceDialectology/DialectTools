# -*- coding: utf8 -*-

# Plot the counted text content

# Use
"""
source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

python3 /stats/stats_viewer.py --input-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned \
    --log-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned-plots/ --output-file als --mode all
python3 /stats/stats_viewer.py --input-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned \
    --log-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned-plots/ --output-file bar --mode all
    
python3 ./stats/stats_viewer.py --input-dir /media/AllBlue/LanguageData/LOGS/DialectBLI \
    --log-dir /media/AllBlue/LanguageData/LOGS/DialectBLI-plots/ --output-file als --mode all --language als
python3 ./stats/stats_viewer.py --input-dir /media/AllBlue/LanguageData/LOGS/DialectBLI \
    --log-dir /media/AllBlue/LanguageData/LOGS/DialectBLI-plots/ --output-file bar --mode all --language bar
"""

import argparse
import glob
import json
import matplotlib.pyplot as plt
import os
import sys

def plot_text_counts(in_dir, log_dir, out_file, mode, language):
    """Reads the JSON log file and plots the text counts."""
    try:
        with open(f'{in_dir}/{language}.json', 'r', encoding='utf-8') as file:
            text_counts = json.load(file)
        
        files = list(text_counts.keys())
        num_lines = [text_counts[file]['lines'] for file in files]
        num_words = [text_counts[file]['words'] for file in files]
        num_chars = [text_counts[file]['characters'] for file in files]
        
        # Plotting the data
        plt.figure(figsize=(10, 6))

        plt.subplot(1, 1, 1)
        plt.bar(files, num_lines, color='b')
        plt.ylabel('Number of Lines')
        plt.title('Text Counts per File')
        plt.xticks(rotation=90)

        # plt.subplot(3, 1, 2)
        # plt.bar(files, num_words, color='g')
        # plt.ylabel('Number of Words')
        # plt.xticks(rotation=90)

        # plt.subplot(3, 1, 3)
        # plt.bar(files, num_chars, color='r')
        # plt.ylabel('Number of Characters')
        # plt.xlabel('Files')
        # plt.xticks(rotation=90)

        plt.tight_layout()
        plt.savefig(f'{log_dir}/{out_file}.png', bbox_inches='tight')
        #plt.show()

    except Exception as e:
        print(f"Error reading JSON file or plotting data: {e}")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Get text statistics')
    parser.add_argument('-i','--input-dir', type=str, help='input directory')
    parser.add_argument('-l','--log-dir', type=str, help='logging directory')
    parser.add_argument('-o','--output-file', type=str, help='output filename')
    parser.add_argument('-m','--mode', type=str, help='counting mode', default="all")
    parser.add_argument('-c','--language', type=str, help='languegcode of log file')

    args = parser.parse_args()
    
    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)
    if os.path.isdir(args.input_dir):
        plot_text_counts(args.input_dir, args.log_dir, args.output_file, args.mode, args.language)
        #read_files = glob.glob(f'{args.input_dir}*.json')
        #for in_file in read_files:
        #    plot_text_counts(in_file, args.log_dir, args.output_file, args.mode)
    else:
        print(f"The provided path '{args.input_dir}' is not a valid directory.")
