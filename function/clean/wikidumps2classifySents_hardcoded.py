# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# 1. Assign dialect-tag-candidates based on dialect-specific word-frequencies
# 2. Verify the validity of this step by investigating those sentences for which the correct/original dialect-tag is known
# 3. Classify untagged sentences from wikidump data based the same dialect-tag-candidates.

import argparse
import glob
import json
import pathlib
import os
from collections import defaultdict

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
        dialect_name = os.path.basename(wordlist_file).replace('-freq.json', '').replace('_', ' ')
        with open(wordlist_file, 'r', encoding='utf-8') as f:
            wordlist = json.load(f)
        wordlists[dialect_name] = wordlist

    return wordlists

# NOTE: Only processing the large file with the "unknown"/untagged sentences
def read_sentences_from_txt_file(input_file):
    sentences = {}

    with open(input_file, 'r', encoding='utf-8') as f:
        file_sentences = f.readlines()
    
    file_name = os.path.basename(input_file)
    sentences[file_name] = [sentence.strip() for sentence in file_sentences]

    return sentences

# NOTE: Processing all files in input_dir
def read_sentences_from_txt_dir(input_dir):
    sentences = {}

    input_files = glob.glob(f'{input_dir}/*.txt')
    for input_file in input_files:
        with open(input_file, 'r', encoding='utf-8') as f:
            file_sentences = f.readlines()
        
        file_name = os.path.basename(input_file)
        sentences[file_name] = [sentence.strip() for sentence in file_sentences]

    return sentences

def inspect_and_tag_sentences(sentences, wordlists):
    tagged_sentences = {}

    for file_name, file_sentences in sentences.items():
        tagged_sentences[file_name] = []
        
        for sentence in file_sentences:
            sentence_tags = defaultdict(int)
            for dialect_name, wordlist in wordlists.items():
                for word in sentence.split():
                    if word in wordlist:
                        sentence_tags[dialect_name] += 1
            
            tagged_sentences[file_name].append({
                "text": sentence,
                "tags": dict(sentence_tags)
            })

    return tagged_sentences

def write_json(output_file_path, data):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def validate_classification(tagged_sentences, correct_dialect_files, new_dialect_files, output_wrong_dir):
    correct_sentences = defaultdict(list)
    incorrect_sentences = defaultdict(list)
    new_sentences = defaultdict(list)
    
    for dialect, files in correct_dialect_files.items():
        for file_name in files:
            for sentence_data in tagged_sentences.get(file_name, []):
                sentence = sentence_data["text"]
                tags = sentence_data["tags"]
                # Check for non-empty sequence
                if tags:
                    if tags.get(dialect, 0) >= max(tags.values()):
                        correct_sentences[dialect].append(sentence_data)
                    else:
                        incorrect_sentences[dialect].append(sentence_data)
                else:
                    incorrect_sentences[dialect].append(sentence_data)
    num_unprocessed_sentences = 0
    for dialect, files in new_dialect_files.items():
        for file_name in files:
            for sentence_data in tagged_sentences.get(file_name, []):
                sentence = sentence_data["text"]
                tags = sentence_data["tags"]
                # Check for non-empty sequence
                if tags:
                    for tag in tags:
                        if tags[tag] >= max(tags.values()):
                            highest_tag = tag
                    new_sentences[highest_tag].append(sentence_data)
                else:
                    num_unprocessed_sentences = num_unprocessed_sentences + 1

    output_wrong_file = f'{output_wrong_dir}/incorrect-tagged.json'
    write_json(output_wrong_file, dict(incorrect_sentences))
    print(f'Number of not newly-tagged sentences: {num_unprocessed_sentences}')
    return correct_sentences, new_sentences

