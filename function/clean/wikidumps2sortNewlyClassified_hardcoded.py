# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Based on previously (newly) classify sentences from wikidump data based the dialect-tag-candidates,
# extract and filter the sentences for further processing
# NOTE: Our own classification can drastically reduce the sentences of previously already under-represented dialect(-groups)!
#       Add the inclusion of the originally tagged sentences "as is" and only add new sentences to dialect-groups 
#       NOTE: This is assuming our automatic approach is less accurate than the estimation of the original authors of the text articles on wikipedia
#             Later inclusion of human annotation (by native speakers) can potentially flip this around

import argparse
import os
import glob
import json
import pathlib

"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

# def extract_sentences_from_json(json_dir, output_dir):
#     json_files = glob.glob(f'{json_dir}/*.json')

#     for json_file in json_files:
#         with open(json_file, 'r', encoding='utf-8') as f:
#             data = json.load(f)
        
#         file_name = os.path.basename(json_file).replace('.json', '.txt').replace('new-','').replace('correct-','').replace('-file','')
#         output_file_path = os.path.join(output_dir, file_name)
        
#         with open(output_file_path, 'w', encoding='utf-8') as f:
#             for sentence in data.keys():
#                 f.write(f"{sentence}\n")

def combine_sentences_from_json_and_txt(txt_dir, json_dir, aggregated_tag, output_dir, quality):
    # NOTE: quality as quick-fix for stupid filenaming from Past-Christian. quality = "gold" | "silver"
    # Read the originally tagged sentences from txt file
    with open(f'{txt_dir}/{aggregated_tag}.txt') as infile:
        original_lines = [line.rstrip() for line in infile] # removing the new line characters

    if quality == "silver":

        # NOTE: For the untagged "Bavarian" we don't need to keep the old ones, since they were never really tagged as "Bavarian"
        if aggregated_tag == "Bavarian":
            original_lines = []

        # Read the newly tagged sentences from json file
        with open(f'{json_dir}/new-{aggregated_tag.replace(" ","_")}-file.json', 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            for sentence in data.keys():
                if not sentence in original_lines:
                    original_lines.append(f"{sentence}")
    elif quality == "gold":
        pass

    # Write sentences to output txt file
    file_name = f'{aggregated_tag.replace(" ","_")}.txt'
    output_file_path = os.path.join(output_dir, file_name)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        for sentence in original_lines:
            f.write(f"{sentence}\n")




if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Extract sentences from JSON files and write to TXT files.")
    # parser.add_argument("-i", "--input_dir", type=str, help="Directory containing JSON files with sentences.")
    # parser.add_argument("-o", "--output_dir", type=str, help="Directory to save the output TXT files.")

    # args = parser.parse_args()
    # dir_maker(args.output_dir)
    
    # input_gold_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagcorrect/bar'
    # output_gold_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/gold'
    # dir_maker(output_gold_dir)
    # extract_sentences_from_json(input_gold_dir, output_gold_dir)

    # input_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagnew/bar'
    # output_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/silver'
    # dir_maker(output_silver_dir)
    # extract_sentences_from_json(input_silver_dir, output_silver_dir)

    input_reference_text_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-aggr/bar'

    aggregated_tags = ["Bavarian", "Northern Bavarian", "Eastern Central Bavarian", "Western Central Bavarian", "Southern Bavarian"]

    # For Gold-Data
    input_gold_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagcorrect/bar'
    output_gold_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/gold'
    # For Silver-Data
    input_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-text-freq-aggr-clean-tagnew/bar'
    output_silver_dir = '/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar/silver'
    
    # For aggregated dialect-tag 
    for aggregated_tag in aggregated_tags:
        # For Gold-Data
        dir_maker(output_gold_dir)
        combine_sentences_from_json_and_txt(input_reference_text_dir, input_gold_dir, aggregated_tag, output_gold_dir, "gold")
        
        # For Silver-Data    
        dir_maker(output_silver_dir)
        combine_sentences_from_json_and_txt(input_reference_text_dir, input_silver_dir, aggregated_tag, output_silver_dir, "silver")
        

    


    #print(f"Processed JSON files from {input_dir} and saved text files to {output_gold_dir} and to {output_silver_dir}")




