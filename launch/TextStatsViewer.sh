#!/bin/bash
###############################################################################
# → Plotting the countet text content of files to get an overview of the data
source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

current_dir="$(dirname "$0")"
script_file="$current_dir/../stats/stats_viewer.py"
INPUT=/media/AllBlue/LanguageData/LOGS/wikidumps-cleaned
LOGDIR=/media/AllBlue/LanguageData/LOGS/wikidumps-cleaned-plots/
mkdir -p "${LOGDIR}"

for CODE in als bar; do
    INDIR="${INPUT}"
    OUTFILE="${CODE}"
    python3 "${script_file}" --input-dir "${INDIR}" \
    --log-dir "${LOGDIR}" --output-file "${OUTFILE}" \
    --mode all --language "${CODE}"
done