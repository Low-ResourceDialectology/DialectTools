#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Clean opustools data

source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

current_dir="$(dirname "$0")"
script_file="opustools.py"

input_path="" # "/media/AllBlue/LanguageData/CLEAN/opustools"
output_path="" # "/media/AllBlue/LanguageData/CLEAN/opustools"
src_lang="" # "bar"
trg_lang="" # "de"
data_quality="" # "clean" | "informed"  (naive automatically happens during extraction)
cosine_filtering="" # "True"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -o output_path -s src_lang -t trg_lang -d data_quality -c cosine_filtering"
exit 1
}

# Parse command-line options
while getopts ":i:o:s:t:d:c:" opt; do
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
		d)
	        data_quality=$OPTARG
	        ;;
        c)
	        cosine_filtering=$OPTARG
	        ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$trg_lang" ] || [ -z "$data_quality" ] || [ -z "$cosine_filtering" ]; then
    usage
fi

script_path="${current_dir}/${script_file}"

python3 "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -t "${trg_lang}" \
    -d "${data_quality}" \
    -c "${cosine_filtering}"

