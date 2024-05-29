#!/bin/bash
# Train neural machine translation model for language pair

#source /media/AllBlue/LanguageData/TOOLS/vSockeye/bin/activate

INPUTDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-deuL-NLLB-engL-NLLB-0001"
SOURCE="bar"
TARGET="deueng"

SUBWORDDIR="${INPUTDIR}/${SOURCE}-${TARGET}/SubwordNMT-small"
mkdir "${SUBWORDDIR}" -p
PREPDIR="${INPUTDIR}/${SOURCE}-${TARGET}/Sockeye-prepared-small"
mkdir "${PREPDIR}" -p
TRAINDIR="${INPUTDIR}/${SOURCE}-${TARGET}/Sockeye-training-small"
mkdir "${TRAINDIR}" -p
EVALDIR="${INPUTDIR}/${SOURCE}-${TARGET}/Sockeye-evaluation-small"
mkdir "${EVALDIR}" -p

# At this point the data should already tokenized, so we only need to apply byte-pair encoding (Sennrich et al., 2016): → https://aclanthology.org/P16-1162/
# cat "${INPUTDIR}"/train."${SOURCE}" "${INPUTDIR}"/train."${TARGET}" |subword-nmt learn-bpe -s 30000 > "${SUBWORDDIR}"/bpe.codes

# for SET in dev test; do
#   subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/"${SET}"."${SOURCE}" >"${SUBWORDDIR}"/"${SET}"."${SOURCE}".bpe
#   subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/"${SET}"."${TARGET}" >"${SUBWORDDIR}"/"${SET}"."${TARGET}".bpe
# done
# subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/train."${SOURCE}" >"${SUBWORDDIR}"/train."${SOURCE}".bpe
# subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/train."${TARGET}" >"${SUBWORDDIR}"/train."${TARGET}".bpe

# # We first split the byte-pair encoded training data into shards and serialize it in PyTorch's tensor format. 
# # This allows us to train on data of any size by loading and unloading different pieces throughout training:
# sockeye-prepare-data \
#     --source "${SUBWORDDIR}"/train."${SOURCE}".bpe --target "${SUBWORDDIR}"/train."${TARGET}".bpe --shared-vocab --output "${PREPDIR}"

# # The following command trains a big transformer (Vaswani et al., 2017) → https://arxiv.org/abs/1706.03762
# # using the large batch recipe described by Ott et al. (2018) → https://arxiv.org/abs/1806.00187
# # We then launch training on 1 GPU. 
# sockeye-train \
#   --prepared-data "${PREPDIR}" \
#   --validation-source "${SUBWORDDIR}"/dev."${SOURCE}".bpe \
#   --validation-target "${SUBWORDDIR}"/dev."${TARGET}".bpe \
#   --output "${TRAINDIR}" \
#   --encoder transformer \
#   --decoder transformer \
#   --transformer-model-size 256 \
#   --transformer-attention-heads 8 \
#   --transformer-feed-forward-num-hidden 256 \
#   --num-layers 6 \
#   --num-embed 256 \
#   --batch-size 4096 \
#   --initial-learning-rate 0.06325 \
#   --learning-rate-scheduler-type inv-sqrt-decay \
#   --learning-rate-warmup 4000 \
#   --optimizer "adam" \
#   --label-smoothing 0.1 \
#   --decode-and-evaluate 500 \
#   --checkpoint-interval 500 \
#   --max-num-checkpoint-not-improved 3 \
#   --max-updates 15000 \
#   --num-words 30000 \
#   --max-seq-len 100 \
#   --shared-vocab

# sockeye-translate \
#     --input "${SUBWORDDIR}"/test."${SOURCE}".bpe \
#     --output "${EVALDIR}"/out-"${SOURCE}".bpe \
#     --model "${TRAINDIR}" \
#     --dtype float16 \
#     --beam-size 5 \
#     --batch-size 64

source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate
sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${SOURCE}".bpe >"${EVALDIR}"/out-"${SOURCE}".tok
sacrebleu "${INPUTDIR}"/test."${TARGET}" -tok none -i "${EVALDIR}"/out-"${SOURCE}".tok -m bleu chrf ter






