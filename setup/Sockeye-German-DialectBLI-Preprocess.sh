#!/bin/bash
# Preprovess parallel data for Sockeye via subword-nmt
# Use: cd ./setup
# bash Sockeye-German-DialectBLI-Preprocess.sh
#  /media/AllBlue/LanguageData/PREP/opustools bar en /media/AllBlue/LanguageData/PREP/subwordnmt

CURRENT="$PWD"

INPUTDIR="/media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001"
SOURCE="bar"
TARGET="deu"
OUTDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-barL-Sock-deuL-DBLI-0001/SubwordNMT"
mkdir "${OUTDIR}" -p
cd "${OUTDIR}"
source /media/AllBlue/LanguageData/TOOLS/vSockeye/bin/activate


# The data is already tokenized, so we only need to apply byte-pair encoding (Sennrich et al., 2016): → https://aclanthology.org/P16-1162/
cat "${INPUTDIR}"/train."${SOURCE}" "${INPUTDIR}"/train."${TARGET}" |subword-nmt learn-bpe -s 32000 >codes
for SET in train dev test; do
  subword-nmt apply-bpe -c codes <"${INPUTDIR}"/"${SET}"."${SOURCE}" >"${OUTDIR}"/"${SET}"."${SOURCE}".bpe
  subword-nmt apply-bpe -c codes <"${INPUTDIR}"/"${SET}"."${TARGET}" >"${OUTDIR}"/"${SET}"."${TARGET}".bpe
done

cd "$CURRENT"


