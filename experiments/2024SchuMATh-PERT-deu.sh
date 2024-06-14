#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Apply replacement rules (lexicograpic | morphological | syntactical) on text to perturb it 

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/PERTURBS"
output_path="/media/AllBlue/LanguageData/PREP"
src_lang="als"
src_name="Alemannic"
trg_lang="deu"
trg_name="German"
mode="lex" # lex | mor | syn
mode2="naive" # naive | clean | informed
current_dir="$(dirname "$0")"
script_file="../launch/Perturbation_Application.sh"
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
    -m "${mode}" \
    -n "${mode2}"

mode="mor"
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

