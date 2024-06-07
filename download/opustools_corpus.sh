#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Resctrict download to a specific corpus for (aligned) data of a language pair from Opus

# Initialize variables and default values
output_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
src_lang="" # ku-Latn
trg_lang="" # ku-Arab
corpus="" # Tatoeba

current_dir="$(dirname "$0")"
source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate

# Function to print usage
usage() {
echo "Usage: $0 -o output_path -s src_lang -t trg_lang -c corpus"
exit 1
}

# Parse command-line options
while getopts ":o:s:t:c:" opt; do
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
        c)
            corpus=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$trg_lang" ] || [ -z "$corpus" ]; then
    usage
fi

echo "Downloading from ${corpus} for ${src_lang}-${trg_lang}."
opus_get --directory "${corpus}" --source "${src_lang}" --target "${trg_lang}" --download_dir "${output_path}" --suppress_prompts

