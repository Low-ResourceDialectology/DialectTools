#!/bin/bash
# Download parallel data for Sockeye
# Use: cd ./setup
#         bash Sockeye-Data-Test-bar-eng.sh /media/AllBlue/LanguageData/PREP/opustools bar en /media/AllBlue/LanguageData/DOWNLOAD/opustools

CURRENT="$PWD"

# First input argument
INPUTDIR="$1"
SOURCE="$2"
TARGET="$3"
DATADIR="${INPUTDIR}/${SOURCE}-${TARGET}"
mkdir "${DATADIR}" -p
cd "${DATADIR}"
source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate

# Second input argument
DOWNLOADDIR="$4"

opus_express -s bar -t en --download-dir "${DOWNLOADDIR}" --root-dir "${DOWNLOADDIR}" --collections 'XLEnt' 'Tatoeba' 'wikimedia' 'WikiMatrix' -q

cd "$CURRENT"


