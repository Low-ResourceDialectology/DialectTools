#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Translate Standard to English and evaluate via Reference

# TODO: Add additionaly evaluation metrics

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/translate/NLLB.sh"

directory="bar-en"
src_lang="en"
trg_lang="de"
input_code="eng_Latn"
output_code="deu_Latn"
input_file="test"
output_file="test"
data_quality="naive"
experiment="postprocess"
input_path="/media/AllBlue/LanguageData/PREP/opustools/${directory}/${data_quality}"
output_path="/media/AllBlue/LanguageData/EXPERIMENT/${data_quality}/${experiment}/${directory}"
#input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
#output_path="/media/AllBlue/LanguageData/EXPERIMENT/${data_quality}/${experiment}/${src_lang}-${trg_lang}"
author_id="facebook"
model_id="nllb-200-3.3B"
model_name="3.3B"
chunk_size="120"

echo "Translating ${input_file} via ${model_id} from ${src_lang} to ${trg_lang}"; 
bash "${script_file}" \
    -a ${input_path} \
    -b ${input_file} \
    -c ${src_lang} \
    -d ${input_code} \
    -e ${output_path} \
    -f ${output_file} \
    -g ${trg_lang} \
    -h ${output_code} \
    -i ${experiment} \
    -j ${author_id} \
    -k ${model_id} \
    -l ${model_name} \
    -m ${chunk_size}

