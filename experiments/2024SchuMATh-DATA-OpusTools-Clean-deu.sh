#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Clean opustools data for German (Bavarian-German and Bavarian-English)

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/clean/opustools.sh"

data_quality="clean" # "naive" | "clean" | "informed"  (naive automatically happens during extraction)

# Bavarian - English
input_path="/media/AllBlue/LanguageData/CLEAN/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="bar"
trg_lang="en"
data_quality="clean" # | "clean" | "informed"
cosine_filtering="True" # "True" | "False"

# Function call for cleaning based on the "naive"-split data
bash "${script_file}" \
    -i "${input_path}/${src_lang}-${trg_lang}/naive-split" \
    -o "${output_path}/${src_lang}-${trg_lang}/${data_quality}-split" \
    -s "${src_lang}" \
    -t "${trg_lang}" \
    -d "${data_quality}" \
    -c "${cosine_filtering}"

# # Bavarian - German
# input_path="/media/AllBlue/LanguageData/CLEAN/opustools"
# output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
# src_lang="bar"
# trg_lang="de"
# data_quality="clean" # | "clean" | "informed"
# cosine_filtering="True" # "True" | "False"

# # Function call for cleaning based on the "naive"-split data
# bash "${script_file}" \
#     -i "${input_path}/${src_lang}-${trg_lang}/naive-split" \
#     -o "${output_path}/${src_lang}-${trg_lang}/${data_quality}-split" \
#     -s "${src_lang}" \
#     -t "${trg_lang}" \
#     -d "${data_quality}" \
#     -c "${cosine_filtering}"

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Function call for cleaning based on the "naive" data
# bash "${script_file}" \
#     -i "${input_path}/${src_lang}-${trg_lang}/naive" \
#     -o "${output_path}/${src_lang}-${trg_lang}/${data_quality}" \
#     -s "${src_lang}" \
#     -t "${trg_lang}" \
#     -d "${data_quality}" \
#     -c "${cosine_filtering}"
