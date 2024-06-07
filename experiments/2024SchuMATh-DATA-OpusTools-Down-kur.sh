#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Download text data via OpusTools for Kurdish varieties

current_dir="$(dirname "$0")"
script_file="$current_dir/../download/opustools.sh" 

# Kurmanji - English
output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="ku"
trg_lang="en"
bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"

output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="kmr"
trg_lang="en"
bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"

output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="ku_Latn"
trg_lang="en"
bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"

output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="ku_Arab"
trg_lang="en"
bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"

# Kurmanji - German
output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="ku"
trg_lang="de"
bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"

output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="kmr"
trg_lang="de"
bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"

output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="ku_Latn"
trg_lang="de"
bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"

output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="ku_Arab"
trg_lang="de"
bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"


# NOTE: WORK IN PROGRESS
# # Kurdish (Monolingual)
# script_file="$current_dir/../download/opustools_mono.sh" 
# output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
#for src_lang in ku kmr kur_Latn kur_Arab; do
    # bash "${script_file}" \
    #     -o "${output_path}" \
    #     -s "${src_lang}"
#done