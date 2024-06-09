#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Aggregates manually collected (cross-lingually aligned) wordlists into clean format

# Initialize variables and default values
# NOTE: Add directory processing, for now only one file
#input_path="/media/AllBlue/LanguageData/DOWNLOAD/handmade/wordlists"
#input_file="/media/AllBlue/LanguageData/DOWNLOAD/handmade/wordlists/Kurdish.csv"

# KURDISH WORDLIST
input_path="/media/AllBlue/LanguageData/DOWNLOAD/handmade/wordlists/Kurdish.csv"
filename="Kurdish-Test"

# GERMAN WORDLIST
# input_path="/media/AllBlue/LanguageData/DOWNLOAD/handmade/wordlists/German.json"
# filename="German-Test"


output_path="/media/AllBlue/LanguageData/CLEAN/handmade/wordlists"
lists=false
current_dir="$(dirname "$0")"
script_file="../function/clean/manual2wordlist.py"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -o output_path -f filename -l list_output_flag"
exit 1
}

# Parse command-line options
while getopts ":i:o:f:l:" opt; do
    case $opt in
        i)
            input_path=$OPTARG
            ;;
        o)
            output_path=$OPTARG
            ;;
        f)
            filename=$OPTARG
            ;;
        l)
            flag=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done
# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$output_path" ] || [ -z "$filename" ]; then
    usage
fi

mkdir -p "${output_path}"
source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate
script_path="${current_dir}/${script_file}"

python3 "${script_path}" -i "${input_path}" -o "${output_path}" -f "${filename}"

