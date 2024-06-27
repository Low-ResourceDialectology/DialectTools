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
perturbation_type="" # lex | mor | syn
data_quality="" # naive | clean | informed
feature_validity="" # guess | reason | authentic
data_file_extension="" # "en" (due to using data previously translated into English via NLLB)
current_dir="$(dirname "$0")"
script_file="../function/perturb/perturbations_lex.py"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -d data_path -o output_path -s src_lang -a src_name -t trg_lang -b trg_name -m perturbation_type -n data_quality -e data_file_extension -f feature_validity"
exit 1
}

# Parse command-line options
while getopts ":i:d:o:s:a:t:b:m:n:e:f:" opt; do
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
            perturbation_type=$OPTARG
            ;;
		n)
            data_quality=$OPTARG
            ;;
        e)
            data_file_extension=$OPTARG
            ;;
        f)
            feature_validity=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$data_path" ] || [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$src_name" ] || [ -z "$trg_lang" ] || [ -z "$trg_name" ]  || [ -z "$perturbation_type" ] || [ -z "$data_quality" ] || [ -z "$feature_validity" ] ; then
    usage
fi


if [ $perturbation_type = "lex" ]; then
    script_file="../function/perturb/perturbations_lex.py"
    script_path="${current_dir}/${script_file}"
    #echo "Lexicographic perturbation for: ${src_name} and ${trg_name}"
    python3 "${script_path}" \
    -i "${input_path}" \
    -d "${data_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${data_quality}" \
    -e "${data_file_extension}"
fi

if [ $perturbation_type = "mor" ]; then
    script_file="../function/perturb/perturbations_mor.py"
    script_path="${current_dir}/${script_file}"
    #echo "Morphological perturbation for: ${src_name} and ${trg_name}"
    python3 "${script_path}" \
    -i "${input_path}" \
    -d "${data_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${data_quality}" \
    -e "${data_file_extension}" \
    -f "${feature_validity}"
fi

if [ $perturbation_type = "all" ]; then
    script_file="../function/perturb/perturbations_all.py"
    script_path="${current_dir}/${script_file}"
    #echo "Lexicographical and Morphological perturbation for: ${src_name} and ${trg_name}"
    python3 "${script_path}" \
    -i "${input_path}" \
    -d "${data_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}" \
    -m "${data_quality}" \
    -n "${perturbation_type}" \
    -e "${data_file_extension}" \
    -f "${feature_validity}"
fi

# if [ $perturbation_type = "syn" ]; then
#     script_file="../function/perturb/perturbations_syn.py"
#     script_path="${current_dir}/${script_file}"
#     echo "Syntactical perturbation for: ${src_name} and ${trg_name}"
#     python3 "${script_path}" \
#     -i "${input_path}" \
#     -d "${data_path}" \
#     -o "${output_path}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${data_quality}" \
#     -n "${perturbation_type}" \
#     -e "${data_file_extension}"
# fi
