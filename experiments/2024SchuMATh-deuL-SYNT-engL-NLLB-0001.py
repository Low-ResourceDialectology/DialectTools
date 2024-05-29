# Python Script for transforming text data from standard variant
# 
# Authors: Christian "Doofnase" Schuler, 
###############################################################################

""" Transform Standard German text data into varietie text data """

import csv
import json
import os
import unicodedata
import shutil
import sys
import glob # For reading multiple txt files and write them into a single file in one go
import re # Regular expressions for replacing strings in files
from pathlib import Path # Alternative approach for replacing strings in-place

# TODO: Input arguments for more versatility
src_l = 'bar'
trg_l = 'deu'
#date_of_experiment = '20240524'
#clean_dir = f'/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-deuL-NLLB-engL-NLLB-0001'
prep_dir = f'/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-deuL-NLLB-engL-NLLB-0001' #NOTE: Same as experiment for now
src_train = f'{prep_dir}/train.{src_l}'
src_dev =  f'{prep_dir}/dev.{src_l}'
src_test =  f'{prep_dir}/test.{src_l}'
trg_train = f'{prep_dir}/train.{trg_l}'
trg_dev =  f'{prep_dir}/dev.{trg_l}'
trg_test =  f'{prep_dir}/test.{trg_l}'

# Decide to include subword replacement rules in addition to the bilexicon-based replacement rules 
subwords = True # False
#experiment_dir = "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-barL-SYNT-mult-Opus-0001/Perturbed/Large" # NOTE: Switch here and at bottom of script
experiment_dir = f'/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-deuL-NLLB-engL-NLLB-0001'
version = "non"
if subwords == True:
    version = "mor"
    src_train_out = f'{experiment_dir}/train-mor.{src_l}{trg_l}'
    src_dev_out =  f'{experiment_dir}/dev-mor.{src_l}{trg_l}'
    src_test_out =  f'{experiment_dir}/test-mor.{src_l}{trg_l}'
    trg_train_out = f'{experiment_dir}/train-mor.{trg_l}{src_l}'
    trg_dev_out =  f'{experiment_dir}/dev-mor.{trg_l}{src_l}'
    trg_test_out =  f'{experiment_dir}/test-mor.{trg_l}{src_l}'
else:
    version = "lex"
    src_train_out = f'{experiment_dir}/train-lex.{src_l}{trg_l}'
    src_dev_out =  f'{experiment_dir}/dev-lex.{src_l}{trg_l}'
    src_test_out =  f'{experiment_dir}/test-lex.{src_l}{trg_l}'
    trg_train_out = f'{experiment_dir}/train-lex.{trg_l}{src_l}'
    trg_dev_out =  f'{experiment_dir}/dev-lex.{trg_l}{src_l}'
    trg_test_out =  f'{experiment_dir}/test-lex.{trg_l}{src_l}'



"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    if not os.path.exists(path):
        os.mkdir(path)
        #print("Folder %s created!" % path)
    else:
        #print("Folder %s already exists" % path)
        pass


def replace_funny_characters(text):
#def replace_long_s_with_s(text):
    """Replace long 's' character (ſ) with standard 's'."""
    return text.replace('ſ', 's').replace('ı', 'i')

def normalize_text(text):
    """Normalize text using Unicode NFC normalization."""
    #return unicodedata.normalize('NFC', text)
    #return unicodedata.normalize('NFKC', text)
    return unicodedata.normalize('NFKD', text)

