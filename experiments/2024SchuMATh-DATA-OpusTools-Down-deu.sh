#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Download text data via OpusTools for German varieties

current_dir="$(dirname "$0")"
script_file="$current_dir/../download/opustools.sh" 

# Bavarian - German
output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="bar"
trg_lang="de"

bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"


# Bavarian - English
output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="bar"
trg_lang="en"

bash "${script_file}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}"


# German - English (But only the same corpora as the above had, to prevent absolute overkill from happening)
script_file="$current_dir/../download/opustools_corpus.sh" 
output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="de"
trg_lang="en"

for corpus in Tatoeba WikiMatrix wikimedia XLEnt; do
    bash "${script_file}" \
        -o "${output_path}" \
        -s "${src_lang}" \
        -t "${trg_lang}" \
        -c "${corpus}"
done

# NOTE: WORK IN PROGRESS
# # Bavarian (Monolingual)
# script_file="$current_dir/../download/opustools_mono.sh" 
# output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
# src_lang="bar"

# bash "${script_file}" \
#     -o "${output_path}" \
#     -s "${src_lang}"