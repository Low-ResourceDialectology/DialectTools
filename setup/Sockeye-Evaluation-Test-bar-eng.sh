#!/bin/bash
# Preprovess parallel data for Sockeye via subword-nmt
# Use: cd ./setup
# bash Sockeye-Evaluation-Test-bar-eng.sh /media/AllBlue/LanguageData/PREP/subwordnmt bar en /media/AllBlue/LanguageData/PREP/opustools

CURRENT="$PWD"

# First input argument
INPUTDIR="$1"
SOURCE="$2"
TARGET="$3"
DATADIR="${INPUTDIR}/${SOURCE}-${TARGET}"
INDIR="$4/${SOURCE}-${TARGET}"

source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate

# When training is complete, we translate the preprocessed test set:
###############################################################################
# One direction
# sockeye-translate \
#     --input "${DATADIR}"/test."${SOURCE}".bpe \
#     --output "${DATADIR}"/out-"${SOURCE}"-"${TARGET}".bpe \
#     --model "${DATADIR}"/model \
#     --dtype float16 \
#     --beam-size 5 \
#     --batch-size 64

# Other direction
# sockeye-translate \
#     --input "${DATADIR}"/test."${TARGET}".bpe \
#     --output "${DATADIR}"/out-"${TARGET}"-"${SOURCE}".bpe \
#     --model "${DATADIR}"/model \
#     --dtype float16 \
#     --beam-size 5 \
#     --batch-size 64


# We then reverse BPE and score the translations against the reference using sacreBLEU:
###############################################################################
sed -re 's/(@@ |@@$)//g' <"${DATADIR}"/out-"${SOURCE}"-"${TARGET}".bpe >"${DATADIR}"/out-"${SOURCE}"-"${TARGET}".tok
sacrebleu "${INDIR}"/test."${TARGET}" -tok none -i "${DATADIR}"/out-"${SOURCE}"-"${TARGET}".tok

sed -re 's/(@@ |@@$)//g' <"${DATADIR}"/out-"${TARGET}"-"${SOURCE}".bpe >"${DATADIR}"/out-"${TARGET}"-"${SOURCE}".tok
sacrebleu "${INDIR}"/test."${SOURCE}" -tok none -i "${DATADIR}"/out-"${TARGET}"-"${SOURCE}".tok

cd "$CURRENT"


