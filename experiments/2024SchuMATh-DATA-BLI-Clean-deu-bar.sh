#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Filter DialectBLI data for (groups of) sub-dialects based on cleaned wikidump data

# Initialize variables and default values
input_path="/media/AllBlue/LanguageData/DICT"
output_path="/media/AllBlue/LanguageData/DICT"


current_dir="$(dirname "$0")"
script_file="../function/clean/dialectBLI2subdialectBLI.sh"
script_path="${current_dir}/${script_file}"


# For Bavarian-German data
src_lang="bar"
src_name="Bavarian"
trg_lang="deu"
trg_name="German"
echo "Filtering: BLI data for ${src_name}-${trg_name}"


bash "${script_path}" \
    -i "${input_path}" \
    -o "${output_path}" \
    -s "${src_lang}" \
    -a "${src_name}" \
    -t "${trg_lang}" \
    -b "${trg_name}"


# For Alemannic-German data

