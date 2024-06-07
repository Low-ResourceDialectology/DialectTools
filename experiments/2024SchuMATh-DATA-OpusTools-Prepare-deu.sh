#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Take split sets for German varieties and combine them (filter for quality?) into final train & dev sets

source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

current_dir="$(dirname "$0")"
script_file="$current_dir/../extract/prepare_splits.py" 

# Bavarian - German
input_path="/media/AllBlue/LanguageData/CLEAN/opustools"
output_path="/media/AllBlue/LanguageData/PREP/opustools"
src_lang="bar"
trg_lang="de"
experiment="naive" # | "clean" | "informed"
substrings="train,dev,test"
python3 "${script_file}" \
    -i "${input_path}/${src_lang}-${trg_lang}/${experiment}" \
    -o "${output_path}/${src_lang}-${trg_lang}/${experiment}" \
    -s "${substrings}"


# Bavarian - English
input_path="/media/AllBlue/LanguageData/CLEAN/opustools"
output_path="/media/AllBlue/LanguageData/PREP/opustools"
src_lang="bar"
trg_lang="en"
experiment="naive" # | "clean" | "informed"
substrings="train,dev,test"
python3 "${script_file}" \
    -i "${input_path}/${src_lang}-${trg_lang}/${experiment}" \
    -o "${output_path}/${src_lang}-${trg_lang}/${experiment}" \
    -s "${substrings}"


# NOTE: From prior script → echo "Processing the small (Bavarian-related) files already pushes the memory usage to 30+ GB... The script will have to be modified for German-English!"
# # German - English
# input_path="/media/AllBlue/LanguageData/CLEAN/opustools"
# output_path="/media/AllBlue/LanguageData/PREP/opustools"
# src_lang="de"
# trg_lang="en"
# experiment="naive" # | "clean" | "informed"
# substrings="train,dev,test"
# python3 "${script_file}" \
#     -i "${input_path}/${src_lang}-${trg_lang}/${experiment}" \
#     -o "${output_path}/${src_lang}-${trg_lang}/${experiment}" \
#     -s "${substrings}"

