#!/bin/bash
# Downloading Kurmanji data from various sources via OpusTools

###############################################################################
# Language Pairs via Script: Bavarian-German and Bavarian-English
for SOURCE in ku kmr ku-Latn ku-Arab; do
    for TARGET in de en; do
        bash /media/CrazyProjects/LowResDialectology/DialectData/download/opustools.sh /media/AllBlue/LanguageData "${SOURCE}" "${TARGET}"
        bash /media/CrazyProjects/LowResDialectology/DialectData/download/opustools.sh /media/AllBlue/LanguageData "${SOURCE}" "${TARGET}"
    done
done
# Corpora → Tatoeba, WikiMatrix, wikimedia, XLEnt

#source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate

###############################################################################
# Also get the alignments between German and English for the above corpora

# for SOURCE in ku kmr ku-Latn ku-Arab; do
#     for TARGET in de en; do
#         for CORPUS in Tatoeba WikiMatrix wikimedia XLEnt; do
#             echo "Downloading from ${CORPUS} for ${SOURCE}-${TARGET}."
#             opus_get --directory "${CORPUS}" --source "${SOURCE}" --target "${TARGET}" --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools" --suppress_prompts
#         done
#     done
# done

###############################################################################
# Download the monolingual data for Bavarian

#SOURCE="bar"
#opus_get --source "${SOURCE}" --preprocess mono --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools" --suppress_prompts

# TODO: This line first downloads a lot of "bar" data and then... continues... Probably until it got all the 983 GB of Opus done??
#opus_get --source bar --preprocess raw --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools" --suppress_prompts

###############################################################################
# Extract the collected data into a raw text format

# DOWNLOADOPUS="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
# CLEANOPUS="/media/AllBlue/LanguageData/CLEAN/opustools"
# mkdir "${CLEANOPUS}" -p
# PREPOPUS="/media/AllBlue/LanguageData/PREP/opustools"
# mkdir "${PREPOPUS}" -p

# mkdir "${CLEANOPUS}"/"${SOURCE}"-"${TARGET}" -p
# mkdir "${PREPOPUS}"/"${SOURCE}"-"${TARGET}" -p

# for CORPUS in Tatoeba WikiMatrix wikimedia XLEnt; do
#     opus_read --root_directory "${DOWNLOADOPUS}" \
#     --download_dir "${DOWNLOADOPUS}" \
#     --directory "${CORPUS}" \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --write "${CLEANOPUS}"/"${SOURCE}"-"${TARGET}"/"${CORPUS}"-"${SOURCE}"-"${TARGET}"."${SOURCE}" "${CLEANOPUS}"/"${SOURCE}"-"${TARGET}"/"${CORPUS}"-"${SOURCE}"-"${TARGET}"."${TARGET}" \
#     --write_mode moses
# done

###############################################################################
# Preprocess and clean the text data
#source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate
#python3 /media/CrazyProjects/LowResDialectology/DialectTools/clean/development-latin-parallel-corpus-split.py


###############################################################################
# Split text data into train/dev/test
# NOTE: Currently evaluating (and developing) based on the DialectBLI data splits that distinguish between human-annotated and machine-annotated data
# → Remove data designated to be "Test" or "Dev" from the above preprocessed data
#source  /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate
#python3 /media/CrazyProjects/LowResDialectology/DialectTools/clean/development-latin-parallel-corpus-split-removeDialectBLI.py


#####################################################
# End of data preprocessing, cleaning and splitting #
# Start of training and evaluation parts            #
#####################################################