def multireplace(string, replacements, ignore_case=False, word_boundary="NONE"):
    """
    Given a string and a replacement map, it returns the replaced string.
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :param bool ignore_case: whether the match should be case insensitive
    :rtype: str
    """
    if not replacements:
        # Edge case that'd produce a funny regex and cause a KeyError
        return string

    # Normalize the input string
    string = normalize_text(string)
    string = replace_funny_characters(string)

    # Normalize the keys in replacements
    replacements = {normalize_text(key): val for key, val in replacements.items()}

    # If case insensitive, we need to normalize the old string so that later a replacement
    # can be found. For instance with {"HEY": "lol"} we should match and find a replacement for "hey",
    # "HEY", "hEy", etc.
    if ignore_case:
        def normalize_old(s):
            return s.lower()

        re_mode = re.IGNORECASE

    else:
        def normalize_old(s):
            return s

        re_mode = 0

    # Apply normalization to the keys for case insensitivity
    replacements = {normalize_old(key): val for key, val in replacements.items()}

    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
    # 'hey ABC' and not 'hey ABc'
    rep_sorted = sorted(replacements, key=len, reverse=True)
    rep_escaped = map(re.escape, rep_sorted)
    
    # Default
    if word_boundary == "NONE":
        # Create a big OR regex that matches any of the substrings to replace
        pattern = re.compile("|".join(rep_escaped), re_mode)

    # TODO: Make it use the given input string as a boundary element → for now: empty space as boundary element
    else:
        pattern = re.compile(r" (" + "|".join(rep_escaped) + r") ", re_mode)
    
    # For each match, look up the new string in the replacements, being the key the normalized old string
    return pattern.sub(lambda match: replacements[normalize_old(normalize_text(match.group(0)))], string)


# #############################################################################
""" Introduce perturbations into German texts """

handmade_file = f'/media/AllBlue/LanguageData/DOWNLOAD/handmade/Substring-German_bar-deu.txt'
#dicts_path = f'/media/AllBlue/LanguageData/TEST/projects/MA-Thesis/NLLB-deu-bar-als/DICT'
dicts_path = f'/media/AllBlue/LanguageData/CLEAN/Bavarian'
#list_of_source_files = glob.glob(f'{input_path}/*')
# NOTE: Manual list to better debug problematic dict-entries and characters for the time being:
list_of_source_files = [
    src_train,
    trg_train,
    src_dev,
    src_test,
    trg_dev,
    trg_test
]
# Read perturbation rules
def read_perturbation_rules(handmade_file, dict_files, direction, subwords):
    """ Read bidicts from multiple files and combine into one """
    bidict = {}
    if direction == 'language2variant':
        if subwords == True:
            with open(handmade_file,'r', encoding='utf-8') as in_f:
                for line in in_f.readlines():
                    variant, language = line.split(',')
                    bidict[normalize_text(language.strip())] = normalize_text(variant.strip())
        
        for dict_file in dict_files:
            with open(dict_file, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader, None)  # skip the headers
                for row in csv_reader:
                    bidict[normalize_text(row[1].strip())] = normalize_text(row[0].strip())
                    
    elif direction == 'variant2language':
        if subwords == True:
            with open(handmade_file,'r', encoding='utf-8') as in_f:
                for line in in_f.readlines():
                    variant, language = line.split(',')
                    bidict[normalize_text(variant.strip())] = normalize_text(language.strip())
        
        for dict_file in dict_files:
            with open(dict_file, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader, None)  # skip the headers
                for row in csv_reader:
                    bidict[normalize_text(row[0].strip())] = normalize_text(row[1].strip())
    
    print(f'Bidict entries for {direction}: {len(bidict.keys())}')
    return bidict

# Read text file
def read_text(input_file):
    input_text = []
    with open(f'{input_file}', 'r', encoding='utf-8') as in_file:
        for text_line in in_file.readlines():
            normalized_string = normalize_text(text_line.strip())
            input_text.append(normalized_string)
    return input_text

# Perturb
def perturb(input_text):
    output_text = []
    for text_line in input_text:
        #print(text_line)
        new_line = multireplace(text_line, bidict, ignore_case=True)#, word_boundary=' ')
        output_text.append(new_line)
    return output_text

# Write output file
def write_output(content, out_file):
    with open(out_file, 'w') as out:
        for line in content:
            out.write(line+'\n')


