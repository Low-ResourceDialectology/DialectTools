# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Get clean text from csv files and write it to txt files for each sub-dialect from wikidumps data

import argparse
import os
import pandas as pd
import pathlib
import re

"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

""" Helper function for text preprocessing """
def preprocess(text):
    # NOTE: Leave this step for later to better compare with DialectBLI data
    #text = str(text).lower()

    # remove line break character
    #text = text.rstrip(" \n")
    text = re.sub(r'\\n', '', text)

    # remove parenthesized texts
    text = re.sub(r"\(.*?\)", "", text)
    
    # remove brackets
    text = re.sub(r"\[.*?\]", "", text)

    # remove quotation marks
    text = re.sub(r'(\<|\>|"|“|”|„|»|«)*', "", text)

    # remove http websites
    text = re.sub(r"(https?:\/\/)[a-zA-Z1-9_.@?=#\/*]*", "", text)

    # remove other symbols
    text = re.sub(r"(\*|\+|@|#|:|;|{|}|\[|\])*", "", text)
    
    # remove parenthesis again
    text = text.replace("(", "").replace(")", "")

    # trim extra whitespace
    text = re.sub(r' {2,100}', "", text)

    # to lowercase 
    text = text.lower()

    return text

def extract_sentences_from_csv(input_path, output_path):
    # Read the CSV file
    df = pd.read_csv(input_path)
    
    # Extract the "Text" column
    sentences = df["Text"].dropna().tolist()
    
    # Generate the output file path
    base_name = os.path.basename(input_path).replace('.csv', '.txt')
    output_file_path = os.path.join(output_path, base_name)
    
    # Write sentences to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for sentence in sentences:
            processed_sentence = preprocess(sentence)
            # Exclude empty lines
            if not len(processed_sentence) < 1:
                file.write(processed_sentence + '\n')

def process_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            input_file_path = os.path.join(input_dir, file_name)
            extract_sentences_from_csv(input_file_path, output_dir)

# Paths to the input directory containing CSV files and the output directory
input_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean/bar'
output_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar'

# Process the directory
process_directory(input_dir, output_dir)

print(f"Processed CSV files from {input_dir} and saved text files to {output_dir}")
