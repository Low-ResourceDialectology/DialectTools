#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Translate English to standard 

# NOTE: Translating data from → to
# REFERENCE
# /PREP/opustools/bar-en/naive/test.en → /EXPERIMENT/2024SchuMATh/bar-en/naive/reference/German/English/NLLB/test.en

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/translate/NLLB.sh"

input_file="test"
output_file="test"
author_id="facebook"
model_id="nllb-200-3.3B"
model_name="3.3B"

# ++++++++++++++++++++++++++++++++++++++++++
# REFERENCE data

data_quality="naive" # "clean" | "informed"
for data_quality in naive clean ; do
    experiment="baseline" # "preprocessing" | "postprocessing"

    # Translate English text to Standard German
    src_name="Bavarian"
    src_lang="bar"

    trg_name="English"
    trg_lang="en"
    input_code="eng_Latn"

    translate_name="German"
    translate_lang="de"
    output_code="deu_Latn"

    input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
    output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${translate_name}/NLLB"

    echo "Translating ${input_file} via ${model_id} from ${trg_lang} to ${translate_lang}"; 
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
        -l ${model_name}
done