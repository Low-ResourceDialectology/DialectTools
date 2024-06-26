#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Extract linguistic features (lexicograpic) from bidictionaries

# Initialize variables and default values
input_path="" #"/media/AllBlue/LanguageData/DICT"
output_path="" #"/media/AllBlue/LanguageData/FEATURES"
src_lang="" #"als"
src_name="" #"Alemannic"
trg_lang="" #"deu"
trg_name="" #"German"
current_dir="$(dirname "$0")"
script_file="features_lex.py"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -o output_path -s src_lang -a srg_name -b trg_name -t trg_lang -c script_file"
exit 1
}

# Parse command-line options
while getopts ":i:o:s:a:t:b:c:" opt; do
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
        a)
            src_name=$OPTARG
            ;;
        t)
            trg_lang=$OPTARG
            ;;
        b)
            trg_name=$OPTARG
            ;;
		c)
	        script_file=$OPTARG
	        ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$src_name" ] || [ -z "$trg_lang" ] || [ -z "$trg_name" ] || [ -z "$script_file" ]; then
    usage
fi

script_path="${current_dir}/${script_file}"

#echo "Lexical features for ${src_name} and ${trg_name}"
python3 "${script_path}" \
    --input_dir "${input_path}" \
    --output_dir "${output_path}" \
    --src_lang "${src_lang}" \
    --src_name "${src_name}" \
    --trg_lang "${trg_lang}" \
    --trg_name "${trg_name}"