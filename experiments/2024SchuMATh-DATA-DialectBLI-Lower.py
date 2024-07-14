# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Lower-case the text data of DialectBLI

import argparse
import csv
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


def lower_case_textdata(text_data):
    if isinstance(text_data, str):
        lower_text = text_data.lower()
    elif isinstance(text_data, list):
        lower_text = [word.lower() for word in text_data]

    return lower_text


def lower_case_dialectBLI(input_dir, output_dir, language_name, language_code):
    # Lower-casing the Bavarian/Alemannic bitexts
    text_file_list = [
        f'2023ArteDial-{language_code}L-BiTe-deuL-0001.csv',
        f'2023ArteDial-{language_code}L-BiTe-deuL-0002.csv',
        f'2023ArteDial-{language_code}L-BiTe-deuL-0003.csv']

    bitext = []

    for file in text_file_list:
        input_filepath = f'{input_dir}/{file}'
        with open(input_filepath, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                src_low = lower_case_textdata(row[0])
                trg_low = lower_case_textdata(row[1])
                #row_low = row
                row_low = [0, 1]
                row_low[0] = src_low
                row_low[1] = trg_low
                bitext.append(row_low)

    output_filepath = f'{output_dir}/2023ArteDial-{language_code}L-BiTe-deuL-Lower.csv'
    with open(output_filepath, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        # Header
        #csv_writer.writerow(['Bavarian', 'German', 'Meaning', "Factual similarity", "Grammar differs?", "Reasons?"])
        csv_writer.writerow([f'{language_name}', 'German'])
        for out_row in bitext:
            csv_writer.writerow(out_row)

    # Lower-casing the Bavarian/Alemannic bidictionaries
    word_file_list = [
        f'2023ArteDial-{language_code}L-BiDi-deuL-0001.csv',
        f'2023ArteDial-{language_code}L-BiDi-deuL-0002.csv',
        f'2023ArteDial-{language_code}L-BiDi-deuL-0003.csv']
    
    bidict = []

    for file in word_file_list:
        input_filepath = f'{input_dir}/{file}'
        with open(input_filepath, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                src_low = lower_case_textdata(row[0])
                trg_low = lower_case_textdata(row[1])
                #row_low = row
                row_low = [0, 1]
                row_low[0] = src_low
                row_low[1] = trg_low
                bidict.append(row_low)

    output_filepath = f'{output_dir}/2023ArteDial-{language_code}L-BiDi-deuL-Lower.csv'
    with open(output_filepath, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        # Header
        #csv_writer.writerow(['Bavarian', 'German', 'Is translation acceptable?'])
        csv_writer.writerow([f'{language_name}', 'German'])
        for out_row in bidict:
            csv_writer.writerow(out_row)
        



# Paths to the input directory containing CSV files and the output directory
language_name = "Bavarian"
language_code = "bar"
input_dir = f'/media/AllBlue/LanguageData/CLEAN/{language_name}'
output_dir = f'/media/AllBlue/LanguageData/CLEAN/{language_name}'

# Process the directory and lower-case the text data
lower_case_dialectBLI(input_dir, output_dir, language_name, language_code)

print(f"Lower-cased CSV files from {input_dir} and saved text files to {output_dir}")


# Paths to the input directory containing CSV files and the output directory
language_name = "Alemannic"
language_code = "als"
input_dir = f'/media/AllBlue/LanguageData/CLEAN/{language_name}'
output_dir = f'/media/AllBlue/LanguageData/CLEAN/{language_name}'

# Process the directory and lower-case the text data
lower_case_dialectBLI(input_dir, output_dir, language_name, language_code)

print(f"Lower-cased CSV files from {input_dir} and saved text files to {output_dir}")

