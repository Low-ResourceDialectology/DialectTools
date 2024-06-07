#!/bin/bash

# Use: bash Wikidump_Dialects.sh -l als bar

###############################################################################
# → Once the structure is known, the dialect-info can directly be filtered out
# Handmade script with downloaded wikidumps - similar to the previous wikidumps2extract.py 
#   script as part of the wikidumps "cleaning" 

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/DOWNLOAD/wikidumps"
output_path="/media/AllBlue/LanguageData/CLEAN/wikidumps/info"
languages=()

# Function to print usage
usage() {
    echo "Usage: $0 -i input_path -o output_path -l lang1 lang2 ... " 
    exit 1
}

# Parse command-line options
while getopts ":i:o:l:" opt; do
    case $opt in
        i)
            input_path=$OPTARG
            ;;
        o)
            output_path=$OPTARG
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
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ ${#languages[@]} -eq 0 ] || [ -z "$input_path" ] || [ -z "$output_path" ]; then
    usage
fi
current_dir="$(dirname "$0")"
script_file="$current_dir/../clean/wikidumps2dialects.py"

echo "Currently work with hard-coded date as part of filenames."

for LANG in "${languages[@]}"; do # als bar #  NOTE: Could not identify any dialect-tags for: ku ckb de
    echo "Processing: ${LANG}"
    CURINDIR="$input_path/${LANG}"
    INFILE="${LANG}"wiki-20240501-pages-meta-current.xml.bz2
    OUTDIR="${output_path}/${LANG}"
    mkdir -p "$OUTDIR"
    OUTFILE="${LANG}"-dialects.json

    python3 "${script_file}" --code "${LANG}" \
    --input-dir "${CURINDIR}" --input-file "${INFILE}" \
    --output-dir "${OUTDIR}" --output-file "${OUTFILE}"
done
