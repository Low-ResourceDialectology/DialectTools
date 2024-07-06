# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Classify articles (from wikidumps) based on word-frequencies (from aggregated wordlists)
#   Input: Json files per pre-tagged language variety in wikidumps-data, json-file of aggregated wordlists
#   Output: (Sub-)Dialect-Tagged articles from wikidumps (as txt-files) 

import argparse
import glob
import json
import pathlib
import os

"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def read_wordlists_from_json(wordlists_dir):
    wordlists = {}
    wordlist_files = glob.glob(f'{wordlists_dir}/*-freq.json')

    for wordlist_file in wordlist_files:
        dialect_name = os.path.basename(wordlist_file).replace('-freq.json', '')
        with open(wordlist_file, 'r', encoding='utf-8') as f:
            wordlist = json.load(f)
        wordlists[dialect_name] = wordlist

    return wordlists

def read_sentences_from_txt(input_dir):
    sentences = {}

    input_files = glob.glob(f'{input_dir}/*.txt')
    for input_file in input_files:
        with open(input_file, 'r', encoding='utf-8') as f:
            file_sentences = f.readlines()
        
        file_name = os.path.basename(input_file)
        sentences[file_name] = [sentence.strip() for sentence in file_sentences]

    return sentences

# def inspect_and_tag_sentences(sentences, wordlists):
#     tagged_sentences = {}

#     for file_name, file_sentences in sentences.items():
#         tagged_sentences[file_name] = []
        
#         for sentence in file_sentences:
#             sentence_tags = []
#             for dialect_name, wordlist in wordlists.items():
#                 for word in sentence.split():
#                     if word in wordlist:
#                         sentence_tags.append(dialect_name)
            
#             tagged_sentences[file_name].append({
#                 "text": sentence,
#                 "tags": sentence_tags
#             })

#     return tagged_sentences

def inspect_and_tag_sentences(sentences, wordlists):
    tagged_sentences = {}

    for file_name, file_sentences in sentences.items():
        tagged_sentences[file_name] = []
        
        for sentence in file_sentences:
            sentence_tags = {}
            for dialect_name, wordlist in wordlists.items():
                for word in sentence.split():
                    if word in wordlist:
                        if dialect_name in sentence_tags:
                            sentence_tags[dialect_name] += 1
                        else:
                            sentence_tags[dialect_name] = 1
            
            tagged_sentences[file_name].append({
                "text": sentence,
                "tags": sentence_tags
            })

    return tagged_sentences

# def write_tagged_sentences(output_dir, tagged_sentences):
#     for file_name, sentences in tagged_sentences.items():
#         output_file_path = os.path.join(output_dir, file_name)
        
#         with open(output_file_path, 'w', encoding='utf-8') as f:
#             for sentence_data in sentences:
#                 sentence = sentence_data["text"]
#                 tags = ', '.join(sentence_data["tags"])
#                 f.write(f"{sentence} [Tags: {tags}]\n")

def write_tagged_sentences(output_dir, tagged_sentences):
    for file_name, sentences in tagged_sentences.items():
        output_file_path = os.path.join(output_dir, file_name.replace('.txt', '.json'))
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump({sentence_data["text"]: sentence_data["tags"] for sentence_data in sentences}, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_dir='/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar'
    output_dir='/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagcand/bar'
    dir_maker(output_dir)

    wordlists_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean/bar'
    wordlists = read_wordlists_from_json(wordlists_dir)
    sentences = read_sentences_from_txt(input_dir)
    
    tagged_sentences = inspect_and_tag_sentences(sentences, wordlists)

    write_tagged_sentences(output_dir, tagged_sentences)

    print(f"Processed text files from {input_dir} and saved tagged sentences to {output_dir}")
