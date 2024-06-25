#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Extract replacement rules from linguistic features (morphological)

# Initialize variables and default values
input_path="" # "/media/AllBlue/LanguageData/FEATURES"
output_path="" # "/media/AllBlue/LanguageData/PERTURBS"
src_lang="" # "als"
src_name="" # "Alemannic"
trg_lang="" # "deu"
trg_name="" # "German"
dict_direction="" # "RightToLeft" | "LeftToRight"
feature_validity="" # guess | reason | authentic
current_dir="$(dirname "$0")"
script_file="pert_mor.py"

# Function to print usage
usage() {
echo "Usage: $0 -i input_path -o output_path -s src_lang -a srg_name -b trg_name -t trg_lang -c script_file -m dict_direction -f feature_validity"
exit 1
}

# Parse command-line options
while getopts ":i:o:s:a:t:b:c:m:f:" opt; do
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
        m)
	        dict_direction=$OPTARG
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
if [ -z "$input_path" ] || [ -z "$output_path" ] || [ -z "$src_lang" ] || [ -z "$src_name" ] || [ -z "$trg_lang" ] || [ -z "$trg_name" ] || [ -z "$script_file" ] || [ -z "$dict_direction" ] || [ -z "$feature_validity" ]; then
    usage
fi

script_path="${current_dir}/${script_file}"

#echo "Morphological features for ${src_name} and ${trg_name}"
python3 "${script_path}" \
    --input_dir "${input_path}" \
    --output_dir "${output_path}" \
    --src_lang "${src_lang}" \
    --src_name "${src_name}" \
    --trg_lang "${trg_lang}" \
    --trg_name "${trg_name}" \
    --dict_direction "${dict_direction}" \
    --feature_validity "${feature_validity}"