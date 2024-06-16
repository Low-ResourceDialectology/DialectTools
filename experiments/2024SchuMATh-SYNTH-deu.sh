#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Extract replacement rules from linguistic features (lexicograpic | morphological | syntactical)

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/FEATURES"
output_path="/media/AllBlue/LanguageData/PERTURBS"
mode="lex" # lex | mor | syn
mode2="LeftToRight" # | "RightToLeft"
current_dir="$(dirname "$0")"
script_file="../launch/Perturbation_Extraction.sh"
script_path="${current_dir}/${script_file}"

# +++++++++++++++++++++++++++++++++++++++++++++++
# Alemannic - GERMAN 
# src_lang="als"
# src_name="Alemannic"
# trg_lang="deu"
# trg_name="German"
# echo "Processing: ${src_name} and ${trg_name}"

# mode="lex"
# mode2="LeftToRight"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${mode}" \
#     -n "${mode2}"

# mode2="RightToLeft"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${mode}" \
#     -n "${mode2}"

# mode="mor"
# mode2="LeftToRight"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${mode}" \
#     -n "${mode2}"

# mode2="RightToLeft"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${mode}" \
#     -n "${mode2}"

# TODO
#mode="syn"


# +++++++++++++++++++++++++++++++++++++++++++++++
# Bavarian - GERMAN 
src_lang="bar"
src_name="Bavarian"
trg_lang="deu"
trg_name="German"
echo "Processing: ${src_name} and ${trg_name}"

mode="lex"
mode2="LeftToRight"
bash "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}" \
    -n "${mode2}"
mode="mor"
mode2="LeftToRight"
bash "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}" \
    -n "${mode2}"

# +++++++++++++++++++++++++++++++++++++++++++++++
# German - Bavarian 
src_lang="deu"
src_name="German"
trg_lang="bar"
trg_name="Bavarian"
echo "Processing: ${src_name} and ${trg_name}"

mode="lex"
mode2="RightToLeft"
bash "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}" \
    -n "${mode2}"
mode="mor"
mode2="RightToLeft"
bash "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}" \
    -n "${mode2}"

# TODO
#mode="syn"