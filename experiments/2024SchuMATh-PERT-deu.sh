#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Apply replacement rules (lexicograpic | morphological | syntactical) on text to perturb it 

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/PERTURBS"
data_path="/media/AllBlue/LanguageData/PREP/opustools/bar-de" # TODO: Split up and make modular for data-sources and language pairs "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive"
output_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh"
mode="lex" # lex | mor | syn
mode2="naive" # naive | clean | informed
current_dir="$(dirname "$0")"
script_file="../launch/Perturbation_Application.sh"
script_path="${current_dir}/${script_file}"

# +++++++++++++++++++++++++++++++++++++++++++++++
# Alemannic - GERMAN 
# src_lang="als"
# src_name="Alemannic"
# trg_lang="deu"
# trg_name="German"
# echo "Perturbing: ${src_name} into ${trg_name}"

# mode="lex"
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${data_path}/${mode2}" \
#     -o "${output_path}/${src_name}/${mode2}/${trg_name}/${mode}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${mode}" \
#     -n "${mode2}"

# mode="mor"
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${data_path}/${mode2}" \
#     -o "${output_path}/${src_name}/${mode2}/${trg_name}/${mode}" \
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
echo "Perturbing: ${src_name} into ${trg_name}"

mode="lex"
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}" \
    -d "${data_path}/${mode2}" \
    -o "${output_path}/${src_name}/${mode2}/${trg_name}/${mode}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}" \
    -n "${mode2}"

mode="mor"
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}" \
    -d "${data_path}/${mode2}" \
    -o "${output_path}/${src_name}/${mode2}/${trg_name}/${mode}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${mode}" \
    -n "${mode2}"

# mode="mor" # Again morphological, but on the results from the lexicographic perturbation process 
# bash "${script_path}" \
#     -i "${output_path}/${src_name}/${mode2}/${trg_name}/lex" \
#     -d "${data_path}/${mode2}" \
#     -o "${output_path}/${src_name}/${mode2}/${trg_name}/${mode}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${mode}" \
#     -n "${mode2}"

# TODO
#mode="syn"