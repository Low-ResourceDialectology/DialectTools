#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Classify articles (from wikidumps) based on word-frequencies (from aggregated wordlists)

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/clean/wikidumps2sort.py"
input_dir="/media/AllBlue/LanguageData/CLEAN/wikidumps/splits/bar"
wordlists_file="/media/AllBlue/LanguageData/CLEAN/handmade/wordlists/German.json"
output_dir="/media/AllBlue/LanguageData/CLEAN/wikidumps/informed/bar"
mkdir "${output_dir}"

script_path="${current_dir}/${script_file}"
    python3 "${script_path}" \
    -i "${input_dir}" \
    -w "${wordlists_file}" \
    -o "${output_dir}" 
