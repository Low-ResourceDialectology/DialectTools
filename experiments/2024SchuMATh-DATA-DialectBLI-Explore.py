# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Lower-case the text data of DialectBLI

import argparse
import csv
import json
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

def compare_text_files(bli_bitext_file, wikidump_dialect_file, dialect_name):
    
    # f1 = open(bli_bitext_file, "r")  NOTE: csv file with Dialect text in first column
    # f1_data = f1.readlines()
    f1_data = []
    with open(bli_bitext_file, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                f1_data.append(row[0])
    
    f2 = open(wikidump_dialect_file, "r")  
    f2_data = f2.readlines()

    #print(f'Printing lines for {dialect_name}')
    # print("\t\tFile 1")
    # for line in f1_data[0:5]:
    #     print(line)
    # print("\t\tFile 2")
    # for line in f2_data[0:5]:
    #     print(line.replace('\n',''))

    #print(f'Comparing DialectBLI with {dialect_name}')
    num_identical = 0
    num_different = 0
    #i = 0
    
    for line1 in f1_data:
        #i += 1
        if line1.replace('\n','') in f2_data:
            num_identical = num_identical + 1
        else:
            num_different = num_different + 1

    print(f'Number of lines in DialectBLI file: {len(f1_data)}')
    print(f'Number of lines in wikidump file of {dialect_name}: {len(f2_data)}')
    print(f'Number of identical lines: {num_identical}')
    print(f'Number of different lines: {num_different}')

    #f1.close()                                       
    f2.close() 



def compare_word_files(bli_bidict_file, wikidump_dialect_file, dialect_name):
    f1_data = []
    with open(bli_bidict_file, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                f1_data.append(row[0])
    
    f2_data = []
    with open(wikidump_dialect_file, 'r') as f:
        data = json.load(f)
        for key in data.keys():
            f2_data.append(key)
             

    # print(f'Printing lines for {dialect_name}')
    # print("\t\tFile 1")
    # for line in f1_data[0:3]:
    #     print(line)
    # print("\t\tFile 2")
    # for line in f2_data[0:3]:
    #     print(line.replace('\n',''))

    #print(f'Comparing DialectBLI with {dialect_name}')
    num_identical = 0
    num_different = 0
    #i = 0
    
    for line1 in f1_data:
        #i += 1
        if line1.replace('\n','') in f2_data:
            num_identical = num_identical + 1
        else:
            num_different = num_different + 1

    print(f'Number of words in DialectBLI file: {len(f1_data)}')
    print(f'Number of words in wikidump file of {dialect_name}: {len(f2_data)}')
    print(f'Number of identical words: {num_identical}')
    print(f'Number of different words: {num_different}')


def compare_word_in_text_files(bli_bitext_file, wikidump_dialect_file, dialect_name, log_dir):
    logging_file = f'{log_dir}/wikidump_dialect_words_contained_DialectBLI-{dialect_name}.txt'
    f1_data = []
    with open(bli_bitext_file, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                f1_data.append(row[0])
    
    f2_data = []
    with open(wikidump_dialect_file, 'r') as f:
        data = json.load(f)
        for key in data.keys():
            f2_data.append(key)
             

    # print(f'Printing lines for {dialect_name}')
    # print("\t\tFile 1")
    # for line in f1_data[0:3]:
    #     print(line)
    # print("\t\tFile 2")
    # for line in f2_data[0:3]:
    #     print(line.replace('\n',''))

    #print(f'Comparing DialectBLI with {dialect_name}')
    num_included_words = 0
    num_inclusions = 0
    num_not_included = 0
    #i = 0
    actual_words = []
    
    for word in f2_data:
        included_word = False
        #i += 1
        for line in f1_data:
            if word.replace('\n','') in line:
                num_inclusions = num_inclusions + 1
                actual_words.append(word)
                included_word = True
        if included_word:
            num_included_words = num_included_words + 1
        else:
            num_not_included = num_not_included + 1

    actual_words = list(set(actual_words))
    # print(f' ---- ')
    # print(f'Number of lines in DialectBLI file: {len(f1_data)}')
    # print(f'Number of words in wikidump file of {dialect_name}: {len(f2_data)}')
    # print(f'Number of words that can be found in text lines: {num_included_words}')
    # print(f'Number of occurences of words across all lines: {num_inclusions}')
    # print(f'Number of words that are not in the text lines: {num_not_included}')
    # print(f'The actual words that are in the text lines: \n{actual_words}')

    with open(logging_file, 'w') as out_file:
        out_file.write(f'Number of lines in DialectBLI file: {len(f1_data)}\n')
        out_file.write(f'Number of words in wikidump file of {dialect_name}: {len(f2_data)}\n')
        out_file.write(f'Number of words that can be found in text lines: {num_included_words}\n')
        out_file.write(f'Number of occurences of words across all lines: {num_inclusions}\n')
        out_file.write(f'Number of words that are not in the text lines: {num_not_included}\n')
        out_file.write(f'The actual words that are in the text lines: \n{actual_words}\n')



def filter_and_extract_dialectBLI(bli_bitext_file, wikidump_dialect_file, dialect_name, output_file):
    pass



# # Explore DialectBLI-Wikidump overlap prior to filtering (bitexts)
# language_name = "Bavarian"
# language_code = "bar"
# bli_bitext_file = f'/media/AllBlue/LanguageData/CLEAN/{language_name}/2023ArteDial-{language_code}L-BiTe-deuL-Lower.csv'
# wikidump_dialect_names = [
#     'Northern_Bavarian', 'Eastern_Central_Bavarian', 'Southern_Bavarian', 'Western_Central_Bavarian'
# ]
# # wikidump_text_files = [
# #     f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-Northern_Bavarian-file.txt',
# #     f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-Eastern_Central_Bavarian-file.txt',
# #     f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-Southern_Bavarian-file.txt',
# #     f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-Western_Central_Bavarian-file.txt'
# # ]

# for dialect_name in wikidump_dialect_names:
#     wikidump_dialect_file = f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-{dialect_name}-file.txt'

#     compare_text_files(bli_bitext_file, wikidump_dialect_file, dialect_name)

# Explore DialectBLI-Wikidump overlap prior to filtering (bidictionaries)
language_name = "Bavarian"
language_code = "bar"
bli_bitext_file = f'/media/AllBlue/LanguageData/CLEAN/{language_name}/2023ArteDial-{language_code}L-BiTe-deuL-Lower.csv'
bli_bidict_file = f'/media/AllBlue/LanguageData/CLEAN/{language_name}/2023ArteDial-{language_code}L-BiDi-deuL-Lower.csv'
wikidump_dialect_names = ['Northern_Bavarian', 'Eastern_Central_Bavarian', 'Southern_Bavarian', 'Western_Central_Bavarian']
#wikidump_dialect_names = ['Bavarian', 'Northern_Bavarian', 'Eastern_Central_Bavarian', 'Southern_Bavarian', 'Western_Central_Bavarian'] # NOTE: Will find A LOT!!!

# wikidump_text_files = [
#     f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-Northern_Bavarian-file.txt',
#     f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-Eastern_Central_Bavarian-file.txt',
#     f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-Southern_Bavarian-file.txt',
#     f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-Western_Central_Bavarian-file.txt'
# ]
# tag_levels = ['silver', 'gold']
# for tag_level in tag_levels:
#     log_dir = f'/media/AllBlue/LanguageData/LOGS/wikidumps-exploring-DialectBLI-{tag_level}'
#     dir_maker(log_dir)

#     for dialect_name in wikidump_dialect_names:
#         print(f'Comparing DialectBLI with {dialect_name}')

        #wikidump_dialect_file = f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/gold/{language_code}/correct-{dialect_name}-file.txt'
        #compare_text_files(bli_bitext_file, wikidump_dialect_file, dialect_name)

        #wikidump_dialect_file = f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/silver/clean-text-freq/{language_code}/new-{dialect_name}-file_word_freq.json'
        #compare_word_files(bli_bidict_file, wikidump_dialect_file, dialect_name)

# tag_levels = ['silver', 'gold']
# for tag_level in tag_levels:
#     log_dir = f'/media/AllBlue/LanguageData/LOGS/wikidumps-exploring-DialectBLI-{tag_level}'
#     dir_maker(log_dir)

#     for dialect_name in wikidump_dialect_names:
#         print(f'Comparing DialectBLI with {dialect_name}')
#         # NOTE: Old path #wikidump_dialect_file = f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/{tag_level}/clean-text-freq/{language_code}/new-{dialect_name}-file_word_freq.json'
#         wikidump_dialect_file = f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/{language_code}/{tag_level}/{dialect_name}.json'
#         compare_word_in_text_files(bli_bitext_file, wikidump_dialect_file, dialect_name, log_dir)


tag_levels = ['silver', 'gold']
for tag_level in tag_levels:
    log_dir = f'/media/AllBlue/LanguageData/LOGS/wikidumps-exploring-DialectBLI-{tag_level}'
    dir_maker(log_dir)

    for dialect_name in wikidump_dialect_names:
        print(f'Comparing DialectBLI with {dialect_name}')

        # Filter and extract data from DialectBLI according to the wikidump-dialect tagged data
        wikidump_dialect_file = f'/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/{language_code}/{tag_level}/{dialect_name}.json'
        output_file = f'/media/AllBlue/LanguageData/CLEAN/{dialect_name}/2024SchuDial-{language_code}L-BiDi-deuL-{tag_level}-Lower.csv'
        filter_and_extract_dialectBLI(bli_bitext_file, wikidump_dialect_file, dialect_name, output_file)





