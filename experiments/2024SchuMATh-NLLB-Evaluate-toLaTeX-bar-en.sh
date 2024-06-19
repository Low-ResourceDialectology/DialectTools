#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Aggregate the results of various evaluation metrics and transform to LaTeX content

current_dir="$(dirname "$0")"

# Aggregation of the metrics from various files
script_file="$current_dir/../function/evaluate/metrics2aggregate.py"

input_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10"
output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/evals"

# Current date
printf -v date '%(%Y%m%d)T' -1 

output_filename="English-Bavarian-${date}"

python3 "${script_file}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -f "${output_filename}"


# Transformation into LaTeX-Table code
script_file="$current_dir/../function/evaluate/metrics2LaTeX.py"
latex_filename="English-Bavarian-${date}-LaTeX"
input_file="${output_path}/${output_filename}.json"
output_file="${output_path}/${latex_filename}"

python3 "${script_file}" \
    -i "${input_file}" \
    -o "${output_file}"

