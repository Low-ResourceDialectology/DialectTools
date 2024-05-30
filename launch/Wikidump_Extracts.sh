#!/bin/bash

###############################################################################
# → Extract wikidumps with less cleaning and keeping the parts for dialect identification
# Handmade script with downloaded wikidumps

current_dir="$(dirname "$0")"
#script_file="$current_dir/../clean/wikidumps-extract-handmade.py"
# NOTE: Renamed and changed scripts without any commits in between :/
script_file="$current_dir/../clean/wikidumps2extract.py" # This should be the name!
INDIR=/media/AllBlue/LanguageData/DOWNLOAD/wikidumps

echo "Currently work with hard-coded date as part of filenames."

for CODE in als bar; do
    CURINDIR="${INDIR}/${CODE}"
    INFILE="${CODE}"wiki-20240520-pages-meta-current.xml.bz2
    OUTDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps/naive/"${CODE}"
    mkdir -p "${OUTDIR}"

    python3 "${script_file}" --code "${CODE}" \
    --input-dir "${CURINDIR}" --input-file "${INFILE}" \
    --output-dir "${OUTDIR}"
done

# ###############################################################################
# → Extract the text content of the wikidumps
# # Wikiextractor → https://github.com/attardi/wikiextractor
# source /media/AllBlue/LanguageData/TOOLS/vWikiextractor/bin/activate
# current_dir="$(dirname "$0")"

# INDIR=/media/AllBlue/LanguageData/DOWNLOAD/wikidumps
# OUTDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps/wikiextractor

# for CODE in als bar; do
#     CURINDIR="${INDIR}/${CODE}"
#     INFILE="${CODE}"wiki-20240520-pages-meta-current.xml.bz2
#     CUROUTDIR="${OUTDIR}"/"${CODE}"
#     mkdir -p "${CUROUTDIR}"

#     cd "${CUROUTDIR}"
#     python3 -m wikiextractor.WikiExtractor "${CURINDIR}/${INFILE}" --json
# done