def classify_untagged_text(not_wrongly_classified_sentences, newly_classified_sentences, output_correct_dir, output_unclear_dir, output_new_dir):
    unclear_sentences = defaultdict(list)
    correct_sentences = defaultdict(list)
    new_sentences = defaultdict(list)
    
    for dialect, sentences in not_wrongly_classified_sentences.items():
        #dialect_file_path = os.path.join(output_new_dir, f"{dialect.replace(' ', '_')}-file.json")
        for sentence_data in sentences:
            sentence = sentence_data["text"]
            tags = sentence_data["tags"]
            max_tag = max(tags, key=tags.get)
            max_count = tags[max_tag]
            second_max_count = sorted(tags.values(), reverse=True)[1] if len(tags) > 1 else 0

            if max_count > second_max_count:
                correct_sentences[dialect].append(sentence_data)
                #write_json(dialect_file_path, {sentence: tags})
            else:
                #unclear_file_path = os.path.join(output_info_dir, f"unclear-{dialect.replace(' ', '_')}-{max_tag.replace(' ', '_')}-file.json") # Not used here...
                unclear_sentences[(dialect, max_tag)].append(sentence_data)

    for dialect, sentences in newly_classified_sentences.items():
        for sentence_data in sentences:
            sentence = sentence_data["text"]
            tags = sentence_data["tags"]
            max_tag = max(tags, key=tags.get)
            max_count = tags[max_tag]
            second_max_count = sorted(tags.values(), reverse=True)[1] if len(tags) > 1 else 0

            if max_count > second_max_count:
                new_sentences[dialect].append(sentence_data)
                #write_json(dialect_file_path, {sentence: tags})
            else:
                #unclear_file_path = os.path.join(output_info_dir, f"unclear-{dialect.replace(' ', '_')}-{max_tag.replace(' ', '_')}-file.json") # Not used here...
                unclear_sentences[(dialect, max_tag)].append(sentence_data)

    for key, sentences in correct_sentences.items():
        correct_file_path = os.path.join(output_correct_dir, f"correct-{key.replace(' ', '_')}-file.json")
        write_json(correct_file_path, {sentence_data["text"]: sentence_data["tags"] for sentence_data in sentences})

    for key, sentences in unclear_sentences.items():
        unclear_file_path = os.path.join(output_unclear_dir, f"unclear-{key[0].replace(' ', '_')}-{key[1].replace(' ', '_')}-file.json")
        write_json(unclear_file_path, {sentence_data["text"]: sentence_data["tags"] for sentence_data in sentences})

    for key, sentences in new_sentences.items():
        new_file_path = os.path.join(output_new_dir, f"new-{key.replace(' ', '_')}-file.json")
        write_json(new_file_path, {sentence_data["text"]: sentence_data["tags"] for sentence_data in sentences})


if __name__ == "__main__":
    # NOTE: Hardcoded approach for Bavarian wikidump data
    input_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar'
    wordlists_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean/bar'
    correct_dialect_files = ''
    output_unclear_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagunclear/bar'
    output_wrong_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagwrong/bar'
    output_correct_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagcorrect/bar'
    output_new_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagnew/bar'
    dir_maker(output_unclear_dir)
    dir_maker(output_wrong_dir)
    dir_maker(output_correct_dir)
    dir_maker(output_new_dir)

    wordlists = read_wordlists_from_json(wordlists_dir)

    sentences = read_sentences_from_txt_dir(input_dir)


    tagged_sentences = inspect_and_tag_sentences(sentences, wordlists)

    # with open(correct_dialect_files, 'r', encoding='utf-8') as f:
    #     correct_dialect_files = json.load(f)
    correct_dialect_files = {
        "Northern Bavarian": [
            "Nordbairisch.txt",
            "Nordmittlboarisch.txt",
            "Nordmittelbairisch.txt"
            ],
        "Eastern Central Bavarian": [
            "Ostmittlboarisch.txt",
            "Ostmittelbairisch.txt",
            "Ostmiddlboarisch.txt"
            ],
        "Western Central Bavarian": [
            "Westmittelbairisch.txt",
            "Westmittlboarisch.txt"
            ],
        "Southern Bavarian": [
            "Südmittelbairisch.txt",
            "Südmittelbayerisch.txt",
            "Südbairisch.txt",
            "ostsüdboarisch.txt",
            "Südostbayerisch.txt",
            "Siadostboarisch.txt"
            ]
    }
    new_dialect_files = {
        "Unbeknownst": [
            "andere.txt",
            "UNKNOWN.txt"
            ]
    }
        

    not_wrongly_classified_sentences, newly_classified_sentences = validate_classification(tagged_sentences, correct_dialect_files, new_dialect_files, output_wrong_dir)

    classify_untagged_text(not_wrongly_classified_sentences, newly_classified_sentences, output_correct_dir, output_unclear_dir, output_new_dir)

    print(f"Processed text files from {input_dir} and saved classified sentences to {output_new_dir}")



# #     parser = argparse.ArgumentParser(description="Validate and classify sentences based on (sub-)dialect-tags.")
# #     parser.add_argument("-i", "--input_dir", type=str, help="Directory containing text files with sentences.")
# #     parser.add_argument("-w", "--wordlists_file", type=str, help="Directory with aggregated wordlists.")
# #     parser.add_argument("-o", "--output_dir", type=str, help="Directory to save the output files.")
# #     parser.add_argument("-c", "--correct_dialect_files", type=str, help="File containing the correct dialect files paths.")
# #     parser.add_argument("-info", "--output_info_file", type=str, help="File to save the incorrect sentences info.")

# #     args = parser.parse_args()
# #     dir_maker(args.output_dir)

# #     wordlists = read_wordlists_from_json(args.wordlists_file)
# #     sentences = read_sentences_from_txt(args.input_dir)
    
# #     tagged_sentences = inspect_and_tag_sentences(sentences, wordlists)

