#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Evaluate the results of machine translation via reference files in sacreBLEU

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/evaluate/sacreBLEU.sh"

# Initialize variables and default values
input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/test-test/naive"
input_file_ref="test.deu"
input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/naive/postprocess/test-test"
input_file_inf="test.bar"

dir_name="2024SchuMATh-Pipeline10-TEST"
output_path="/media/AllBlue/LanguageData/LOGS/${dir_name}"
output_file="naive_postprocess_deu-bar.txt"

experiment="postprocess"
metrics="bleu chrf ter"
precision="4"
options=""

echo "Evaluating machine translation via sacreBLEU writing to: ${output_path}/${output_file}"; 
bash "${script_file}" \
    -a "${input_path_ref}" \
    -b "${input_file_ref}" \
    -c "${input_path_inf}" \
    -d "${input_file_inf}" \
    -e "${output_path}" \
    -f "${output_file}" \
    -g "${experiment}" \
    -h "${metrics}" \
    -i "${precision}" \
    -j "${options}" 