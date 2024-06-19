#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Remove all those sentences that are way too long (lenght of over 2000)

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/clean/exclude_long_sentences.py"

src_lang="bar"
trg_lang="en"
data_quality="naive"
input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
output_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
maximum_length=1800

input_file="blubb.en"
output_file="test.en"

echo "Remove long sentences from ${input_path}/${input_file} and save remaining sentences in ${output_path}/${output_file}"; 
python3 "${script_file}" \
    -i "${input_path}/${input_file}" \
    -o "${output_path}/${output_file}" \
    -m "${maximum_length}"

input_file="blubb.bar"
output_file="test.bar"

echo "Remove long sentences from ${input_path}/${input_file} and save remaining sentences in ${output_path}/${output_file}"; 
python3 "${script_file}" \
    -i "${input_path}/${input_file}" \
    -o "${output_path}/${output_file}" \
    -m "${maximum_length}"