#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Extract replacement rules from linguistic features (lexicograpic | morphological | syntactical)

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/FEATURES"
output_path="/media/AllBlue/LanguageData/PERTURBS"
perturbation_type="" # lex | mor | syn
feature_validity="" # guess | relaxed | reason | authentic
dict_direction="" # "RightToLeft" | "LeftToRight"
extraction_method="direct" # direct | ?? something heuristic based ??
unit_frequency="1" # 5 # NOTE: Currently only used in mor, not in lex
unit_length="6" # 5 # NOTE: Currently only used in mor, not in lex
current_dir="$(dirname "$0")"
script_file="../launch/Perturbation_Extraction.sh"
script_path="${current_dir}/${script_file}"


# +++++++++++++++++++++++++++++++++++++++++++++++
# Bavarian - GERMAN 
src_lang="bar"
src_name="Bavarian"
trg_lang="deu"
trg_name="German"
echo "Processing: ${src_name} and ${trg_name}"

for feature_validity in relaxed ; do # guess relaxed reason authentic
    for perturbation_type in lex mor ; do
        #perturbation_type="lex"
        dict_direction="LeftToRight"
        bash "${script_path}" \
            -i "${input_path}" \
            -o "${output_path}" \
            -s "${src_lang}" \
            -a "${src_name}" \
            -t "${trg_lang}" \
            -b "${trg_name}" \
            -m "${perturbation_type}" \
            -n "${dict_direction}" \
            -f "${feature_validity}" \
            -e "${extraction_method}" \
            -u "${unit_frequency}" \
            -l "${unit_length}"
        #perturbation_type="mor"
        dict_direction="LeftToRight"
        bash "${script_path}" \
            -i "${input_path}" \
            -o "${output_path}" \
            -s "${src_lang}" \
            -a "${src_name}" \
            -t "${trg_lang}" \
            -b "${trg_name}" \
            -m "${perturbation_type}" \
            -n "${dict_direction}" \
            -f "${feature_validity}" \
            -e "${extraction_method}" \
            -u "${unit_frequency}" \
            -l "${unit_length}"
    done
done



# +++++++++++++++++++++++++++++++++++++++++++++++
# German - Bavarian 
src_lang="deu"
src_name="German"
trg_lang="bar"
trg_name="Bavarian"
echo "Processing: ${src_name} and ${trg_name}"

for feature_validity in relaxed ; do # guess reason authentic
    for perturbation_type in lex mor ; do
        #perturbation_type="lex"
        dict_direction="RightToLeft"
        bash "${script_path}" \
            -i "${input_path}" \
            -o "${output_path}" \
            -s "${src_lang}" \
            -a "${src_name}" \
            -t "${trg_lang}" \
            -b "${trg_name}" \
            -m "${perturbation_type}" \
            -n "${dict_direction}" \
            -f "${feature_validity}" \
            -e "${extraction_method}" \
            -u "${unit_frequency}" \
            -l "${unit_length}"
        #perturbation_type="mor"
        dict_direction="RightToLeft"
        bash "${script_path}" \
            -i "${input_path}" \
            -o "${output_path}" \
            -s "${src_lang}" \
            -a "${src_name}" \
            -t "${trg_lang}" \
            -b "${trg_name}" \
            -m "${perturbation_type}" \
            -n "${dict_direction}" \
            -f "${feature_validity}" \
            -e "${extraction_method}" \
            -u "${unit_frequency}" \
            -l "${unit_length}"
    done
done



# +++++++++++++++++++++++++++++++++++++++++++++++
# Alemannic - GERMAN 
# src_lang="als"
# src_name="Alemannic"
# trg_lang="deu"
# trg_name="German"
# echo "Processing: ${src_name} and ${trg_name}"

# perturbation_type="lex"
# dict_direction="LeftToRight"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${dict_direction}" \
#     -f "${feature_validity}"
# perturbation_type="mor"
# dict_direction="LeftToRight"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${dict_direction}" \
#     -f "${feature_validity}"

# +++++++++++++++++++++++++++++++++++++++++++++++
# German - Alemannic 
# src_lang="deu"
# src_name="German"
# trg_lang="als"
# trg_name="Alemannic"
# echo "Processing: ${src_name} and ${trg_name}"

# perturbation_type="lex"
# dict_direction="RightToLeft"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${dict_direction}" \
#     -f "${feature_validity}"
# perturbation_type="mor"
# dict_direction="RightToLeft"
# bash "${script_path}" \
#     -i "${input_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${perturbation_type}" \
#     -n "${dict_direction}" \
#     -f "${feature_validity}"





# TODO
#perturbation_type="syn"