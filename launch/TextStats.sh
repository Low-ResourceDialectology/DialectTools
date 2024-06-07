#!/bin/bash
###############################################################################
# → Counting text content of files to get an overview of the data

current_dir="$(dirname "$0")"
script_file="$current_dir/../stats/text_counter.py"

INPUT=/media/AllBlue/LanguageData/CLEAN/wikidumps/clean
LOGDIR=/media/AllBlue/LanguageData/LOGS/wikidumps-cleaned/

mkdir -p "${LOGDIR}"

for CODE in als bar; do
    INDIR="${INPUT}/${CODE}"
    OUTFILE="${CODE}"
    python3 "${script_file}" --input-dir "${INDIR}" \
    --log-dir "${LOGDIR}" --output-file "${OUTFILE}" \
    --mode all
done