###############################################################################
# Including all Bidictionaries for more volume, but also getting more noise.
# → Saved in the subdirectory /Perturbed/Large/
#dict_files = [f'{dicts_path}/2023ArteDial-barL-BiDi-deuL-0003.csv',f'{dicts_path}/2023ArteDial-barL-BiDi-deuL-0002.csv',f'{dicts_path}/2023ArteDial-barL-BiDi-deuL-0001.csv']

# direction = 'language2variant' # variant2language
# bidict = read_perturbation_rules(handmade_file, dict_files, direction)
# # Serializing json and write to file
# json_object = json.dumps(bidict, indent=4, ensure_ascii=False)
# with open(f'{experiment_dir}/bidict-{direction}.json', "w") as outfile:
#     outfile.write(json_object)

# input_text = read_text(trg_test)
# perturbed_text = perturb(input_text)
# write_output(perturbed_text, trg_test_out)

# input_text = read_text(trg_dev)
# perturbed_text = perturb(input_text)
# write_output(perturbed_text, trg_dev_out)

# input_text = read_text(trg_train)
# perturbed_text = perturb(input_text)
# write_output(perturbed_text, trg_train_out)

# direction = 'variant2language' # language2variant
# bidict = read_perturbation_rules(handmade_file, dict_files, direction)
# # Serializing json and write to file
# json_object = json.dumps(bidict, indent=4, ensure_ascii=False)
# with open(f'{experiment_dir}/bidict-{direction}.json', "w") as outfile:
#     outfile.write(json_object)

# input_text = read_text(src_test)
# perturbed_text = perturb(input_text)
# write_output(perturbed_text, src_test_out)

# input_text = read_text(src_dev)
# perturbed_text = perturb(input_text)
# write_output(perturbed_text, src_dev_out)

# input_text = read_text(src_train)
# perturbed_text = perturb(input_text)
# write_output(perturbed_text, src_train_out)




###############################################################################
# Including human-annotated Bidictionaries for less noise, but also getting less volume.
# → Saved in the subdirectory /Perturbed/Medium/
dict_files = [f'{dicts_path}/2023ArteDial-barL-BiDi-deuL-0003.csv',f'{dicts_path}/2023ArteDial-barL-BiDi-deuL-0002.csv']
dict_files_large = [f'{dicts_path}/2023ArteDial-barL-BiDi-deuL-0003.csv',f'{dicts_path}/2023ArteDial-barL-BiDi-deuL-0002.csv',f'{dicts_path}/2023ArteDial-barL-BiDi-deuL-0001.csv']
# NOTE: The large file (0001) contains a lot of noise that deteriorates the text content considerably
# NOTE: subwords = True | False decides about inclusion of subword replacement rules in addition to the bilexicon-based replacement rules 

direction = 'language2variant' # variant2language
bidict = read_perturbation_rules(handmade_file, dict_files, direction, subwords)
# Serializing json and write to file
json_object = json.dumps(bidict, indent=4, ensure_ascii=False)
with open(f'{experiment_dir}/bidict-{direction}-{version}.json', "w") as outfile:
    outfile.write(json_object)

input_text = read_text(trg_test)
perturbed_text = perturb(input_text)
write_output(perturbed_text, trg_test_out)

input_text = read_text(trg_dev)
perturbed_text = perturb(input_text)
write_output(perturbed_text, trg_dev_out)

input_text = read_text(trg_train)
perturbed_text = perturb(input_text)
write_output(perturbed_text, trg_train_out)




direction = 'variant2language' # language2variant
bidict = read_perturbation_rules(handmade_file, dict_files, direction, subwords)
# Serializing json and write to file
json_object = json.dumps(bidict, indent=4, ensure_ascii=False)
with open(f'{experiment_dir}/bidict-{direction}-{version}.json', "w") as outfile:
    outfile.write(json_object)

input_text = read_text(src_test)
perturbed_text = perturb(input_text)
write_output(perturbed_text, src_test_out)

input_text = read_text(src_dev)
perturbed_text = perturb(input_text)
write_output(perturbed_text, src_dev_out)

input_text = read_text(src_train)
perturbed_text = perturb(input_text)
write_output(perturbed_text, src_train_out)


