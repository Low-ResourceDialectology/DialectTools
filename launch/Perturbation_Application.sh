#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Extract linguistic features (lexicograpic | morphological | syntactical) from bidictionaries

# Initialize variables and default values
input_path="" # "/media/AllBlue/LanguageData/PERTURBS/German/Alemannic"
data_path="" # "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive"
output_path="" # /media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Alemannic
src_lang="" # "als"
src_name="" # "Alemannic"
trg_lang="" # "deu"
trg_name="" # "German"
mode="" # lex | mor | syn
mode2="" # naive | clean | informed
current_dir="$(dirname "$0")"
script_file="../function/perturb/perturbations_lex.py"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -d data_path -o output_path -s src_lang -a src_name -b trg_name -t trg_lang -m mode -n mode2"
exit 1
}

# Parse command-line options
while getopts ":i:d:o:s:a:b:t:m:" opt; do
    case $opt in
        i)
            input_path=$OPTARG
            ;;
        d)
            data_path=$OPTARG
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
		n)
            mode2=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$data_path" ] || [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$src_name" ] || [ -z "$trg_lang" ] || [ -z "$trg_name" ]  || [ -z "$mode" ] || [ -z "$mode2" ] ; then
    usage
fi


if [ $mode = "lex" ]; then
    script_file="../function/perturb/perturbations_lex.py"
    script_path="${current_dir}/${script_file}"
    echo "Lexicographic perturbation for: ${src_name} and ${trg_name}"
    bash "${script_path}" \
    -i "${input_path}" \
    -d "${data_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${data_quality}"
fi

if [ $mode = "mor" ]; then
    script_file="../function/perturb/perturbations_mor.py"
    script_path="${current_dir}/${script_file}"
    echo "Morphological perturbation for: ${src_name} and ${trg_name}"
    bash "${script_path}" \
    -i "${input_path}" \
    -d "${data_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${data_quality}"
fi

# if [ $mode = "syn" ]; then
#     script_file="../function/perturb/perturbations_syn.py"
#     script_path="${current_dir}/${script_file}"
#     echo "Syntactical perturbation for: ${src_name} and ${trg_name}"
#     bash "${script_path}" \
#     -i "${input_path}" \
#     -d "${data_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${data_quality}"
# fi
