#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Aggregate manually collected wordlists by (sub-)dialects for text classification of untagged wikidump-data

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/clean/wordlists2aggregate.py"

data_quality="informed" # "naive" | "clean" | "informed"  (naive automatically happens during extraction)

# Bavarian - English
input_path="/media/AllBlue/LanguageData/DOWNLOAD/handmade/wordlists"
output_path="/media/AllBlue/LanguageData/CLEAN/handmade/wordlists"
lang_name="German"
input_file="${input_path}/${lang_name}.json"
output_file="${output_path}/${lang_name}.json"

mkdir -p "${output_path}"
script_path="${current_dir}/${script_file}"

python3 "${script_path}" -i "${input_file}" -o "${output_file}"

