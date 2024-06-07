#!/bin/bash
###############################################################################
# → Get a word frequency dictionary for each file of an input directory

current_dir="$(dirname "$0")"
script_file="$current_dir/../extract/word_freq_dicts.py"
INPUT=/media/AllBlue/LanguageData/CLEAN/wikidumps/clean
OUTDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps/clean-freqdicts
mkdir -p "${OUTDIR}"

for CODE in als bar; do
    INDIR="${INPUT}/${CODE}"
    python3 "${script_file}" \
    --input-dir "${INDIR}" \
    --output-dir "${OUTDIR}/${CODE}"
done