#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Extract text data into raw text format via OpusTools for German varieties

current_dir="$(dirname "$0")"
script_file="$current_dir/../extract/opustools.sh" 

# Kurdish (any) - English
input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="ku"
trg_lang="en"
corpora="Bianet CCAligned GlobalVoices GNOME KDE4 NeuLab-TedTalks QED Tanzil Tatoeba TED2020 tico-19 Ubuntu wikimedia"
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


# Kurdish (kmr) - English
input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="kmr"
trg_lang="en"
corpora="Mozilla-I10n Tatoeba"
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


# Kurdish (kmr Latin?) - English
input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="ku_Latn"
trg_lang="en"
corpora="NLLB"
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


# Kurdish (any) - German
input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="ku"
trg_lang="de"
corpora="GNOME KDE4 MultiCCAligned NeuLab-TedTalks QED Tanzil Tatoeba TED2020 Ubuntu wikimedia"
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


# Kurdish (kmr) - German
input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="kmr"
trg_lang="de"
corpora="Mozilla-I10n Tatoeba"
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


# # German - English (But only the same corpora as the above had, to prevent absolute overkill from happening)
# input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
# output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
# src_lang="de"
# trg_lang="en"
# corpora="Bianet CCAligned GlobalVoices GNOME KDE4 Mozilla-I10n MultiCCAligned NeuLab-TedTalks NLLB QED Tanzil Tatoeba TED2020 tico-19 Ubuntu wikimedia"
# mode="moses"
# for corpus in $corpora; do
#     bash "${script_file}" \
#         -i "${input_path}" \
#         -o "${output_path}" \
#         -s "${src_lang}" \
#         -t "${trg_lang}" \
#         -c "${corpus}" \
#         -m "${mode}"
# done
echo "Consider if it is worth the effort to collect German-English data from the same corpora, if you have already collected so much data during the collectiong of Bavarian (and related German-English) data..."
