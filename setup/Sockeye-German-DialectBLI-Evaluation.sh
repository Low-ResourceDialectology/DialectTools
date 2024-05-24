#!/bin/bash
# Preprovess parallel data for Sockeye via subword-nmt
# Use: cd ./setup
# bash Sockeye-Evaluation-Test-bar-eng.sh /media/AllBlue/LanguageData/PREP/subwordnmt bar en /media/AllBlue/LanguageData/PREP/opustools

CURRENT="$PWD"

INPUTDIR="/media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001"
PREPDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-barL-Sock-deuL-DBLI-0001/Sockeye-prepared"
SUBWORDDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-barL-Sock-deuL-DBLI-0001/SubwordNMT"
SOURCE="bar"
TARGET="deu"
OUTDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-barL-Sock-deuL-DBLI-0001/Sockeye-training"
EVALDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-barL-Sock-deuL-DBLI-0001/Sockeye-evaluation"
mkdir "${EVALDIR}" -p
cd "${EVALDIR}"
source /media/AllBlue/LanguageData/TOOLS/vSockeye/bin/activate

# When training is complete, we translate the preprocessed test set:
###############################################################################
# One direction
sockeye-translate \
    --input "${SUBWORDDIR}"/test."${SOURCE}".bpe \
    --output "${EVALDIR}"/out-"${SOURCE}".bpe \
    --model "${OUTDIR}" \
    --dtype float16 \
    --beam-size 5 \
    --batch-size 64

# Other direction
sockeye-translate \
    --input "${SUBWORDDIR}"/test."${TARGET}".bpe \
    --output "${EVALDIR}"/out-"${TARGET}".bpe \
    --model "${OUTDIR}" \
    --dtype float16 \
    --beam-size 5 \
    --batch-size 64


# Switch to other venv
deactivate
source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate


# We then reverse BPE and score the translations against the reference using sacreBLEU:
###############################################################################

sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${SOURCE}".bpe >"${EVALDIR}"/out-"${SOURCE}".tok
sacrebleu "${INPUTDIR}"/test."${TARGET}" -tok none -i "${EVALDIR}"/out-"${SOURCE}".tok

sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${TARGET}".bpe >"${EVALDIR}"/out-"${TARGET}".tok
sacrebleu "${INPUTDIR}"/test."${SOURCE}" -tok none -i "${EVALDIR}"/out-"${TARGET}".tok

cd "$CURRENT"


