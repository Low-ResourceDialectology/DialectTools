#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Translate Standard to English and evaluate via Reference

# TODO: Add additionaly evaluation metrics

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/translate/NLLB.sh"

input_path=""
input_file="test"
input_extension="ckb_Arab"
src_lang="ckb"
output_path="/media/AllBlue/LanguageData/EXPERIMENT"
output_file="test"
output_extension="eng_Latn"
trg_lang="eng"
experiment="2024SchuMATh-NLLB-Baseline-ckb"
author_id="facebook"
model_id="nllb-200-3.3B"
model_name="3.3B"

for input_file in "${input_path}"/*; do 
    echo "Translating $input_file via $model_id"; 
    bash "${script_file}" \
        -a ${input_path} \
        -b ${input_file} \
        -c ${input_extension} \
        -d ${src_lang} \
        -e ${output_path} \
        -f ${output_file} \
        -g ${output_extension} \
        -h ${trg_lang} \
        -i ${experiment} \
        -j ${author_id} \
        -k ${model_id} \
        -l ${model_name}    
done



