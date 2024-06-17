#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Evaluate the results of machine translation via reference files in sacreBLEU

# NOTE: Reference-data and test-data (after translation by NLLB)
# REFERENCE
# /EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB/test.en
# "Reference" of Bavarian text directly translated into English
# /EXPERIMENT/2024SchuMATh/bar-de/naive/reference/Bavarian/English/NLLB/test.en
# Phase 1: NAIVE & GUESS
# /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/all/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/lex/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/mor/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/all/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/lex/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/mor/English/NLLB/test.en

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/evaluate/sacreBLEU.sh"

# Initialize variables and default values
input_path_ref=""
input_file_ref=""
input_path_inf=""
input_file_inf=""
output_path=""
output_file=""
metrics="bleu chrf ter"
precision="4"
options=""

# ++++++++++++++++++++++++++++++++++++++++++++
# Evaluate Perturbations (How close do we get to the other language variety?)
input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive" 
input_file_ref="test.de"
src_name="Bavarian"
src_lang="bar"
trg_name="German"
trg_lang="de"
echo "Evaluating perturbations via sacreBLEU for: ${src_name} to ${trg_name}";

for data_quality in naive; # naive clean informed
do
    for feature_validity in guess; # guess reason authentic
    do
        for perturbation_type in all lex mor;
        do
            input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}"
            input_file_inf="test.${src_lang}"
            output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
            output_file="PERT.txt"
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
    done
done

input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive" 
input_file_ref="test.de"
src_name="German"
src_lang="de"
trg_name="Bavarian"
trg_lang="bar"
echo "Evaluating perturbations via sacreBLEU for: ${src_name} to ${trg_name}";


for data_quality in naive; # naive clean informed
do
    for feature_validity in guess; # guess reason authentic
    do
        for perturbation_type in all lex mor;
        do
            input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}"
            input_file_inf="test.${src_lang}"
            output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
            output_file="PERT.txt"
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
    done
done




# ++++++++++++++++++++++++++++++++++++++++++++
# Evaluate Translations
# NOTE: Same reference file for all translations below
input_path_ref="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB" 
input_file_ref="test.en"

# Evaluate the translation of Bavarian (standardized) into English
src_name="Bavarian"
src_lang="bar"
trg_name="German"
trg_lang="de"
translate_name="English"
translate_lang="en"

echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
for data_quality in naive; # naive clean informed
do
    for feature_validity in guess; # guess reason authentic
    do
        for perturbation_type in all lex mor;
        do
            input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}/${translate_name}/NLLB"
            input_file_inf="test.de"
            output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
            output_file="NLLB.txt"
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
    done
done

# Evaluate the translation of German (dialectized) into English
src_name="German"
src_lang="de"
trg_name="Bavarian"
trg_lang="bar"
translate_name="English"
translate_lang="en"

echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
for data_quality in naive; # naive clean informed
do
    for feature_validity in guess; # guess reason authentic
    do
        for perturbation_type in all lex mor;
        do
            input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}/${translate_name}/NLLB"
            input_file_inf="test.de"
            output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
            output_file="NLLB.txt"
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
    done
done





