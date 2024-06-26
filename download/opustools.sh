#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Download all available (aligned) data for language pair from Opus

# Initialize variables and default values
output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="" # ku-Latn
trg_lang="" # ku-Arab

current_dir="$(dirname "$0")"

# Function to print usage
usage() {
echo "Usage: $0 -o output_path -s src_lang -t trg_lang"
exit 1
}

# Parse command-line options
while getopts ":o:s:t:" opt; do
    case $opt in
        o)
            output_path=$OPTARG
            ;;
		s)
            src_lang=$OPTARG
            ;;
        t)
            trg_lang=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$trg_lang" ] ; then
    usage
fi

source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate

# List all corpora with this language pair
CORPORASTRING=$(opus_get --list_corpora --source "${src_lang}" --target "${trg_lang}")
#CORPORASTRING=$(opus_get --list_corpora --source "${src_lang}")
echo "List of found corpora: ${CORPORASTRING}"
IFS=', ' read -r -a CORPORA <<< "${CORPORASTRING}"
for CORPUS in "${CORPORA[@]}"; do
	#echo "${CORPUS}"
	echo "Downloading from ${CORPUS} for ${src_lang}-${trg_lang}."
	opus_get --directory "${CORPUS}" --source "${src_lang}" --target "${trg_lang}" --download_dir "${output_path}" --suppress_prompts
done
