#!/bin/bash
# Downloading Kurmanji data from various sources via OpusTools

###############################################################################
# Find corpora for a language
#source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate

# for SOURCE in ku kmr ku_Latn ku_Arab; do
#     opus_get --list_corpora --source "${SOURCE}"
#     # This executes: 
#     # opus_get --list_corpora --source ku        # → Bianet, CCAligned, GlobalVoices, GNOME, KDE4, MultiCCAligned, NeuLab-TedTalks, QED, Tanzil, Tatoeba, TED2020, tico-19, Ubuntu, wikimedia
#     # opus_get --list_corpora --source kmr       # → Mozilla-I10n, Tatoeba
#     # opus_get --list_corpora --source ku_Latn   # → NLLB
#     # opus_get --list_corpora --source ku_Arab   # → NLLB
# done
# NOTE: ku-Latn and ku-Arab do not yield any results, even though, something can be found via the Opus-Website
# NOTE: While the Opus-Website shows "ku-Latn" and "ku-Arab" as languages codes, the OpusTools expects "ku_Latn" and "ku_Arab"


###############################################################################
# Find corpora for a language pair
# for SOURCE in ku kmr ku_Latn ku_Arab; do
#     for TARGET in de en; do
#         opus_get --list_corpora --source "${SOURCE}" --target "${TARGET}"
#         # This executes: 
#         # opus_get --list_corpora --source ku --target de
#             # → GNOME, KDE4, MultiCCAligned, NeuLab-TedTalks, QED, Tanzil, Tatoeba, TED2020, Ubuntu, wikimedia
#         # opus_get --list_corpora --source ku --target en
#             # → Bianet, CCAligned, GlobalVoices, GNOME, KDE4, NeuLab-TedTalks, QED, Tanzil, Tatoeba, TED2020, tico-19, Ubuntu, wikimedia
#         # opus_get --list_corpora --source kmr --target de
#             # → Mozilla-I10n, Tatoeba
#         # opus_get --list_corpora --source kmr --target en
#             # → Mozilla-I10n, Tatoeba
#         # opus_get --list_corpora --source ku_Latn --target de
#             # → 
#         # opus_get --list_corpora --source ku_Latn --target en
#             # → NLLB
#         # opus_get --list_corpora --source ku_Arab --target de
#             # → 
#         # opus_get --list_corpora --source ku_Arab --target en
#             # → 
#     done
# done


###############################################################################
# Language Pairs via Script: Various language tags of Kurmanji Kurdiah with German and English
# for SOURCE in ku kmr ku_Latn ku_Arab; do
#     for TARGET in de en; do
#         bash /media/CrazyProjects/LowResDialectology/DialectData/download/opustools.sh /media/AllBlue/LanguageData "${SOURCE}" "${TARGET}"
#         bash /media/CrazyProjects/LowResDialectology/DialectData/download/opustools.sh /media/AllBlue/LanguageData "${SOURCE}" "${TARGET}"
#     done
# done

# NOTE: During the downloading of data for language pairs via the opustools.sh script, the list of found corpora is printed to console.
#       These lists can then be used to acquire the alignments between de (German) and en (English) in addition to the already downloaded text data.
#       TODO: Introduce input argument to the opustools.sh script to automatically collect these alignments 


###############################################################################
# Also get the alignments between German and English for the above corpora

# TODO: The following code does not download anything??!! 
# source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate
# SOURCE="de"
# TARGET="en"
# DOWNLOADDIR="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
# for CORPUS in GNOME, KDE4, MultiCCAligned, NeuLab-TedTalks, QED, Tanzil, Tatoeba, TED2020, Ubuntu, wikimedia, Bianet, CCAligned, GlobalVoices, GNOME, tico-19; do
#     echo "Downloading from ${CORPUS} for ${SOURCE}-${TARGET}."
#     opus_get --directory "${CORPUS}" --source "${SOURCE}" --target "${TARGET}" --download_dir "${DOWNLOADDIR}" --suppress_prompts
#     # This executes:
#     # opus_get --directory GNOME --source de --target en --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools" --suppress_prompts
#     # → 
# done
# NOTE: This does nothing:
# opus_get --directory MultiCCAligned --source de --target en --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools"
# NOTE: This does work and downloads 962 MB of Chinese text data:
# opus_get --directory MultiCCAligned --source ku --target zh_CN --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools"


###############################################################################
# Download the monolingual data for Kurmanji
# TODO: Work in progress and did weird things for "bar" (Bavarian) as input...
#SOURCE="bar"
#opus_get --source "${SOURCE}" --preprocess mono --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools" --suppress_prompts

# TODO: This line first downloads a lot of "bar" data and then... continues... Probably until it got all the 983 GB of Opus done??
#opus_get --source bar --preprocess raw --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools" --suppress_prompts


###############################################################################
# Extract the collected data into a raw text format
# source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate
# DOWNLOADOPUS="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
# CLEANOPUS="/media/AllBlue/LanguageData/CLEAN/opustools"
# mkdir "${CLEANOPUS}" -p
# PREPOPUS="/media/AllBlue/LanguageData/PREP/opustools"
# mkdir "${PREPOPUS}" -p

# SOURCE="ku"
# for TARGET in de en; do
#     mkdir "${CLEANOPUS}"/"${SOURCE}"-"${TARGET}" -p
#     mkdir "${PREPOPUS}"/"${SOURCE}"-"${TARGET}" -p
#     CORPORAKOMMA=$(opus_get --list_corpora --source "${SOURCE}" --target "${TARGET}")
#     #CORPORA=$("${CORPORAKOMMA}" | tr ',' ' ')
#     CORPORA=$(echo "${CORPORAKOMMA//,/ }")

#     for CORPUS in ${CORPORA[@]}; do        
#         opus_read --root_directory "${DOWNLOADOPUS}" \
#         --download_dir "${DOWNLOADOPUS}" \
#         --directory "${CORPUS}" \
#         --source "${SOURCE}" \
#         --target "${TARGET}" \
#         --write "${CLEANOPUS}"/"${SOURCE}"-"${TARGET}"/"${CORPUS}"-"${SOURCE}"-"${TARGET}"."${SOURCE}" "${CLEANOPUS}"/"${SOURCE}"-"${TARGET}"/"${CORPUS}"-"${SOURCE}"-"${TARGET}"."${TARGET}" \
#         --write_mode moses
#     done
# done

