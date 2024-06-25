#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Extract linguistic features (lexicograpic | morphological | syntactical) from bidictionaries

# Initialize variables and default values
input_path="" # "/media/AllBlue/LanguageData/DICT"
output_path="" # "/media/AllBlue/LanguageData/FEATURES"
src_lang="" # "als"
src_name="" # "Alemannic"
trg_lang="" # "deu"
trg_name="" # "German"
perturbation_type="" # lex | mor | syn
extraction_method="direct" # direct | ?? something heuristic based ??
context_length="" # 1 | 2 | 3 # NOTE: Currently only used for morphemes, not for lex
current_dir="$(dirname "$0")"
script_file="../function/extract/features_lex.sh"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -o output_path -s src_lang -a src_name -b trg_name -t trg_lang -m perturbation_type -e extraction_method -c context_length"
exit 1
}

# Parse command-line options
while getopts ":i:o:s:a:b:t:m:e:c:" opt; do
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
            perturbation_type=$OPTARG
            ;;
        e)
            extraction_method=$OPTARG
            ;;
        c)
            context_length=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$src_name" ] || [ -z "$trg_lang" ] || [ -z "$trg_name" ]  || [ -z "$perturbation_type" ] || [ -z "$extraction_method" ] || [ -z "$context_length" ]; then
    usage
fi


if [ $perturbation_type = "lex" ]; then
    script_file="../function/extract/features_lex.sh"
    script_path="${current_dir}/${script_file}"
    echo "Lexicographic features for: ${src_name} and ${trg_name}"
    bash "${script_path}" \
    -i "${input_path}/${src_name}" \
    -o "${output_path}/${src_name}/${extraction_method}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}"
fi

if [ $perturbation_type = "mor" ]; then
    script_file="../function/extract/features_mor.sh"
    script_path="${current_dir}/${script_file}"
    echo "Morphological features for: ${src_name} and ${trg_name}"
    bash "${script_path}" \
    -i "${input_path}/${src_name}" \
    -o "${output_path}/${src_name}/${extraction_method}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -c "${context_length}"
fi

# if [ $perturbation_type = "syn" ]; then
#     script_file="../function/extract/features_syn.sh"
#     script_path="${current_dir}/${script_file}"
#     echo "Syntactical features for: ${src_name} and ${trg_name}"
#     bash "${script_path}" \
#     -i "${input_path}/${src_name}" \
#     -o "${output_path}/${src_name}/${extraction_method}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}"
# fi
