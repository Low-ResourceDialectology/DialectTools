#!/bin/bash
# Preprovess parallel data for Sockeye via subword-nmt
# Use: cd ./setup
# bash Sockeye-Preprocess-Test-bar-eng.sh /media/AllBlue/LanguageData/PREP/opustools bar en /media/AllBlue/LanguageData/PREP/subwordnmt

CURRENT="$PWD"

# First input argument
INPUTDIR="$1"
SOURCE="$2"
TARGET="$3"
DATADIR="${INPUTDIR}/${SOURCE}-${TARGET}"

OUTDIR="$4/${SOURCE}-${TARGET}"
mkdir "${OUTDIR}" -p
cd "${OUTDIR}"
source /media/AllBlue/LanguageData/TOOLS/vSockeye/bin/activate


# The data is already tokenized, so we only need to apply byte-pair encoding (Sennrich et al., 2016): → https://aclanthology.org/P16-1162/
cat "${DATADIR}"/train."${SOURCE}" "${DATADIR}"/train."${TARGET}" |subword-nmt learn-bpe -s 32000 >codes
for SET in train dev test; do
  subword-nmt apply-bpe -c codes <"${DATADIR}"/"${SET}"."${SOURCE}" >"${OUTDIR}"/"${SET}"."${SOURCE}".bpe
  subword-nmt apply-bpe -c codes <"${DATADIR}"/"${SET}"."${TARGET}" >"${OUTDIR}"/"${SET}"."${TARGET}".bpe
done

cd "$CURRENT"


