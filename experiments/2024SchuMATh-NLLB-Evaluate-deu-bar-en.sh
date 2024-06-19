#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Evaluate the results of machine translation via reference files in sacreBLEU

# NOTE: Reference-data and test-data (after translation by NLLB)
# REFERENCE
# /PREP/opustools/bar-en/naive/test.bar
# "Reference" of Bavarian text originally aligned with English
# Phase 1: NAIVE & GUESS of "English text, translated into German and perturbed into Bavarian"
# /EXPERIMENT/2024SchuMATh/Bavarian/naive/English/NLLB//Bavarian/all/test.en
# /EXPERIMENT/2024SchuMATh/Bavarian/naive/English/NLLB//Bavarian/lex/test.en
# /EXPERIMENT/2024SchuMATh/Bavarian/naive/English/NLLB//Bavarian/mor/test.en

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/evaluate/sacreBLEU.sh"

# Initialize variables and default values
input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-en/naive"
input_file_ref="test.bar"
input_path_inf=""
input_file_inf=""
output_path=""
output_file=""
metrics="bleu chrf ter"
precision="4"
options=""

# (Postprocessing) Evaluate the translation of English into German then perturbing into Bavarian
src_name="English"
src_lang="en"
trg_name="Bavarian"
trg_lang="bar"
translation_name="German"
translation_lang="de"

echo "Evaluating translation model performance for language variety via sacreBLEU for: ${src_name} to ${translation_name} perturbed to ${trg_name}";
input_path_inf="" #/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${trg_name}/${translation_name}/NLLB/${trg_name}"
input_file_inf="" # "test.en"
output_path="" # "/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/naive/guess/none"
output_file="" # "PERT.txt"
data_quality="naive"
feature_validity="guess"

for perturbation_type in all lex mor;
do
    input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${translation_name}/NLLB/${trg_name}/${perturbation_type}"
    input_file_inf="test.${src_lang}"
    output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
    output_file="POST.txt"
    bash "${script_file}" \
        -a "${input_path_ref}" \
        -b "${input_file_ref}" \
        -c "${input_path_inf}" \
        -d "${input_file_inf}" \
        -e "${output_path}" \
        -f "${output_file}" \
        -h "${metrics}" \
        -i "${precision}" \
        -j "${options}" 
done



