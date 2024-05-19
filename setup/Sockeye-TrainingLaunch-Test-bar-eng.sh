#!/bin/bash
# Preprovess parallel data for Sockeye via subword-nmt
# Use: cd ./setup
# bash Sockeye-TrainingLaunch-Test-bar-eng.sh /media/AllBlue/LanguageData/PREP/opustools bar en /media/AllBlue/LanguageData/PREP/subwordnmt
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

# The following command trains a big transformer (Vaswani et al., 2017) → https://arxiv.org/abs/1706.03762
# using the large batch recipe described by Ott et al. (2018) → https://arxiv.org/abs/1806.00187

# We then launch training on 1 GPU. 
sockeye-train \
    --prepared-data prepared --validation-source "${OUTDIR}"/dev."${SOURCE}".bpe \
    --validation-target "${OUTDIR}"/dev."${TARGET}".bpe --output model --num-layers 6 \
    --transformer-model-size 1024 --transformer-attention-heads 16 \
    --transformer-feed-forward-num-hidden 4096 --amp --batch-type max-word \
    --batch-size 5000 --update-interval 80 --checkpoint-interval 500 \
    --max-updates 15000 --optimizer-betas 0.9:0.98 \
    --initial-learning-rate 0.06325 \
    --learning-rate-scheduler-type inv-sqrt-decay --learning-rate-warmup 4000 \
    --seed 1

# Alternate command for 8 GPUs: 
# torchrun --no_python --nproc_per_node 8 sockeye-train \
#     --prepared-data prepared --validation-source "${OUTDIR}"/dev."${SOURCE}".bpe \
#     --validation-target "${OUTDIR}"/dev."${TARGET}".bpe --output model --num-layers 6 \
#     --transformer-model-size 1024 --transformer-attention-heads 16 \
#     --transformer-feed-forward-num-hidden 4096 --amp --batch-type max-word \
#     --batch-size 5000 --update-interval 10 --checkpoint-interval 500 \
#     --max-updates 15000 --optimizer-betas 0.9:0.98 --dist \
#     --initial-learning-rate 0.06325 \
#     --learning-rate-scheduler-type inv-sqrt-decay --learning-rate-warmup 4000 \
#     --seed 1 --quiet-secondary-workers

# Training on larger data typically requires more updates for the model to reach a perplexity plateau. 
# When using the above recipe with larger data sets, increase the number of updates (--max-updates) 
# or train until the model does not improve over many checkpoints 
# (specify --max-num-checkpoint-not-improved X instead of --max-updates Y).

cd "$CURRENT"


