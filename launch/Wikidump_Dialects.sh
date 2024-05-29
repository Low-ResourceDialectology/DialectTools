#!/bin/bash

###############################################################################
# Handmade script with downloaded wikidumps

current_dir="$(dirname "$0")"
script_file="$current_dir/../clean/wikidumps2dialects.py"
INDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps

for CODE in als bar; do
    CURINDIR="${INDIR}/naive/${CODE}"
    INFILE="${CODE}"-info.json
    OUTDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps/info
    mkdir -p "${OUTDIR}"
    OUTFILE="${CODE}"-dialects.json

    python3 "${script_file}" --code "${CODE}" --input-dir "${CURINDIR}" --input-file "${INFILE}" --output-dir "${OUTDIR}" --output-file "${OUTFILE}"
done
