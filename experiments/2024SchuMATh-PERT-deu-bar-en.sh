#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Apply replacement rules (lexicograpic | morphological | syntactical) on text to perturb it 

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/PERTURBS"
data_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/English/German/NLLB" # TODO: Split up and make modular for data-sources and language pairs "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive"
output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/English/German/NLLB/Bavarian"
mode="lex" # lex | mor | syn
mode2="naive" # naive | clean | informed
current_dir="$(dirname "$0")"
script_file="../launch/Perturbation_Application.sh"
script_path="${current_dir}/${script_file}"

# +++++++++++++++++++++++++++++++++++++++++++++++
# German - Bavarian 
src_lang="deu"
src_name="German"
trg_lang="bar"
trg_name="Bavarian"
data_file_extension="en"
echo "Perturbing: ${src_name} into ${trg_name}"

# mode="lex"
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${data_path}" \
#     -o "${output_path}/lex" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${mode}" \
#     -n "${mode2}" \
#     -e "${data_file_extension}"

mode="mor"
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}" \
    -d "${data_path}" \
    -o "${output_path}/mor" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}" \
    -n "${mode2}" \
    -e "${data_file_extension}"

mode="all" # Again morphological, but on the results from the lexicographic perturbation process 
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}" \
    -d "${output_path}/lex" \
    -o "${output_path}/all" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}" \
    -n "${mode2}" \
    -e "${data_file_extension}"

# TODO
#mode="syn"