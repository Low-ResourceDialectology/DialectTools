#!/bin/bash

###############################################################################
# → Split Wikidump into dialect subsets that were extracted via /launch/Wikidump_Dialects.sh
languages=()

current_dir="$(dirname "$0")"
script_file="$current_dir/../clean/wikidumps2splits.py"
INDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps

# Parse command-line options
while getopts ":l:" opt; do
    case $opt in
        l)
            # Capture all remaining arguments as languages
            for (( i = OPTIND - 1; i <= $#; i++ )); do
                if [[ ${!i} != -* ]]; then
                    languages+=("${!i}")
                else
                    break
                fi
            done
            ;;
    esac
done

echo "Currently work with hard-coded date as part of filenames."

for LANG in "${languages[@]}"; do
    INDIR01="${INDIR}/info/${LANG}"
    INFILE01="${LANG}"-dialects.json
    INFILEFREQ="${LANG}"-dialects.json-freq
    INDIR02="${INDIR}/wikiextractor/${LANG}"/text/AA
    #INFILE02=wiki_00 and wiki_01 and wiki_02 and . . . → Sorted out in Python script
    
    OUTDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps/splits/"${LANG}"
    FREQDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps/splits
    mkdir -p "${OUTDIR}"
    OUTFILE="${LANG}".json # Holds the frequencies, while the splits get new names inside the script

    python3 "${script_file}" --code "${LANG}" \
    --input-dir01 "${INDIR01}" --input-file "${INFILE01}" \
    --input-dir02 "${INDIR02}" --input-file-freq "${INFILEFREQ}" \
    --output-dir "${OUTDIR}" --output-file "${OUTFILE}" \
    --sort-level 1 --freq-dir "${FREQDIR}"
done
