#!/bin/bash
# Preprovess parallel data for Sockeye via subword-nmt
# Use: cd ./setup
#         bash Subwordnmt-Test-bar-eng.sh /media/AllBlue/LanguageData/PREP/opustools bar en /media/AllBlue/LanguageData/PREP/subwordnmt

CURRENT="$PWD"

# First input argument
INPUTDIR="$1"
SOURCE="$2"
TARGET="$3"
DATADIR="${INPUTDIR}/${SOURCE}-${TARGET}"
mkdir "${DATADIR}" -p
cd "${DATADIR}"
source /media/AllBlue/LanguageData/TOOLS/vSockeye/bin/activate

# Second input argument
OUTDIR="$4"

cat train."${SOURCE}" train."${TARGET}" |subword-nmt learn-bpe -s 32000 >codes
for SET in train dev test; do
  subword-nmt apply-bpe -c codes <${SET}."${SOURCE}" >${SET}."${SOURCE}".bpe
  subword-nmt apply-bpe -c codes <${SET}."${TARGET}" >${SET}."${TARGET}".bpe
done

cd "$CURRENT"


