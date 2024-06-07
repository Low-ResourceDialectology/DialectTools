#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Translate text via NLLB

# NLLB → https://github.com/facebookresearch/fairseq/tree/nllb
# ? Open-NLLB → https://github.com/gordicaleksa/Open-NLLB

# Initialize variables and default values
input_path=""
input_file="" # test
src_lang="" # de
input_code="" # deu_Latn
output_path="/media/AllBlue/LanguageData/EXPERIMENT"
output_file="" # test
trg_lang="" # en
putput_code="" # eng_Latn
experiment="" # 2024SchuMATh-NLLB-Baseline-deu
author_id="facebook"
model_id="nllb-200-3.3B"
model_name="3.3B" # 3.3B || 1.3B || distilled-1.3B || 600M
chunk_size="100"
current_dir="$(dirname "$0")"
script_file="$current_dir/../../launch/NLLB.py"

# Function to print usage
usage() {
echo "Usage: $0 -a input_path -b input_file -c src_lang -d input_code -e output_path -f output_file -g trg_lang -h output_code -i experiment -j author_id -k model_id -l model_name -m chunk_size"
exit 1
}

# Parse command-line options
while getopts ":a:b:c:d:e:f:g:h:i:j:k:l:m:" opt; do
    case $opt in
        a)  input_path=$OPTARG;;
        b)  input_file=$OPTARG;;
        c)  src_lang=$OPTARG;;
        d)  input_code=$OPTARG;;
        e)  output_path=$OPTARG;;
        f)  output_file=$OPTARG;;
        g)  trg_lang=$OPTARG;;
        h)  output_code=$OPTARG;;
        i)  experiment=$OPTARG;;
        j)  author_id=$OPTARG;;
        k)  model_id=$OPTARG;;
        l)  model_name=$OPTARG;;
        m)  chunk_size=$OPTARG;;
        *)  usage;;
    esac
done
# The `for` loop iterates over the positional parameters from `OPTIND - 1` to the end (`$#`).
# The loop breaks if it encounters another flag (`-`).

# Check if all required arguments are provided
if [ -z "$input_path" ] || \
    [ -z "$input_file" ] || \
    [ -z "$src_lang" ] || \
    [ -z "$input_code" ] || \
    [ -z "$output_path" ] || \
    [ -z "$output_file" ] || \
    [ -z "$trg_lang" ] || \
    [ -z "$output_code" ] || \
    [ -z "$experiment" ] || \
    [ -z "$chunk_size" ]; then
    usage
fi

# Create output directory and copy input file over prior to translation process
mkdir -p "${output_path}"
#mkdir -p "${out_path}/${experiment}"
#cp "${INDIR}/${INFILENAME}.${INFILEEXTENSION}" "${OUTDIR}/${INFILENAME}.${INFILEEXTENSION}" # NOTE: Too much clutter

source /media/AllBlue/LanguageData/TOOLS/vNLLB/bin/activate

python3 "${script_file}" \
    --input_code "${input_code}" \
    --input_file "${input_path}/${input_file}.${src_lang}" \
    --output_code "${output_code}" \
    --output_file "${output_path}/${output_file}.${trg_lang}" \
    --authorid "${author_id}" \
    --modelid "${model_id}" \
    --chunk_size "${chunk_size}"
