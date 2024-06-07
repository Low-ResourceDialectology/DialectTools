#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Evaluate machine translation via SacreBLEU

# SacreBLEU → https://github.com/mjpost/sacreBLEU

# Initialize variables and default values
input_path_ref=""
input_file_ref=""
input_path_inf=""
input_file_inf=""

output_path=""
output_file=""

experiment=""
metrics="bleu chrf ter"
precision="4"
options=""
# Function to print usage
usage() {
echo "Usage: $0 -a input_path_ref -b input_file_ref -c input_path_inf -d input_file_inf -e output_path -f output_file -g experiment -h metrics -i precision -j options"
exit 1
}

# Parse command-line options
while getopts ":a:b:c:d:e:f:g:h:i:j:" opt; do
    case $opt in
        a)  input_path_ref=$OPTARG;;
        b)  input_file_ref=$OPTARG;;
        c)  input_path_inf=$OPTARG;;
        d)  input_file_inf=$OPTARG;;
        e)  output_path=$OPTARG;;
        f)  output_file=$OPTARG;;
        g)  experiment=$OPTARG;;
        h)  metrics=$OPTARG;;
        i)  precision=$OPTARG;;
        j)  options=$OPTARG;;
        *)  usage;;
    esac
done
# The `for` loop iterates over the positional parameters from `OPTIND - 1` to the end (`$#`).
# The loop breaks if it encounters another flag (`-`).

# Check if all required arguments are provided
if [ -z "$input_path_ref" ] || \
    [ -z "$input_file_ref" ] || \
    [ -z "$input_path_inf" ] || \
    [ -z "$input_file_inf" ] || \
    [ -z "$output_path" ] || \
    [ -z "$output_file" ] || \
    [ -z "$experiment" ] || \
    [ -z "$metrics" ] || \
    [ -z "$precision" ]; then
    usage
fi

# Create output directory and copy input file over prior to translation process
mkdir -p "${output_path}"

source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate

# Convert the metrics string into an array
IFS=' ' read -r -a metrics_array <<< "$metrics"

sacrebleu "${input_path_ref}/${input_file_ref}" \
    -i "${input_path_inf}/${input_file_inf}" \
    -m "${metrics_array[@]}" \
    -w "${precision}" \
    > "${output_path}/${output_file}"
# TODO: Include optionally provided options to the sacreBLEU script → #"${options}" 