#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Extract linguistic features (lexicograpic | morphological | syntactical) from bidictionaries

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/DICT"
output_path="/media/AllBlue/LanguageData/FEATURES"
perturbation_type="lex" # lex | mor | syn
extraction_method="direct" # direct | ?? something heuristic based ??
context_length="1" # 1 | 2 | 3 # NOTE: Currently only used in mor not in lex
current_dir="$(dirname "$0")"
script_file="../launch/Linguistic_Features.sh"
script_path="${current_dir}/${script_file}"

# +++++++++++++++++++++++++++++++++++++++++++++++
# Alemannic - GERMAN 
# src_lang="als"
# src_name="Alemannic"
# trg_lang="deu"
# trg_name="German"
# echo "Processing: ${src_name} and ${trg_name}"

# perturbation_type="lex"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -e "${extraction_method}" \
#     -c "${context_length}"

# perturbation_type="mor"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -e "${extraction_method}" \
#     -c "${context_length}"

# TODO
#perturbation_type="syn"


# +++++++++++++++++++++++++++++++++++++++++++++++
# BAVARIAN - GERMAN 
src_lang="bar"
src_name="Bavarian"
trg_lang="deu"
trg_name="German"
echo "Processing: ${src_name} and ${trg_name}"

perturbation_type="lex"
bash "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${perturbation_type}" \
    -e "${extraction_method}" \
    -c "${context_length}"

perturbation_type="mor"
bash "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${perturbation_type}" \
    -e "${extraction_method}" \
    -c "${context_length}"

# TODO
#perturbation_type="syn"

