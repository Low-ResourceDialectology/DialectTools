#!/bin/bash
# Install a (by name) specified list of tools into target directory
# Use: cd ./download
#         bash /media/CrazyProjects/LowResDialectology/DialectData/download/opustools.sh /media/AllBlue/LanguageData ku-Latn ku-Arab

CURRENT="$PWD"

source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate

# First input argument: Target directory
DATADIR="$1"
DOWNLOADDIR="${DATADIR}/DOWNLOAD/opustools"

# Second input argument: Source language
SOURCE="$2"

# Second input argument: Target language
TARGET="$3"

# List all corpora with this language pair
CORPORASTRING=$(opus_get --list_corpora --source "${SOURCE}" --target "${TARGET}")
#CORPORASTRING=$(opus_get --list_corpora --source "${SOURCE}")
echo "List of found corpora: ${CORPORASTRING}"
IFS=', ' read -r -a CORPORA <<< "${CORPORASTRING}"
for CORPUS in "${CORPORA[@]}"; do
	#echo "${CORPUS}"
	echo "Downloading from ${CORPUS} for ${SOURCE}-${TARGET}."
	opus_get --directory "${CORPUS}" --source "${SOURCE}" --target "${TARGET}" --download_dir "${DOWNLOADDIR}" --suppress_prompts
done


cd "$CURRENT"


