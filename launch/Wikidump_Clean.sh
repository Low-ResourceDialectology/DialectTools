#!/bin/bash

###############################################################################
# → Clean Wikidump splits that resulted from /launch/Wikidump_Splits.sh
source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

languages=()

current_dir="$(dirname "$0")"
script_file="$current_dir/../clean/wikidumps2clean.py"
INDIRECTORY=/media/AllBlue/LanguageData/CLEAN/wikidumps

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

LOGDIR=/media/AllBlue/LanguageData/LOGS/
mkdir -p "${LOGDIR}"
echo "Logs written into ${LOGDIR}"

for LANG in "${languages[@]}"; do
    INDIR="${INDIRECTORY}/splits/${LANG}"
    OUTDIR="${INDIRECTORY}/clean/${LANG}"
    echo "Writing clean data splits to: ${OUTDIR}"
    mkdir -p "${OUTDIR}"
    
    python3 "${script_file}" --code "${LANG}" \
    --input-dir "${INDIR}" --output-dir "${OUTDIR}" \
    --log-dir "${LOGDIR}"
done