SUBWORDDIR="${INPUTDIR}/${SOURCE}-${TARGET}/SubwordNMT-med"
mkdir "${SUBWORDDIR}" -p
PREPDIR="${INPUTDIR}/${SOURCE}-${TARGET}/Sockeye-prepared-med"
mkdir "${PREPDIR}" -p
TRAINDIR="${INPUTDIR}/${SOURCE}-${TARGET}/Sockeye-training-med"
mkdir "${TRAINDIR}" -p
EVALDIR="${INPUTDIR}/${SOURCE}-${TARGET}/Sockeye-evaluation-med"
mkdir "${EVALDIR}" -p

# At this point the data should already tokenized, so we only need to apply byte-pair encoding (Sennrich et al., 2016): → https://aclanthology.org/P16-1162/
# cat "${INPUTDIR}"/train."${SOURCE}" "${INPUTDIR}"/train."${TARGET}" |subword-nmt learn-bpe -s 30000 > "${SUBWORDDIR}"/bpe.codes

# for SET in dev test; do
#   subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/"${SET}"."${SOURCE}" >"${SUBWORDDIR}"/"${SET}"."${SOURCE}".bpe
#   subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/"${SET}"."${TARGET}" >"${SUBWORDDIR}"/"${SET}"."${TARGET}".bpe
# done
# subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/train."${SOURCE}" >"${SUBWORDDIR}"/train."${SOURCE}".bpe
# subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/train."${TARGET}" >"${SUBWORDDIR}"/train."${TARGET}".bpe

# # We first split the byte-pair encoded training data into shards and serialize it in PyTorch's tensor format. 
# # This allows us to train on data of any size by loading and unloading different pieces throughout training:
# sockeye-prepare-data \
#     --source "${SUBWORDDIR}"/train."${SOURCE}".bpe --target "${SUBWORDDIR}"/train."${TARGET}".bpe --shared-vocab --output "${PREPDIR}"

# # The following command trains a big transformer (Vaswani et al., 2017) → https://arxiv.org/abs/1706.03762
# # using the large batch recipe described by Ott et al. (2018) → https://arxiv.org/abs/1806.00187
# # We then launch training on 1 GPU. 
# sockeye-train \
#   --prepared-data "${PREPDIR}" \
#   --validation-source "${SUBWORDDIR}"/dev."${SOURCE}".bpe \
#   --validation-target "${SUBWORDDIR}"/dev."${TARGET}".bpe \
#   --output "${TRAINDIR}" \
#   --encoder transformer \
#   --decoder transformer \
#   --transformer-model-size 512 \
#   --transformer-attention-heads 8 \
#   --transformer-feed-forward-num-hidden 512 \
#   --num-layers 6 \
#   --num-embed 512 \
#   --batch-size 4096 \
#   --initial-learning-rate 0.06325 \
#   --learning-rate-scheduler-type inv-sqrt-decay \
#   --learning-rate-warmup 4000 \
#   --optimizer "adam" \
#   --label-smoothing 0.1 \
#   --decode-and-evaluate 500 \
#   --checkpoint-interval 500 \
#   --max-num-checkpoint-not-improved 3 \
#   --max-updates 15000 \
#   --num-words 30000 \
#   --max-seq-len 100 \
#   --shared-vocab

# sockeye-translate \
#     --input "${SUBWORDDIR}"/test."${SOURCE}".bpe \
#     --output "${EVALDIR}"/out-"${SOURCE}".bpe \
#     --model "${TRAINDIR}" \
#     --dtype float16 \
#     --beam-size 5 \
#     --batch-size 64

source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate
sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${SOURCE}".bpe >"${EVALDIR}"/out-"${SOURCE}".tok
sacrebleu "${INPUTDIR}"/test."${TARGET}" -tok none -i "${EVALDIR}"/out-"${SOURCE}".tok -m bleu chrf ter










SUBWORDDIR="${INPUTDIR}/${SOURCE}-${TARGET}/SubwordNMT-big"
mkdir "${SUBWORDDIR}" -p
PREPDIR="${INPUTDIR}/${SOURCE}-${TARGET}/Sockeye-prepared-big"
mkdir "${PREPDIR}" -p
TRAINDIR="${INPUTDIR}/${SOURCE}-${TARGET}/Sockeye-training-big"
mkdir "${TRAINDIR}" -p
EVALDIR="${INPUTDIR}/${SOURCE}-${TARGET}/Sockeye-evaluation-big"
mkdir "${EVALDIR}" -p

