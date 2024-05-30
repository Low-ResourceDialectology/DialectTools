#!/bin/bash

###############################################################################
# → Split Wikidump into dialect subsets that were extracted via /launch/Wikidumo_Dialects.sh
source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

current_dir="$(dirname "$0")"
script_file="$current_dir/../clean/wikidumps2clean.py"
INDIRECTORY=/media/AllBlue/LanguageData/CLEAN/wikidumps
LOGDIR=/media/AllBlue/LanguageData/LOGS/
mkdir -p "${LOGDIR}"

for CODE in als; do #bar; do # als bar; do
    INDIR="${INDIRECTORY}/splits/${CODE}"
    OUTDIR="${INDIRECTORY}/clean/${CODE}"
    echo "${OUTDIR}"
    mkdir -p "${OUTDIR}"
    
    python3 "${script_file}" --code "${CODE}" \
    --input-dir "${INDIR}" --output-dir "${OUTDIR}" \
    --log-dir "${LOGDIR}"
done
