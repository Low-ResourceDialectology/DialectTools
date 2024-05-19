#!/bin/bash
# Preprovess parallel data for Sockeye via subword-nmt
# Use: cd ./setup
# bash Sockeye-TrainingSplit-Test-bar-eng.sh /media/AllBlue/LanguageData/PREP/opustools bar en /media/AllBlue/LanguageData/PREP/subwordnmt

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

# We first split the byte-pair encoded training data into shards and serialize it in PyTorch's tensor format. 
# This allows us to train on data of any size by loading and unloading different pieces throughout training:
sockeye-prepare-data \
    --source "${OUTDIR}"/train."${SOURCE}".bpe --target "${OUTDIR}"/train."${TARGET}".bpe --shared-vocab \
    --word-min-count 2 --pad-vocab-to-multiple-of 8 --max-seq-len 95 \
    --num-samples-per-shard 10000000 --output prepared --max-processes $(nproc)


cd "$CURRENT"


