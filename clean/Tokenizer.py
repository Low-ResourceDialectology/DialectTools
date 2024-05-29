# Tokenize text from input file

""" Use:
cd /media/CrazyProjects/LowResDialectology/DialectTools/clean
source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate
python3 Tokenizer.py -i input_file_path -o output_file_path -l deu -p -t
"""

import argparse
import pandas as pd
import seaborn as sns
import glob
import re
import math
import pathlib
import os
from collections import Counter
import numpy as np
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

parser = argparse.ArgumentParser(description='Textfile Tokenizer')
parser.add_argument('-i', '--input-file', type=str, help='file to be tokenized')
parser.add_argument('-o', '--output-file', type=str, help='file for tokenized text to be saved')
parser.add_argument('-l', '--language', type=str, nargs='*', help='(optional) language of input text', default='eng')
parser.add_argument('-p', '--preprocess', action="store_true", help='preprocessing the text lines i.e. removing http code')
parser.add_argument('-t', '--tokenize', action="store_true", help='tokenize the text lines')


args = parser.parse_args()

print(f'No input language provided!\n (still TODO) Attempt to detect language automatically.\n For time being: Defaulting to eng')
#if args.language == '':
#    print(f'No input language provided!\n (still TODO) Attempt to detect language automatically.\n For time being: Defaulting to eng')

#args.language = "kob"
#args.input_file = f'/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-kmrL-MT__-deuL-Opus-0001/Sockeye-evaluation/T06.kob'
#args.output_file = f'/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-kmrL-MT__-deuL-Opus-0001/Sockeye-evaluation/T06-clean.kob'

""" Check whether directory already exists and create if not """
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
output_directory = os.path.dirname(args.output_file)
dir_maker(output_directory)

# Read files into list as lines
src_lines = []

with open(args.input_file) as f:
    for line in f.readlines():
        src_lines.append(line.rstrip(" \n"))

# transform lists of lines into dataframe

df = pd.DataFrame(src_lines, columns = [args.language])

# text preprocessing
def preprocess(text):
    # lower-case the text lines
    text = str(text).lower()
    
    # remove parenthesized texts
    text = re.sub(r"\(.*?\)", "", text)
    
    # remove brackets
    text = re.sub(r"\[.*?\]", "", text)

    # remove quotation marks
    text = re.sub(r'(\<|\>|"|“|”|„|»|«)*', "", text)

    # remove http websites
    text = re.sub(r"(https?:\/\/)[a-zA-Z1-9_.@?=#\/*]*", "", text)

    # remove other symbols
    text = re.sub(r"(\*|\+|@|#|:|;)*", "", text)
    
    # remove parenthesis again
    text = text.replace("(", "").replace(")", "")

    # trim extra whitespace
    #text = re.sub(r' {2,100}', "", text)
    # TODO: Build it more modular → Introduce an input parameter for truncation

    return text

df[args.language] = df[args.language].apply(preprocess)



# TODO: What happens when I tokenize a tokenized text again? How clever are modern tokenizers?
# tokenize texts
def nltk_tokenize(text):
    tokenized = word_tokenize(text)
    if len(tokenized[-1]) != 1:
        tokenized.append(".")
    return " ".join(tokenized)

df[args.language] = df[args.language].apply(nltk_tokenize)


# Save all data to a single file for training that does not build on cross-validaton
with open(f'{args.output_file}','w') as file:
    for line in df[args.language]:
        file.write(line + "\n")

