#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Extract linguistic features (lexicograpic | morphological | syntactical) from bidictionaries

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/DICT"
output_path="/media/AllBlue/LanguageData/PERTURBS"
src_lang="als"
src_name="Alemannic"
trg_lang="deu"
trg_name="German"
mode="" # lex | mor | syn
current_dir="$(dirname "$0")"
script_file="../function/extract/perturbations_lex.sh"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -o output_path -s src_lang -a src_name -b trg_name -t trg_lang -m mode"
exit 1
}

# Parse command-line options
while getopts ":i:o:s:a:b:t:m:" opt; do
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
		m)
            mode=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$src_name" ] || [ -z "$trg_lang" ] || [ -z "$trg_name" ]  || [ -z "$mode" ] ; then
    usage
fi


if [ $mode = "lex" ]; then
    script_file="../function/extract/perturbations_lex.sh"
    script_path="${current_dir}/${script_file}"
    echo "Lexicographic replacements for: ${src_name} and ${trg_name}"
    bash "${script_path}" \
    -i "${input_path}/${src_name}" \
    -o "${output_path}/${src_name}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}"
fi

if [ $mode = "mor" ]; then
    script_file="../function/extract/perturbations_mor.sh"
    script_path="${current_dir}/${script_file}"
    echo "Morphological replacements for: ${src_name} and ${trg_name}"
    bash "${script_path}" \
    -i "${input_path}/${src_name}" \
    -o "${output_path}/${src_name}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}"
fi

# if [ $mode = "syn" ]; then
#     script_file="../function/extract/perturbations_syn.sh"
#     script_path="${current_dir}/${script_file}"
#     echo "Syntactical replacements for: ${src_name} and ${trg_name}"
#     bash "${script_path}" \
#     -i "${input_path}/${src_name}" \
#     -o "${output_path}/${src_name}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}"
# fi
