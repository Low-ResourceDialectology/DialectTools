#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Extract text data into raw text format via OpusTools for German varieties

current_dir="$(dirname "$0")"
script_file="$current_dir/../extract/opustools.sh" 

# Bavarian - German
input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="bar"
trg_lang="de"
corpora="Tatoeba WikiMatrix wikimedia XLEnt"
mode="moses"

for corpus in $corpora; do
    bash "${script_file}" \
        -i "${input_path}" \
        -o "${output_path}" \
        -s "${src_lang}" \
        -t "${trg_lang}" \
        -c "${corpus}" \
        -m "${mode}"
done


# Bavarian - English
input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="bar"
trg_lang="en"
corpora="Tatoeba WikiMatrix wikimedia XLEnt"
mode="moses"

for corpus in $corpora; do
    bash "${script_file}" \
        -i "${input_path}" \
        -o "${output_path}" \
        -s "${src_lang}" \
        -t "${trg_lang}" \
        -c "${corpus}" \
        -m "${mode}"
done


# German - English (But only the same corpora as the above had, to prevent absolute overkill from happening)
input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="de"
trg_lang="en"
corpora="Tatoeba WikiMatrix wikimedia XLEnt"
mode="moses"

for corpus in $corpora; do
    bash "${script_file}" \
        -i "${input_path}" \
        -o "${output_path}" \
        -s "${src_lang}" \
        -t "${trg_lang}" \
        -c "${corpus}" \
        -m "${mode}"
done