#!/bin/bash

###############################################################################
# → Split Wikidump into dialect subsets that were extracted via /launch/Wikidumo_Dialects.sh


current_dir="$(dirname "$0")"
script_file="$current_dir/../clean/wikidumps2splits.py"
INDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps

echo "Currently work with hard-coded date as part of filenames."

for CODE in als bar; do
    INDIR01="${INDIR}/info/${CODE}"
    INFILE01="${CODE}"-dialects.json
    INFILEFREQ="${CODE}"-dialects.json-freq
    INDIR02="${INDIR}/wikiextractor/${CODE}"/text/AA
    #INFILE02=wiki_00 and wiki_01 and wiki_02 and . . . → Sorted out in Python script
    
    OUTDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps/splits/"${CODE}"
    FREQDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps/splits"
    mkdir -p "${OUTDIR}"
    OUTFILE="${CODE}".json # Holds the frequencies, while the splits get new names inside the script

    python3 "${script_file}" --code "${CODE}" \
    --input-dir01 "${INDIR01}" --input-file "${INFILE01}" \
    --input-dir02 "${INDIR02}" --input-file-freq "${INFILEFREQ}" \
    --output-dir "${OUTDIR}" --output-file "${OUTFILE}" \
    --sort-level 1 --freq-dir "${FREQDIR}"
done
