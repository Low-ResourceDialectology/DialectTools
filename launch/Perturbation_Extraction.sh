#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Extract linguistic features (lexicograpic | morphological | syntactical) from bidictionaries

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/FEATURES"
output_path="/media/AllBlue/LanguageData/PERTURBS"
src_lang="" # "als"
src_name="" # "Alemannic"
trg_lang="" # "deu"
trg_name="" # "German"
perturbation_type="" # lex | mor | syn
feature_validity="" # guess | reason | authentic
dict_direction="" # "RightToLeft" | "LeftToRight"
extraction_method="" # direct | ?? something heuristic based ??
unit_frequency="" # 5
unit_length="" # 5
current_dir="$(dirname "$0")"
script_file="../function/extract/perturbations_lex.sh"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -o output_path -s src_lang -a src_name -b trg_name -t trg_lang -m perturbation_type -n dict_direction -f feature_validity -e extraction_method -u unit_frequency -l unit_length"
exit 1
}

# Parse command-line options
while getopts ":i:o:s:a:b:t:m:n:f:e:u:l:" opt; do
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
        n)
            dict_direction=$OPTARG
            ;;
        f)
            feature_validity=$OPTARG
            ;;
        e)
            extraction_method=$OPTARG
            ;;
        u)
            unit_frequency=$OPTARG
            ;;
        l)
            unit_length=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$input_path" ] || [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$src_name" ] || [ -z "$trg_lang" ] || [ -z "$trg_name" ] || [ -z "$perturbation_type" ] || [ -z "$dict_direction" ] || [ -z "$feature_validity" ] || [ -z "$extraction_method" ] || [ -z "$unit_frequency" ] || [ -z "$unit_length" ] ; then
    usage
fi

if [ $dict_direction = "LeftToRight" ]; then
    if [ $perturbation_type = "lex" ]; then
        script_file="../function/extract/perturbations_lex.sh"
        script_path="${current_dir}/${script_file}"
        echo "Lexicographic replacements for: ${src_name} and ${trg_name}"
        bash "${script_path}" \
        -i "${input_path}/${src_name}/${extraction_method}" \
        -o "${output_path}/${src_name}/${trg_name}/${feature_validity}" \
        -s "${src_lang}" \
        -a "${src_name}" \
        -t "${trg_lang}" \
        -b "${trg_name}" \
        -m "${dict_direction}" \
        -f "${feature_validity}" \
        -e "${extraction_method}"
    fi
    if [ $perturbation_type = "mor" ]; then
        script_file="../function/extract/perturbations_mor.sh"
        script_path="${current_dir}/${script_file}"
        echo "Morphological replacements for: ${src_name} and ${trg_name}"
        bash "${script_path}" \
        -i "${input_path}/${src_name}/${extraction_method}/frequencies" \
        -o "${output_path}/${src_name}/${trg_name}/${feature_validity}" \
        -s "${src_lang}" \
        -a "${src_name}" \
        -t "${trg_lang}" \
        -b "${trg_name}" \
        -m "${dict_direction}" \
        -f "${feature_validity}" \
        -e "${extraction_method}" \
        -n "${unit_frequency}" \
        -l "${unit_length}"
    fi
fi

if [ $dict_direction = "RightToLeft" ]; then
    if [ $perturbation_type = "lex" ]; then
        script_file="../function/extract/perturbations_lex.sh"
        script_path="${current_dir}/${script_file}"
        echo "Lexicographic replacements for: ${src_name} and ${trg_name}"
        bash "${script_path}" \
        -i "${input_path}/${trg_name}/${extraction_method}" \
        -o "${output_path}/${src_name}/${trg_name}/${feature_validity}" \
        -s "${src_lang}" \
        -a "${src_name}" \
        -t "${trg_lang}" \
        -b "${trg_name}" \
        -m "${dict_direction}" \
        -f "${feature_validity}" \
        -e "${extraction_method}"
        fi
    if [ $perturbation_type = "mor" ]; then
        script_file="../function/extract/perturbations_mor.sh"
        script_path="${current_dir}/${script_file}"
        echo "Morphological replacements for: ${src_name} and ${trg_name}"
        bash "${script_path}" \
        -i "${input_path}/${trg_name}/${extraction_method}/frequencies" \
        -o "${output_path}/${src_name}/${trg_name}/${feature_validity}" \
        -s "${src_lang}" \
        -a "${src_name}" \
        -t "${trg_lang}" \
        -b "${trg_name}" \
        -m "${dict_direction}" \
        -f "${feature_validity}" \
        -e "${extraction_method}" \
        -n "${unit_frequency}" \
        -l "${unit_length}"
    fi
fi

# if [ $perturbation_type = "syn" ]; then
#     script_file="../function/extract/perturbations_syn.sh"
#     script_path="${current_dir}/${script_file}"
#     echo "Syntactical replacements for: ${src_name} and ${trg_name}"
#     bash "${script_path}" \
#     -i "${input_path}/${src_name}/${extraction_method}" \
#     -o "${output_path}/${src_name}/${trg_name}/${feature_validity}" \
#     -s "${src_lang}" \
#     -a "${src_name}" \
#     -t "${trg_lang}" \
#     -b "${trg_name}" \
#     -m "${dict_direction}" \
#     -f "${feature_validity}" \
#     -e "${extraction_method}"
# fi
