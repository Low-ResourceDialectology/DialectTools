# Based on bidictionaries: Find string matches in aligned words and output all + frequencies in separat files
# 
# Authors: Christian "Doofnase" Schuler, 
###############################################################################

""" Transform Standard German text data into varietie text data """

import argparse
import csv
import json
import os
import unicodedata
import shutil
import sys
import pandas as pd
import glob # For reading multiple txt files and write them into a single file in one go
import re # Regular expressions for replacing strings in files
import pathlib
#from pathlib import Path # Alternative approach for replacing strings in-place
from difflib import SequenceMatcher  
#import Levenshtein 
from collections import defaultdict


parser = argparse.ArgumentParser(description='Merge frequency dictionaries')
parser.add_argument('--match', type=str, help='type of matching substring')
parser.add_argument('--source', type=str, help='source language code')
parser.add_argument('--target', type=str, help='aligned target language code')
parser.add_argument('--exp-dir', type=str, help='output directory for experiment files')
#parser.add_argument('--files', type=str, help='different filenames (temporary fix to include other data)')

# Example:
"""
match="prefix"
src-lang="Bavarian"
trg-lang="German"
clean-dir="/media/AllBlue/LanguageData/CLEAN"
exp-dir="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-Sock-${TARGET}L-DBLI-0001"
"""
args = parser.parse_args()

# Directory containing your JSON files
directory = args.exp_dir

# Defaultdict to store the merged counts
merged_counts = defaultdict(int)

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json') and args.match in filename:
        filepath = os.path.join(directory, filename)
        
        # Open and read the JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Merge counts
            for key, count in data.items():
                merged_counts[key] += count

# Convert the defaultdict back to a regular dictionary
merged_counts = dict(merged_counts)

# Save the merged result to a new JSON file
with open(f'{args.exp_dir}/{args.match}-{args.source}-{args.target}-sum.json', 'w', encoding='utf-8') as f:
    json.dump(merged_counts, f, ensure_ascii=False, indent=4)

print(f'Merged counts have been saved to {args.exp_dir}/{args.match}-{args.source}-{args.target}-sum.json')

