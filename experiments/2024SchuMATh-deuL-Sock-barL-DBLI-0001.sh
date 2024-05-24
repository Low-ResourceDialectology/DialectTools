#!/bin/bash
# Preprovess parallel data for Sockeye via subword-nmt
# Use: cd ./setup
# bash Sockeye-German-DialectBLI-Preprocess.sh
#  /media/AllBlue/LanguageData/PREP/opustools bar en /media/AllBlue/LanguageData/PREP/subwordnmt

CURRENT="$PWD"

source /media/AllBlue/LanguageData/TOOLS/vSockeye/bin/activate

INPUTDIR="/media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001"
SOURCE="deu"
TARGET="bar"

SUBWORDDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-Sock-${TARGET}L-DBLI-0001/SubwordNMT"
mkdir "${SUBWORDDIR}" -p

PREPDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-Sock-${TARGET}L-DBLI-0001/Sockeye-prepared"
mkdir "${PREPDIR}" -p

TRAINDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-Sock-${TARGET}L-DBLI-0001/Sockeye-training"
mkdir "${TRAINDIR}" -p

EVALDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-Sock-${TARGET}L-DBLI-0001/Sockeye-evaluation"
mkdir "${EVALDIR}" -p

# # At this point the data should already tokenized, so we only need to apply byte-pair encoding (Sennrich et al., 2016): → https://aclanthology.org/P16-1162/
# cat "${INPUTDIR}"/train."${SOURCE}" "${INPUTDIR}"/train."${TARGET}" |subword-nmt learn-bpe -s 32000 >codes
# for SET in train dev test; do
#   subword-nmt apply-bpe -c codes <"${INPUTDIR}"/"${SET}"."${SOURCE}" >"${SUBWORDDIR}"/"${SET}"."${SOURCE}".bpe
#   subword-nmt apply-bpe -c codes <"${INPUTDIR}"/"${SET}"."${TARGET}" >"${SUBWORDDIR}"/"${SET}"."${TARGET}".bpe
# done

# We first split the byte-pair encoded training data into shards and serialize it in PyTorch's tensor format. 
# This allows us to train on data of any size by loading and unloading different pieces throughout training:
# sockeye-prepare-data \
#     --source "${SUBWORDDIR}"/train."${SOURCE}".bpe --target "${SUBWORDDIR}"/train."${TARGET}".bpe --shared-vocab \
#     --word-min-count 2 --pad-vocab-to-multiple-of 8 --max-seq-len 95 \
#     --num-samples-per-shard 10000000 --output "${PREPDIR}" --max-processes $(nproc)

# The following command trains a big transformer (Vaswani et al., 2017) → https://arxiv.org/abs/1706.03762
# using the large batch recipe described by Ott et al. (2018) → https://arxiv.org/abs/1806.00187
# We then launch training on 1 GPU. 
sockeye-train \
    --prepared-data "${PREPDIR}" --validation-source "${SUBWORDDIR}"/dev."${SOURCE}".bpe \
    --validation-target "${SUBWORDDIR}"/dev."${TARGET}".bpe --output "${TRAINDIR}" --num-layers 6 \
    --transformer-model-size 1024 --transformer-attention-heads 16 \
    --transformer-feed-forward-num-hidden 4096 --amp --batch-type max-word \
    --batch-size 5000 --update-interval 80 --checkpoint-interval 500 \
    --max-updates 15000 --optimizer-betas 0.9:0.98 \
    --initial-learning-rate 0.06325 \
    --learning-rate-scheduler-type inv-sqrt-decay --learning-rate-warmup 4000 \
    --seed 1

# Training on larger data typically requires more updates for the model to reach a perplexity plateau. 
# When using the above recipe with larger data sets, increase the number of updates (--max-updates) 
# or train until the model does not improve over many checkpoints 
# (specify --max-num-checkpoint-not-improved X instead of --max-updates Y).


# # When training is complete, we translate the preprocessed test set:
# ###############################################################################
# # One direction
# sockeye-translate \
#     --input "${SUBWORDDIR}"/test."${SOURCE}".bpe \
#     --output "${EVALDIR}"/out-"${SOURCE}".bpe \
#     --model "${TRAINDIR}" \
#     --dtype float16 \
#     --beam-size 5 \
#     --batch-size 64

# # Other direction
# sockeye-translate \
#     --input "${SUBWORDDIR}"/test."${TARGET}".bpe \
#     --output "${EVALDIR}"/out-"${TARGET}".bpe \
#     --model "${TRAINDIR}" \
#     --dtype float16 \
#     --beam-size 5 \
#     --batch-size 64

# # Switch to other venv
# deactivate
# source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate

# # We then reverse BPE and score the translations against the reference using sacreBLEU:
# ###############################################################################
# sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${SOURCE}".bpe >"${EVALDIR}"/out-"${SOURCE}".tok
# sacrebleu "${INPUTDIR}"/test."${TARGET}" -tok none -i "${EVALDIR}"/out-"${SOURCE}".tok

# sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${TARGET}".bpe >"${EVALDIR}"/out-"${TARGET}".tok
# sacrebleu "${INPUTDIR}"/test."${SOURCE}" -tok none -i "${EVALDIR}"/out-"${TARGET}".tok

# echo "################"
# echo "Script to Script"
# echo "################"
# echo "TODO"

# SacreBLEU → https://github.com/mjpost/sacreBLEU
#bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/SacreBLEU.sh "/media/AllBlue/LanguageData/CLEAN/English/2022NLLBNLLB_devtest.engL" "${OUTDIR}"




cd "$CURRENT"
