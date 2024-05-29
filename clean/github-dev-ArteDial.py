# cd /media/CrazyProjects/LowResDialectology/DialectData/clean
# source /media/AllBlue/LanguageData/TOOLS/vStanza/bin/activate
# python3 /media/CrazyProjects/LowResDialectology/DialectData/clean/github-dev-ArteDial.py

import csv
import glob
import json
import os
import pathlib
import stanza 

# TODO: Select languages | datasources | ...
# TODO: Callable from outside (create a main.py ?)
# NOTE: For now just "all" as default

# NOTE: Due to inconsistencies among datasets and researcher, each repository will require a manual check-up first.

# TODO: Identify reoccurring patterns and create "cleaning classes" for each to streamline this process across multiple repositories.
# TODO: Create a "cleaning-config" file to store execution-information for this

# def clean_github_repos(config_file_in='./config.json',
#                        sources_file_in='./sources/github_cleaning.json',
#                        data_root_dir_in='/media/AllBlue/LanguageData'):
    
#     config_file = config_file_in
#     sources_file = sources_file_in
#     data_root_dir = f'{data_root_dir_in}/DOWNLOAD/githubrepos'

#     # Default in function-head vs. input-paramter vs. config-file → Who should take precedence?
#     # with open(config_file, 'r') as input_file:
#     #     json_data = json.load(input_file)
#     #     data_root_dir = json_data["data_root_dir"]

#     """ Go through all downloaded repositories and clean if corresponding repo-key found in "cleaning-config" file """

print(f'Script-under-construction: Hard-coded solution for now!')
SOURCE="Alemannic" # "Bavarian" "Alemannic"
SRC_DIR="als" # "bar" "als"
TARGET="German"
TRG_DIR="deu"

print(f'SOURCE: {SOURCE} with SRC_DIR: {SRC_DIR}\n TARGET: {TARGET} with TRG_DIR: {TRG_DIR}')

"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

in_path = f'/media/AllBlue/LanguageData/CLEAN/{SOURCE}'
out_path = f'/media/AllBlue/LanguageData/PREP/2024SchuMATh-{SRC_DIR}L-Sock-{TRG_DIR}L-DBLI-0001'
temp_path = f'/media/AllBlue/LanguageData/PREP/2024SchuMATh-{SRC_DIR}L-Sock-{TRG_DIR}L-DBLI-0001/Temp'
dir_maker(temp_path)
log_info = []