# At this point the data should already tokenized, so we only need to apply byte-pair encoding (Sennrich et al., 2016): → https://aclanthology.org/P16-1162/
# cat "${INPUTDIR}"/train."${SOURCE}" "${INPUTDIR}"/train."${TARGET}" |subword-nmt learn-bpe -s 30000 > "${SUBWORDDIR}"/bpe.codes

# for SET in dev test; do
#   subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/"${SET}"."${SOURCE}" >"${SUBWORDDIR}"/"${SET}"."${SOURCE}".bpe
#   subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/"${SET}"."${TARGET}" >"${SUBWORDDIR}"/"${SET}"."${TARGET}".bpe
# done
# subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/train."${SOURCE}" >"${SUBWORDDIR}"/train."${SOURCE}".bpe
# subword-nmt apply-bpe -c "${SUBWORDDIR}"/bpe.codes <"${INPUTDIR}"/train."${TARGET}" >"${SUBWORDDIR}"/train."${TARGET}".bpe

# # We first split the byte-pair encoded training data into shards and serialize it in PyTorch's tensor format. 
# # This allows us to train on data of any size by loading and unloading different pieces throughout training:
# sockeye-prepare-data \
#     --source "${SUBWORDDIR}"/train."${SOURCE}".bpe --target "${SUBWORDDIR}"/train."${TARGET}".bpe --shared-vocab --output "${PREPDIR}"

# # The following command trains a big transformer (Vaswani et al., 2017) → https://arxiv.org/abs/1706.03762
# # using the large batch recipe described by Ott et al. (2018) → https://arxiv.org/abs/1806.00187
# # We then launch training on 1 GPU. 
# sockeye-train \
#   --prepared-data "${PREPDIR}" \
#   --validation-source "${SUBWORDDIR}"/dev."${SOURCE}".bpe \
#   --validation-target "${SUBWORDDIR}"/dev."${TARGET}".bpe \
#   --output "${TRAINDIR}" \
#   --encoder transformer \
#   --decoder transformer \
#   --transformer-model-size 1024 \
#   --transformer-attention-heads 8 \
#   --transformer-feed-forward-num-hidden 1024 \
#   --num-layers 6 \
#   --num-embed 1024 \
#   --batch-size 4096 \
#   --initial-learning-rate 0.06325 \
#   --learning-rate-scheduler-type inv-sqrt-decay \
#   --learning-rate-warmup 4000 \
#   --optimizer "adam" \
#   --label-smoothing 0.1 \
#   --decode-and-evaluate 500 \
#   --checkpoint-interval 500 \
#   --max-num-checkpoint-not-improved 3 \
#   --max-updates 15000 \
#   --num-words 30000 \
#   --max-seq-len 100 \
#   --shared-vocab

# sockeye-translate \
#     --input "${SUBWORDDIR}"/test."${SOURCE}".bpe \
#     --output "${EVALDIR}"/out-"${SOURCE}".bpe \
#     --model "${TRAINDIR}" \
#     --dtype float16 \
#     --beam-size 5 \
#     --batch-size 64

source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate
sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${SOURCE}".bpe >"${EVALDIR}"/out-"${SOURCE}".tok
sacrebleu "${INPUTDIR}"/test."${TARGET}" -tok none -i "${EVALDIR}"/out-"${SOURCE}".tok -m bleu chrf ter














# Training on larger data typically requires more updates for the model to reach a perplexity plateau. 
# When using the above recipe with larger data sets, increase the number of updates (--max-updates) 
# or train until the model does not improve over many checkpoints 
# (specify --max-num-checkpoint-not-improved X instead of --max-updates Y).


# When training is complete, we translate the preprocessed test set:
###############################################################################
# One direction
# sockeye-translate \
#     --input "${SUBWORDDIR}"/test."${SOURCE}".bpe \
#     --output "${EVALDIR}"/out-"${SOURCE}".bpe \
#     --model "${TRAINDIR}" \
#     --dtype float16 \
#     --beam-size 5 \
#     --batch-size 64

# Switch to other venv
# deactivate
# source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate

# # We then reverse BPE and score the translations against the reference using sacreBLEU:
# ###############################################################################
#sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${SOURCE}".bpe >"${EVALDIR}"/out-"${SOURCE}".tok
#sacrebleu "${INPUTDIR}/test.${TARGET}" -i "${EVALDIR}"/out-"${SOURCE}".tok -m bleu chrf ter