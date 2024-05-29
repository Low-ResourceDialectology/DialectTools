
#source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

# Text preprocessing of parallel data into training corpus splits

import pandas as pd
import seaborn as sns
import glob
import re
import math
import pathlib
from collections import Counter
import langid
import numpy as np
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

# TODO: Input arguments for more versatility
src_l = "kob"
input_file = f'/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-kmrL-MT__-deuL-Opus-0001/Sockeye-evaluation/T06.kob'
output_file = f'/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-kmrL-MT__-deuL-Opus-0001/Sockeye-evaluation/T06-clean.kob'

""" Check whether directory already exists and create if not """
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


# Read files into list as lines
src_lines = []

with open(input_file) as f:
    for line in f.readlines():
        src_lines.append(line.rstrip(" \n"))

# transform lists of lines into dataframe

df = pd.DataFrame(src_lines, columns = [src_l])

# text preprocessing
def preprocess(text):
    # NOTE: Leave this step for later to check for nouns and such
    #text = str(text).lower()
    
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
    text = re.sub(r' {2,100}', "", text)

    return text

df[src_l] = df[src_l].apply(preprocess)



# TODO: What happens when I tokenize a tokenized text again? How clever are modern tokenizers?
# tokenize texts
def nltk_tokenize(text):
    tokenized = word_tokenize(text)
    if len(tokenized[-1]) != 1:
        tokenized.append(".")
    return " ".join(tokenized)

df[src_l] = df[src_l].apply(nltk_tokenize)


# Save all data to a single file for training that does not build on cross-validaton
with open(f'{output_file}','w') as file:
    for line in df[src_l]:
        file.write(line + "\n")

