#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Translate standard and dialect text to English

# NOTE: Translating data from → to
# REFERENCE
# /PREP/opustools/bar-de/naive/test.de → /EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB/test.en
# /PREP/opustools/bar-de/naive/test.bar → /EXPERIMENT/2024SchuMATh/bar-de/naive/reference/Bavarian/English/NLLB/test.en
# Phase 1: NAIVE & GUESS
# /PREP/2024SchuMATh/German/naive/Bavarian/all/test.de → /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/all/English/NLLB/test.en
# /PREP/2024SchuMATh/German/naive/Bavarian/lex/test.de → /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/lex/English/NLLB/test.en
# /PREP/2024SchuMATh/German/naive/Bavarian/mor/test.de → /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/mor/English/NLLB/test.en
# /PREP/2024SchuMATh/Bavarian/naive/German/all/test.de → /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/all/English/NLLB/test.en
# /PREP/2024SchuMATh/Bavarian/naive/German/lex/test.de → /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/lex/English/NLLB/test.en
# /PREP/2024SchuMATh/Bavarian/naive/German/mor/test.de → /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/mor/English/NLLB/test.en

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
experiment="baseline" # "preprocessing" | "postprocessing"

# Translate Bavarian text to English
src_name="Bavarian"
src_lang="bar"

trg_name="German"
trg_lang="de"
input_code="deu_Latn"

translate_name="English"
translate_lang="en"
output_code="eng_Latn"

input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${src_name}/${translate_name}/NLLB"

echo "Translating ${input_file} via ${model_id} from ${src_lang} to ${translate_lang}"; 
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


# Translate German text to English
src_name="Bavarian"
src_lang="bar"

trg_name="German"
trg_lang="de"
input_code="deu_Latn"

translate_name="English"
translate_lang="en"
output_code="eng_Latn"

input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${trg_name}/${translate_name}/NLLB"

echo "Translating ${input_file} via ${model_id} from ${src_lang} to ${translate_lang}"; 
bash "${script_file}" \
    -a ${input_path} \
    -b ${input_file} \
    -c ${trg_lang} \
    -d ${input_code} \
    -e ${output_path} \
    -f ${output_file} \
    -g ${trg_lang} \
    -h ${output_code} \
    -i ${experiment} \
    -j ${author_id} \
    -k ${model_id} \
    -l ${model_name}



# ++++++++++++++++++++++++++++++++++++++++++
# Phase 1 data - "naive" & "guess"

data_quality="naive" # "clean" | "informed"
experiment="baseline" # "preprocessing" | "postprocessing"

for perturbation_type in lex mor all;
do
    # Translate Bavarian text to English
    src_name="Bavarian"
    src_lang="bar"

    trg_name="German"
    trg_lang="de"
    input_code="deu_Latn"

    translate_name="English"
    translate_lang="en"
    output_code="eng_Latn"
    input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}"
    output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}/${translate_name}/NLLB"

    echo "Translating ${input_file} via ${model_id} from ${src_name} to ${translate_name}"; 
    bash "${script_file}" \
        -a ${input_path} \
        -b ${input_file} \
        -c ${src_lang} \
        -d ${input_code} \
        -e ${output_path} \
        -f ${output_file} \
        -g ${translate_lang} \
        -h ${output_code} \
        -i ${experiment} \
        -j ${author_id} \
        -k ${model_id} \
        -l ${model_name}

    # Translate German text to English
    src_name="Bavarian"
    src_lang="bar"

    trg_name="German"
    trg_lang="de"
    input_code="deu_Latn"

    translate_name="English"
    translate_lang="en"
    output_code="eng_Latn"

    input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${perturbation_type}"
    output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${perturbation_type}/${translate_name}/NLLB"

    echo "Translating ${input_file} via ${model_id} from ${trg_name} to ${translate_name}"; 
    bash "${script_file}" \
        -a ${input_path} \
        -b ${input_file} \
        -c ${trg_lang} \
        -d ${input_code} \
        -e ${output_path} \
        -f ${output_file} \
        -g ${translate_lang} \
        -h ${output_code} \
        -i ${experiment} \
        -j ${author_id} \
        -k ${model_id} \
        -l ${model_name}

done

