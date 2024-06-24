#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Apply replacement rules (lexicograpic | morphological | syntactical) on text to perturb it 

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/PERTURBS"
data_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/English/German/NLLB" # TODO: Split up and make modular for data-sources and language pairs "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive"
output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/English/German/NLLB/Bavarian"
perturbation_type="" # lex | mor | syn
data_quality="clean" # naive | clean | informed # → Change variable here for each "Phase"
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

perturbation_type="lex"
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}" \
    -d "${data_path}" \
    -o "${output_path}/lex" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${perturbation_type}" \
    -n "${data_quality}" \
    -e "${data_file_extension}"

perturbation_type="mor"
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}" \
    -d "${data_path}" \
    -o "${output_path}/mor" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${perturbation_type}" \
    -n "${data_quality}" \
    -e "${data_file_extension}"

# perturbation_type="all" # Again morphological, but on the results from the lexicographic perturbation process 
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${output_path}/lex" \
#     -o "${output_path}/all" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}" \
#     -e "${data_file_extension}"

# TODO
#perturbation_type="syn"