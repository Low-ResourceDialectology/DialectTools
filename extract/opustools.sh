#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Extract text data into raw text format via OpusTools for German varieties

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/DOWNLOAD/opustools"
output_path="/media/AllBlue/LanguageData/CLEAN/opustools"
corpus=""
src_lang=""
trg_lang=""
mode=""
current_dir="$(dirname "$0")"
script_file="../clean/wikidumps2dialects.py"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -o output_path -s src_lang -t trg_lang -c corpus -m mode"
exit 1
}

# Parse command-line options
while getopts ":i:o:s:t:c:m:" opt; do
    case $opt in
        i)
            input_path=$OPTARG
            ;;
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
        m)
            mode=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$trg_lang" ] || [ -z "$corpus" ] || [ -z "$mode" ]  || [ -z "$script_file" ]; then
    usage
fi

source /media/AllBlue/LanguageData/TOOLS/vOpusTools/bin/activate
echo "Extracting ${src_lang}-${trg_lang} from ${corpus} dataset into ${output_path}"
mkdir -p "${output_path}/${src_lang}-${trg_lang}"

opus_read --root_directory "${input_path}" \
    --download_dir "${input_path}" \
    --directory "${corpus}" \
    --source "${src_lang}" \
    --target "${trg_lang}" \
    --write "${output_path}/${src_lang}-${trg_lang}/${corpus}-${src_lang}-${trg_lang}.${src_lang}" "${output_path}/${src_lang}-${trg_lang}/${corpus}-${src_lang}-${trg_lang}.${trg_lang}" \
    --write_mode "${mode}"