#!/bin/bash

###############################################################################
# → Once the structure is known, the dialect-info can directly be filtered out
# Handmade script with downloaded wikidumps - similar to the previous wikidumps2extract.py 
#   script as part of the wikidumps "cleaning" 


current_dir="$(dirname "$0")"
script_file="$current_dir/../clean/wikidumps2dialects.py"
INDIR=/media/AllBlue/LanguageData/DOWNLOAD/wikidumps

echo "Currently work with hard-coded date as part of filenames."

for CODE in als bar; do
    CURINDIR="${INDIR}/${CODE}"
    INFILE="${CODE}"wiki-20240520-pages-meta-current.xml.bz2
    OUTDIR=/media/AllBlue/LanguageData/CLEAN/wikidumps/info/"${CODE}"
    mkdir -p "${OUTDIR}"
    OUTFILE="${CODE}"-dialects.json

    python3 "${script_file}" --code "${CODE}" \
    --input-dir "${CURINDIR}" --input-file "${INFILE}" \
    --output-dir "${OUTDIR}" --output-file "${OUTFILE}"
done
