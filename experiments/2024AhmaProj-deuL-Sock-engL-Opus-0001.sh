#!/bin/bash
# Acquired data via OpusTools and preprocessed close to (Her and Kruschhwitz, 2024)'s setup for comparison baseline

CURRENT="$PWD"

source /media/AllBlue/LanguageData/TOOLS/vSockeye/bin/activate

INPUTDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-de-Sock-en-Opus-0001/Sockeye-input"
SOURCE="de"
TARGET="en"
EXPID="0001"

SUBWORDDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/SubwordNMT"
mkdir "${SUBWORDDIR}" -p

PREPDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/Sockeye-prepared"
mkdir "${PREPDIR}" -p

TRAINDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/Sockeye-training"
mkdir "${TRAINDIR}" -p

EVALDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/Sockeye-evaluation"
mkdir "${EVALDIR}" -p

#DATA_DIR="/home/raman/Desktop/MT/Language_data/output/de-en/naive"
# NOTE: DATA_DIR == SUBWORDDIR
#cd $SUBWORDDIR
# Byte-Pair Encoding (BPE)
# cat "${INPUTDIR}/"train.de "${INPUTDIR}/"train.en | subword-nmt learn-bpe -s 32000 > codes
# for SET in train dev test; do
#   subword-nmt apply-bpe -c "${SUBWORDDIR}/"codes < "${INPUTDIR}/"${SET}.en > "${SUBWORDDIR}/"${SET}.en.bpe
#   subword-nmt apply-bpe -c "${SUBWORDDIR}/"codes < "${INPUTDIR}/"${SET}.de > "${SUBWORDDIR}/"${SET}.de.bpe
# done


#DATA_DIR="/home/raman/Desktop/MT/Language_data/output/de-en/naive"
#cd $DATA_DIR
# NOTE: DATA_DIR == SUBWORDDIR

# Serialize data into PyTorch's tensor format
# sockeye-prepare-data \
#     --source "${SUBWORDDIR}/"train.en.bpe \
#     --target "${SUBWORDDIR}/"train.de.bpe \
#     --shared-vocab \
#     --word-min-count 2 \
#     --pad-vocab-to-multiple-of 8 \
#     --max-seq-len 95 \
#     --num-samples-per-shard 10000000 \
#     --output "${PREPDIR}" \
#     --max-processes $(nproc)


# Hyperparameter Tuning
# for ACTIVATION in swish1 gelu relu;
# do
#     for LAYERS in 12 6;
#     do
#         TRAINDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/Sockeye-training-activation-${ACTIVATION}_layers-${LAYERS}"
#         mkdir "${TRAINDIR}" -p

#         sockeye-train \
#         --prepared-data "${PREPDIR}" \
#         --validation-source "${SUBWORDDIR}/"dev.en.bpe \
#         --validation-target "${SUBWORDDIR}/"dev.de.bpe \
#         --output "${TRAINDIR}" \
#         --num-layers "${LAYERS}" \
#         --transformer-model-size 512 \
#         --transformer-attention-heads 8 \
#         --transformer-feed-forward-num-hidden 2048 \
#         --transformer-activation-type "${ACTIVATION}" \
#         --amp \
#         --batch-type max-word \
#         --batch-size 5000 \
#         --update-interval 100 \
#         --checkpoint-interval 1000 \
#         --max-updates 5000 \
#         --optimizer-betas 0.9:0.98 \
#         --initial-learning-rate 0.06325 \
#         --learning-rate-scheduler-type inv-sqrt-decay \
#         --learning-rate-warmup 2000 \
#         --seed 1 \
#         --max-num-checkpoint-not-improved 1
#     done
# done



# TESTING THE TRAINED MODELS
# for ACTIVATION in swish1 gelu relu;
# do
#     for LAYERS in 12 6;
#     do
#         TRAINDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/Sockeye-training-activation-${ACTIVATION}_layers-${LAYERS}"
        
#         EVALDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/Sockeye-evaluation-activation-${ACTIVATION}_layers-${LAYERS}"
#         mkdir "${EVALDIR}" -p

#         # Translate the preprocessed test set
#         sockeye-translate \
#             --input "${SUBWORDDIR}/"test.en.bpe \
#             --output $EVALDIR/out.bpe \
#             --model $TRAINDIR \
#             --dtype float16 \
#             --beam-size 5 \
#             --batch-size 64

#     done
# done


# FINAL EVALUATION VIA sacreBLEU OF THE TRAINED MODELS
for ACTIVATION in swish1 gelu relu;
do
    for LAYERS in 12 6;
    do
        TRAINDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/Sockeye-training-activation-${ACTIVATION}_layers-${LAYERS}"
        
        EVALDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/Sockeye-evaluation-activation-${ACTIVATION}_layers-${LAYERS}"

        # We reverse BPE and score the translations against the reference using sacreBLEU:
        source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate

        sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out.bpe >"${EVALDIR}"/out.tok
        sacrebleu "${INPUTDIR}"/test."${TARGET}" -tok none -i "${EVALDIR}"/out.tok -m bleu ter chrf > "${EVALDIR}/eval-metrics.json"

        # We translated "test.de" (German) into "out.bpe" (English)
        # Now we compare the content of "out.bpe" (English) with "test.en" (English)
    done
done


# ++++++++++++++++++++++++++++++++++++++++++
# The lines of code BELOW are from earlier, when we worked with only a single experiment setup and without hyper-parameter-fine-tuning!


# DATA_DIR="/home/raman/Desktop/MT/Language_data/output/de-en/naive"
# MODEL_DIR="/home/raman/Desktop/MT/Language_data/output/de-en/naive/model"
# OUTPUT_DIR="/home/raman/Desktop/MT/Language_data/output/de-en/naive"
# cd $DATA_DIR

# TEMPORARY TRAINING TO TEST:
# TRAINDIR="/media/AllBlue/LanguageData/WORKS/Ramans-University-Project/2024AhmaProj-${SOURCE}-Sock-${TARGET}-Opus-${EXPID}/Sockeye-training-transformer-model-size-512_transformer-attention-heads-8"

# # # Translate the preprocessed test set
# sockeye-translate \
#     --input "${SUBWORDDIR}/"test.en.bpe \
#     --output $EVALDIR/out.bpe \
#     --model $TRAINDIR \
#     --dtype float16 \
#     --beam-size 5 \
#     --batch-size 64



# TEMP EVALUATION OF A SINGLE MODEL TRANSLATION


# We then reverse BPE and score the translations against the reference using sacreBLEU:
###############################################################################
# source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate

# sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out.bpe >"${EVALDIR}"/out.tok
# sacrebleu "${INPUTDIR}"/test."${TARGET}" -tok none -i "${EVALDIR}"/out.tok -m bleu ter chrf

# We translated "test.de" (German) into "out.bpe" (English)
# Now we compare the content of "out.bpe" (English) with "test.en" (English)




