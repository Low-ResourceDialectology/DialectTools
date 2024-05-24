#!/bin/bash
# Downloading Bavarian data from various sources

#bash /media/CrazyProjects/LowResDialectology/DialectData/download/opustools.sh /media/AllBlue/LanguageData bar de
#bash /media/CrazyProjects/LowResDialectology/DialectData/download/opustools.sh /media/AllBlue/LanguageData bar en

# → Tatoeba, WikiMatrix, wikimedia, XLEnt

source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate

# Also get the alignments between German and English

# SOURCE="de"
# TARGET="en"
# for CORPUS in Tatoeba WikiMatrix wikimedia XLEnt; do
#     echo "Downloading from ${CORPUS} for ${SOURCE}-${TARGET}."
#     opus_get --directory "${CORPUS}" --source "${SOURCE}" --target "${TARGET}" --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools" --suppress_prompts
# done

# Download the monolingual data for Bavarian

# TODO: This first downloads a lot of "bar" data and then... continues... Probably until it got all the 983 GB of Opus done??
#SOURCE="bar"
#opus_get --source "${SOURCE}" --preprocess raw --download_dir "/media/AllBlue/LanguageData/DOWNLOAD/opustools" --suppress_prompts



