#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: 
# Read sentences from (second column) of multiple csv files and split into subsets for train/dev/test

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/CLEAN/wikidumps/clean"
output_path="/media/AllBlue/LanguageData/PREP/wikidumps"
languages=(als bar)
proportions="0.6,0.3,0.1"
column="1"
format_output="txt"

current_dir="$(dirname "$0")"
script_file="$current_dir/../extract/csv_split_text.py"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -o output_path -l lang1 lang2 langn -p proportions"
exit 1
}

# Parse command-line options
while getopts ":i:o:s:l:p:c:" opt; do
    case $opt in
        i)
            input_path=$OPTARG
            ;;
        o)
            output_path=$OPTARG
            ;;
        s)
	        script_file=$OPTARG
	        ;;
        l)
            # Capture all remaining arguments as languages
            for (( i = OPTIND - 1; i <= $#; i++ )); do
                if [[ ${!i} != -* ]]; then
                    languages+=("${!i}")
                else
                    break
                fi
            done
            ;;
        p)
            proportions=$OPTARG
            ;;
        c)
            column=$OPTARG
            ;;
        f)
            format_output=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done
# The `for` loop iterates over the positional parameters from `OPTIND - 1` to the end (`$#`).
# The loop breaks if it encounters another flag (`-`).

# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$output_path" ] || [ ${#languages[@]} -eq 0 ] || [ -z "$proportions" ] || [ -z "$column" ] || [ -z "$format_output" ]; then
    usage
fi

source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

for LANG in "${languages[@]}"; do
	echo "Processing: ${LANG}"
	python3 "${script_file}" \
		--input_dir "${input_path}/${LANG}" \
        --column "${column}" \
		--output_dir "${output_path}/${LANG}" \
		--proportions "${proportions}" \
        --language "${LANG}" \
        --format_output "${format_output}"
done