# #     with open(args.correct_dialect_files, 'r', encoding='utf-8') as f:
# #         correct_dialect_files = json.load(f)
    
# #     correct_sentences = validate_classification(tagged_sentences, correct_dialect_files, args.output_info_file)

# #     classify_untagged_text(correct_sentences, args.output_dir)

# #     print(f"Processed text files from {args.input_dir} and saved classified sentences to {args.output_dir}")

#     input_dir='/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar'
#     output_dir='/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagnew/bar'
#     dir_maker(output_dir)

#     wordlists_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean/bar'
#     wordlists = read_wordlists_from_json(wordlists_dir)
    
#     # # NOTE: Entire directory
#     # sentences = read_sentences_from_txt_dir(input_dir)
    
#     # NOTE: Just a single file
#     input_file = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar/UNKNOWN.txt'
#     sentences = read_sentences_from_txt_file(input_file)
    
#     tagged_sentences = inspect_and_tag_sentences(sentences, wordlists)

#     # # TODO: Clean code for the validation part
#     # # Current function expects a json file with paths to the (correct/known) dialect-files in it
#     # # NOTE: Change to work directly on the dictionary we create in the lines below(?)
#     # input_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar"
#     # aggregated_tags = ["Northern Bavarian", "Eastern Central Bavarian", "Western Central Bavarian", "Southern Bavarian"]

#     # # For aggregated dialect-tag 
#     # for aggregated_tag in aggregated_tags:

#     #     noisy_tags = []
#     #     noisy_tags_files = []
#     #     if aggregated_tag == "Northern Bavarian":
#     #         noisy_tags = ["Nordbairisch","Nordmittlboarisch","Nordmittelbairisch"]
            
#     #     elif aggregated_tag == "Eastern Central Bavarian":
#     #         noisy_tags = ["Ostmittlboarisch","Ostmittelbairisch","Ostmiddlboarisch"]
            
#     #     elif aggregated_tag == "Western Central Bavarian":
#     #         noisy_tags = ["Westmittelbairisch","Westmittlboarisch"]
            
#     #     elif aggregated_tag == "Southern Bavarian":
#     #         noisy_tags = ["Südmittelbairisch","Südmittelbayerisch","Südbairisch","ostsüdboarisch","Südostbayerisch","Siadostboarisch"]
            
#     #     # Build file paths based on noisy tags
#     #     for noisy_tag in noisy_tags:
#     #         file_path = f'{input_dir_bar}/{noisy_tag}.txt'
#     #         noisy_tags_files.append(file_path)

#     #     correct_dialect_files = noisy_tags_files

#     #     with open(correct_dialect_files, 'r', encoding='utf-8') as f:
#     #         correct_dialect_files = json.load(f)
    
#     #     correct_sentences = validate_classification(tagged_sentences, correct_dialect_files, args.output_info_file)

#     #     classify_untagged_text(correct_sentences, args.output_dir)

#     #     print(f"Processed text files from {args.input_dir} and saved classified sentences to {args.output_dir}")

    

#     input_dir_bar = "/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text/bar"
#     aggregated_tags = ["Northern Bavarian", "Eastern Central Bavarian", "Western Central Bavarian", "Southern Bavarian"]

#     # For aggregated dialect-tag 
#     for aggregated_tag in aggregated_tags:

#         noisy_tags = []
#         noisy_tags_files = []
#         if aggregated_tag == "Northern Bavarian":
#             noisy_tags = ["Nordbairisch","Nordmittlboarisch","Nordmittelbairisch"]
            
#         elif aggregated_tag == "Eastern Central Bavarian":
#             noisy_tags = ["Ostmittlboarisch","Ostmittelbairisch","Ostmiddlboarisch"]
            
#         elif aggregated_tag == "Western Central Bavarian":
#             noisy_tags = ["Westmittelbairisch","Westmittlboarisch"]
            
#         elif aggregated_tag == "Southern Bavarian":
#             noisy_tags = ["Südmittelbairisch","Südmittelbayerisch","Südbairisch","ostsüdboarisch","Südostbayerisch","Siadostboarisch"]
            
#         # Build file paths based on noisy tags
#         for noisy_tag in noisy_tags:
#             file_path = f'{input_dir_bar}/{noisy_tag}.txt'
#             noisy_tags_files.append(file_path)

#         correct_dialect_files = noisy_tags_files

#         with open(correct_dialect_files, 'r', encoding='utf-8') as f:
#             correct_dialect_files = json.load(f)
    
#         correct_sentences = validate_classification(tagged_sentences, correct_dialect_files, args.output_info_file)

#         classify_untagged_text(correct_sentences, args.output_dir)

#         print(f"Processed text files from {args.input_dir} and saved classified sentences to {args.output_dir}")