""" Read twice annotated data from DialectBLI for testing """
test_src_trg = []
#src_trg = []
#test_trg = []
with open(f'{in_path}/2023ArteDial-{SRC_DIR}L-BiTe-{TRG_DIR}L-0003.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',',quotechar='"')
    next(csv_reader, None)
    for row in csv_reader:
        test_src_trg.append([row[0], row[1]])
        #test_src.append(row[0])
        #test_trg.append(row[1])
log_info.append(f'Length of {SOURCE} TEST {SRC_DIR}_0003: {len(test_src_trg)}')
#log_info.append(f'Length of {SOURCE} TEST {SRC_DIR}_0003: {len(test_src)}')
#log_info.append(f'Length of {TARGET} TEST {SRC_DIR}_0003: {len(test_trg)}')
with open(f'{temp_path}/test.{SRC_DIR}', 'w') as src_file:
    with open(f'{temp_path}/test.{TRG_DIR}', 'w') as trg_file:
        for entry in test_src_trg:
            src_file.write(entry[0]+'\n')
            trg_file.write(entry[1]+'\n')

#    for line in test_src:
#        txt_file.write(line+'\n')
#with open(f'{temp_path}/test.{TRG_DIR}', 'w') as txt_file:
#    for line in test_trg:
#        txt_file.write(line+'\n')

""" Read once annotated data from DialectBLI for dev, but remove elements overlapping with (above) test data """
dev_src_trg = []
#dev_src = []
#dev_trg = []
with open(f'{in_path}/2023ArteDial-{SRC_DIR}L-BiTe-{TRG_DIR}L-0002.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',',quotechar='"')
    next(csv_reader, None)
    for row in csv_reader:
        dev_src_trg.append([row[0],row[1]])
        #dev_src.append(row[0])
        #dev_trg.append(row[1])
log_info.append(f'Length of {SOURCE} DEV {SRC_DIR}_0002: {len(dev_src_trg)}')
#log_info.append(f'Length of {SOURCE} DEV {SRC_DIR}_0002: {len(dev_src)}')
#log_info.append(f'Length of {TARGET} DEV {SRC_DIR}_0002: {len(dev_trg)}')

# Remove duplicates to prevent information/knowledge leakage
dev_src_trg_out = []
for entry in dev_src_trg:
    if entry in test_src_trg:
        #print(f'Pair in dev that is also in test and will be dropped: \n\t{entry}')
        pass
    else:
        dev_src_trg_out.append(entry)
log_info.append(f'Length of unique {SOURCE} DEV {SRC_DIR}_0002: {len(dev_src_trg_out)}')
# for dev_sent in dev_src:
#     if dev_sent in test_src:
#         dev_src.remove(dev_sent)
# for dev_sent in dev_trg:
#     if dev_sent in test_trg:
#         dev_trg.remove(dev_sent)
#log_info.append(f'Length of unique {SOURCE} text {SRC_DIR}_0002: {len(dev_src)}')
#log_info.append(f'Length of unique {TARGET} text {SRC_DIR}_0002: {len(dev_trg)}')
with open(f'{temp_path}/dev.{SRC_DIR}', 'w') as src_file:
    with open(f'{temp_path}/dev.{TRG_DIR}', 'w') as trg_file:
        for entry in dev_src_trg_out:
            src_file.write(entry[0]+'\n')
            trg_file.write(entry[1]+'\n')
# with open(f'{temp_path}/dev.{SRC_DIR}', 'w') as txt_file:
#     for line in dev_src:
#         txt_file.write(line+'\n')
# with open(f'{temp_path}/dev.{TRG_DIR}', 'w') as txt_file:
#     for line in dev_trg:
#         txt_file.write(line+'\n')

""" Read machine annotated data from DialectBLI for training, but remove elements overlapping with (above) test and dev data """
train_src_trg = []
other_src_trg = []
#train_src = []
#train_trg = []

""" Compare length of sentences to reasonably exclude inproportionately sized 'alignment-pairs' """
def check_sent_length_reasonable(sent_01, sent_02):
    if len(sent_01) > 3 * len(sent_02) or len(sent_02) > 3 * len(sent_01):
        return False
    else:
        return True
def clean_on_string_level(sent_01, sent_02):
    clean_sent_01 = sent_01.replace('&lt;onlyinclude&gt;* ','').replace('&lt;onlyinclude&gt;*','').replace('&lt;br&gt;','').replace('&lt;','')
    clean_sent_02 = sent_02.replace('&lt;onlyinclude&gt;* ','').replace('&lt;onlyinclude&gt;*','').replace('&lt;br&gt;','').replace('&lt;','')

    return clean_sent_01, clean_sent_02


counter_of_same_sentence_on_both_sides = 0
with open(f'{in_path}/2023ArteDial-{SRC_DIR}L-BiTe-{TRG_DIR}L-0001.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',',quotechar='"')
    next(csv_reader, None)
    for row in csv_reader:
        # ###############################################################################
        # Some more dataset cleaning. TODO: Combine with earlier steps from MA-Thesis scripts
        if not (row[2] == ' ||meta.wikimedia.org/wiki/Special:BannerLoader?*.' or row[3] == ' ||meta.wikimedia.org/wiki/Special:BannerLoader?*.')and \
        not (row[2] == '&lt;poem style="font-style:italic"&gt;.' or row[3] == '&lt;poem style="font-style:italic"&gt;.') and \
        not (row[2] == ' InternetAnfrage := "http://de.wikipedia.org/w/index.php?title=".' or row[3] == ' InternetAnfrage := "http://de.wikipedia.org/w/index.php?title=".') and \
        not ('parentid&gt;' in row[2] or 'parentid&gt;' in row[3]) and \
        not ('username&gt;' in row[2] or 'username&gt;' in row[3]) and \
        not ('format&gt;' in row[2] or 'format&gt;' in row[3]) and \
        not ('ns&gt;' in row[2] or 'ns&gt;' in row[3]) and \
        not ('model&gt;' in row[2] or 'model&gt;' in row[3]) and \
        not ('timestamp&gt;' in row[2] or 'timestamp&gt;' in row[3]) and \
        not ('&lt;/poem&gt;' in row[2] or '&lt;/poem&gt;' in row[3]) and \
        not ('&lt;ref' in row[2] or '&lt;ref' in row[3]) and \
        not [row[2],row[3]] in train_src_trg:
            # Only consider entries where the source and the target sentence are not already (in) the same (language).
            if not row[2] == row[3]:
                # For when both sentences have a certain length to begin with
                if len(row[2]) > 5 and len(row[3]) > 5:
                    # Keep entries where the one side is not unproportionally longer than the other side
                    if check_sent_length_reasonable(row[2], row[3]):
                        sent_01, sent_02 = clean_on_string_level(row[2], row[3])
                        train_src_trg.append([sent_01, sent_02])
                    else:
                        other_src_trg.append([row[2],row[3]])
                # For shorter sentences
                else:
                    sent_01, sent_02 = clean_on_string_level(row[2], row[3])
                    train_src_trg.append([sent_01, sent_02])
            else:
                counter_of_same_sentence_on_both_sides = counter_of_same_sentence_on_both_sides + 1
    
        #train_src.append(row[2]) # 0 is {SOURCE} title
        #train_trg.append(row[3]) # 1 is {TARGET} title
log_info.append(f'Length of {SOURCE} TRAIN {SRC_DIR}_0001: {len(train_src_trg)}')
log_info.append(f'Number of sentences that were the same for source and target side: {counter_of_same_sentence_on_both_sides}')
#log_info.append(f'Length of {SOURCE} text {SRC_DIR}_0001: {len(train_src)}')
#log_info.append(f'Length of {TARGET} text {SRC_DIR}_0001: {len(train_trg)}')
# Remove duplicates to prevent information/knowledge leakage
train_src_trg_out = []
#train_src_out = []
#train_trg_out = []
for train_entry in train_src_trg:
    if train_entry in test_src_trg:
        #print(f'Pair in train that is also in test and will be dropped: \n\t{train_entry}')
        pass
    elif train_entry in dev_src_trg_out:
        #print(f'Pair in train that is also in dev and will be dropped: \n\t{train_entry}')
        pass
    else:
        train_src_trg_out.append(train_entry)
        #print(train_entry)
# for index, train_sent in enumerate(train_src):
#     if not train_sent in test_src and not train_sent in dev_src:
#         train_src_out.append(train_sent)
#         train_trg_out.append(train_trg[index])

# for index, train_sent in enumerate(train_src):
#     if not train_sent in dev_src:
#         train_src_out.append(train_sent)
#         train_trg_out.append(train_trg[index])

# for train_sent in train_trg:
#     if train_sent in test_trg:
#         train_trg.remove(train_sent)
# for train_sent in train_trg:
#     if train_sent in dev_trg:
#         train_trg.remove(train_sent)
log_info.append(f'Length of unique {SOURCE} text {SRC_DIR}_0001: {len(train_src_trg_out)}')
# print(f'#### Example Entries of Train-Set: ####')
# print(f'{train_src_trg_out[0]}')
# print(f'{train_src_trg_out[1]}')
# print(f'{train_src_trg_out[2]}')
# print(f'{train_src_trg_out[3]}')

#log_info.append(f'Length of unique {SOURCE} text {SRC_DIR}_0001: {len(train_src_out)}')
#log_info.append(f'Length of unique {TARGET} text {SRC_DIR}_0001: {len(train_trg_out)}')
with open(f'{temp_path}/train.{SRC_DIR}', 'w') as src_file:
    with open(f'{temp_path}/train.{TRG_DIR}', 'w') as trg_file:
        for entry in train_src_trg_out:
            src_file.write(entry[0]+'\n')
            trg_file.write(entry[1]+'\n')

# Store the excluded entries (viewing the data indicated that these contain a lot of "real" {SOURCE} data- even if not properly aligned)
with open(f'{temp_path}/other.{SRC_DIR}', 'w') as src_file:
    with open(f'{temp_path}/other.{TRG_DIR}', 'w') as trg_file:
        for entry in other_src_trg:
            src_file.write(entry[0]+'\n')
            trg_file.write(entry[1]+'\n')

# with open(f'{temp_path}/train.{SRC_DIR}', 'w') as txt_file:
#     for line in train_src_out:
#         txt_file.write(line+'\n')
# with open(f'{temp_path}/train.{TRG_DIR}', 'w') as txt_file:
#     for line in train_trg_out:
#         txt_file.write(line+'\n')
for info in log_info:
    print(info)



""" Tokenize German texts via stanza """
def tokenize_german_texts(input_path = f'/media/AllBlue/LanguageData/PREP/2024SchuMATh-{SRC_DIR}L-Sock-{TRG_DIR}L-DBLI-0001/Temp', out_path = f'/media/AllBlue/LanguageData/PREP/2024SchuMATh-{SRC_DIR}L-Sock-{TRG_DIR}L-DBLI-0001'):
    # Download stanzas models
    #stanza.download(lang='de', model_dir='/media/AllBlue/LanguageData/MODELS/stanza/', verbose=True)#, processors='tokenize')

    nlp = stanza.Pipeline('de', processors='tokenize', tokenize_no_ssplit=True) # tokenize_pretokenized=True,

    dir_maker(out_path)
    list_of_source_files = glob.glob(f'{input_path}/*')

    for text_file in list_of_source_files:
        tokenized_text = []
        output_file = text_file
        output_file = output_file.replace('/Temp','')

        text_content = []
        # Read the text content from file
        print(f'Input file: {text_file}')
        with open(text_file, 'r') as in_file:
            #text_content = in_file.read()
            text_content = in_file.readlines()
            for line in text_content:
                line = line+'\n'

        # All sentences of text file in a single stanza-document
        doc = nlp(text_content)

        for sentence in doc.sentences:
            tokenized_sentence = ""
            for current_token in sentence.tokens:
                tokenized_sentence = tokenized_sentence+current_token.text+' '
            
            tokenized_text.append(tokenized_sentence)

        print(f'Output file: {output_file}')
        with open(output_file, 'w') as out_file:
            for sent in tokenized_text:
                out_file.write(sent+'\n')

tokenize_german_texts(temp_path, out_path)

# Remove the first n=32 entries that were identified to be the same despite some minor punctuation differences.
src_text = []
with open(f'{out_path}/train.{SRC_DIR}', 'r') as src_in:
    src_text = src_in.readlines()
with open(f'{out_path}/train.{SRC_DIR}', 'w') as src_out:
    for sentence in src_text[33:]:
        src_out.write(sentence)

trg_text = []
with open(f'{out_path}/train.{TRG_DIR}', 'r') as trg_in:
    trg_text = trg_in.readlines()
with open(f'{out_path}/train.{TRG_DIR}', 'w') as trg_out:
    for sentence in trg_text[33:]:
        trg_out.write(sentence)



