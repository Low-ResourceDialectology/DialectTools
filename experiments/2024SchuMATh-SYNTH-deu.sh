#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Extract replacement rules from linguistic features (lexicograpic | morphological | syntactical)

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/FEATURES"
output_path="/media/AllBlue/LanguageData/PERTURBS"
src_lang="als"
src_name="Alemannic"
trg_lang="deu"
trg_name="German"
mode="lex" # lex | mor | syn
current_dir="$(dirname "$0")"
script_file="../launch/Perturbation_Extraction.sh"
script_path="${current_dir}/${script_file}"

echo "Processing: ${src_name} and ${trg_name}"

mode="lex"
bash "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}"

mode="mor"
bash "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}"

# TODO
#mode="syn"
