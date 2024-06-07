#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Take extracted text data and split into train/dev/test sets for German varieties

source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

current_dir="$(dirname "$0")"
script_file="$current_dir/../extract/split_text.py" 

# Bavarian - German
input_path="/media/AllBlue/LanguageData/CLEAN/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="bar"
trg_lang="de"
mode="default" # "default" = train,dev,test | "cv" = more than 3 output files named according to split-proportions
experiment="naive" # | "clean" | "informed"
proportions="0.8,0.1,0.1"
python3 "${script_file}" \
    -i "${input_path}/${src_lang}-${trg_lang}" \
    -o "${output_path}/${src_lang}-${trg_lang}/${experiment}" \
    -e "${output_extension}" \
    -s "${src_lang}" \
    -t "${trg_lang}" \
    -m "${mode}" \
    -p "${proportions}"


# Bavarian - English
input_path="/media/AllBlue/LanguageData/CLEAN/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="bar"
trg_lang="en"
mode="default" # "default" = train,dev,test | "cv" = more than 3 output files named according to split-proportions
experiment="naive" # | "clean" | "informed"
proportions="0.8,0.1,0.1"
python3 "${script_file}" \
    -i "${input_path}/${src_lang}-${trg_lang}" \
    -o "${output_path}/${src_lang}-${trg_lang}/${experiment}" \
    -e "${output_extension}" \
    -s "${src_lang}" \
    -t "${trg_lang}" \
    -m "${mode}" \
    -p "${proportions}"


echo "Processing the small (Bavarian-related) files already pushes the memory usage to 30+ GB... The script will have to be modified for German-English!"
# # German - English
# input_path="/media/AllBlue/LanguageData/CLEAN/opustools"
# output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
# src_lang="de"
# trg_lang="en"
# mode="default" # "default" = train,dev,test | "cv" = more than 3 output files named according to split-proportions
# experiment="naive" # | "clean" | "informed"
# proportions="0.8,0.1,0.1"
# python3 "${script_file}" \
#     -i "${input_path}/${src_lang}-${trg_lang}" \
#     -o "${output_path}/${src_lang}-${trg_lang}/${experiment}" \
#     -e "${output_extension}" \
#     -s "${src_lang}" \
#     -t "${trg_lang}" \
#     -m "${mode}" \
#     -p "${proportions}"

