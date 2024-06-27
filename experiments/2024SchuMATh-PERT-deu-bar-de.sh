#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Apply replacement rules (lexicograpic | morphological | syntactical) on text to perturb it 

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/PERTURBS"
data_path="/media/AllBlue/LanguageData/PREP/opustools/bar-de" # TODO: Split up and make modular for data-sources and language pairs "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive"
output_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh"
perturbation_type="" # lex | mor | syn 
data_quality="clean" # naive | clean | informed  # → Change variable here for each "Phase"
feature_validity="reason" # guess | reason | authentic # → Change variable here for each "Phase"
current_dir="$(dirname "$0")"
script_file="../launch/Perturbation_Application.sh"
script_path="${current_dir}/${script_file}"


# +++++++++++++++++++++++++++++++++++++++++++++++
# Bavarian - German 
src_lang="bar"
src_name="Bavarian"
trg_lang="deu"
trg_name="German"
data_file_extension="noname"
echo "Perturbing: ${src_name} into ${trg_name}"

perturbation_type="lex"
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}/${feature_validity}" \
    -d "${data_path}/${data_quality}" \
    -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${perturbation_type}" \
    -n "${data_quality}" \
    -e "${data_file_extension}" \
    -f "${feature_validity}"

perturbation_type="mor"
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}/${feature_validity}" \
    -d "${data_path}/${data_quality}" \
    -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${perturbation_type}" \
    -n "${data_quality}" \
    -e "${data_file_extension}" \
    -f "${feature_validity}"

# perturbation_type="all" # Again morphological, but on the results from the lexicographic perturbation process 
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}/${feature_validity}" \
#     -d "${output_path}/${src_name}/${data_quality}/${trg_name}/lex" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}" \
#     -e "${data_file_extension}" \
#     -f "${feature_validity}"

# # TODO
# #perturbation_type="syn"



# +++++++++++++++++++++++++++++++++++++++++++++++
# German - Bavarian 
src_lang="deu"
src_name="German"
trg_lang="bar"
trg_name="Bavarian"
data_file_extension="noname"
echo "Perturbing: ${src_name} into ${trg_name}"

perturbation_type="lex"
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}/${feature_validity}" \
    -d "${data_path}/${data_quality}" \
    -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${perturbation_type}" \
    -n "${data_quality}" \
    -e "${data_file_extension}" \
    -f "${feature_validity}"

perturbation_type="mor"
bash "${script_path}" \
    -i "${input_path}/${src_name}/${trg_name}/${feature_validity}" \
    -d "${data_path}/${data_quality}" \
    -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${perturbation_type}" \
    -n "${data_quality}" \
    -e "${data_file_extension}" \
    -f "${feature_validity}"

# perturbation_type="all" # Again morphological, but on the results from the lexicographic perturbation process 
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}/${feature_validity}" \
#     -d "${output_path}/${src_name}/${data_quality}/${trg_name}/lex" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}" \
#     -e "${data_file_extension}" \
#     -f "${feature_validity}"

# TODO
#perturbation_type="syn"




# +++++++++++++++++++++++++++++++++++++++++++++++
# Alemannic - German 
# src_lang="als"
# src_name="Alemannic"
# trg_lang="deu"
# trg_name="German"
# data_file_extension="noname"
# echo "Perturbing: ${src_name} into ${trg_name}"

# perturbation_type="lex"
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${data_path}/${data_quality}" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}" \
#     -e "${data_file_extension}"

# perturbation_type="mor"
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${data_path}/${data_quality}" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}" \
#     -e "${data_file_extension}"

# perturbation_type="all" # Again morphological, but on the results from the lexicographic perturbation process 
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${output_path}/${src_name}/${data_quality}/${trg_name}/lex" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}" \
#     -e "${data_file_extension}"

# TODO
#perturbation_type="syn"



# +++++++++++++++++++++++++++++++++++++++++++++++
# German - Alemannic 
# src_lang="deu"
# src_name="German"
# trg_lang="als"
# trg_name="Alemannic"
# data_file_extension="noname"
# echo "Perturbing: ${src_name} into ${trg_name}"

# perturbation_type="lex"
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${data_path}/${data_quality}" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}" \
#     -e "${data_file_extension}"

# perturbation_type="mor"
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${data_path}/${data_quality}" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}" \
#     -e "${data_file_extension}"

# perturbation_type="all" # Again morphological, but on the results from the lexicographic perturbation process 
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${output_path}/${src_name}/${data_quality}/${trg_name}/lex" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}" \
#     -e "${data_file_extension}"

# TODO
#perturbation_type="syn"






# TODO
# +++++++++++++++++++++++++++++++++++++++++++++++
# Alemannic - GERMAN 
# src_lang="als"
# src_name="Alemannic"
# trg_lang="deu"
# trg_name="German"
# echo "Perturbing: ${src_name} into ${trg_name}"

# perturbation_type="lex"
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${data_path}/${data_quality}" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}"

# perturbation_type="mor"
# bash "${script_path}" \
#     -i "${input_path}/${src_name}/${trg_name}" \
#     -d "${data_path}/${data_quality}" \
#     -o "${output_path}/${src_name}/${data_quality}/${trg_name}/${perturbation_type}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${data_quality}"

# TODO
#perturbation_type="syn"
