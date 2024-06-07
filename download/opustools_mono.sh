#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Download all monolingual data for language from Opus

echo "WARNING: This script download seemingly all languages of the corpora that contain the source language?!"

# Initialize variables and default values
output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="" # ku-Latn

current_dir="$(dirname "$0")"
source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate

# Function to print usage
usage() {
echo "Usage: $0 -o output_path -s src_lang"
exit 1
}

# Parse command-line options
while getopts ":o:s:" opt; do
    case $opt in
        o)
            output_path=$OPTARG
            ;;
		s)
            src_lang=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$output_path" ] || [ -z "$src_lang" ] ; then
    usage
fi

# List all corpora with this language pair
CORPORASTRING=$(opus_get --list_corpora --source "${src_lang}")

echo "List of found corpora: ${CORPORASTRING}"
IFS=', ' read -r -a CORPORA <<< "${CORPORASTRING}"
for CORPUS in "${CORPORA[@]}"; do
	#echo "${CORPUS}"
	echo "Downloading from ${CORPUS} for ${src_lang}."
	opus_get --directory "${CORPUS}" --source "${src_lang}" --download_dir "${output_path}" --suppress_prompts
done
