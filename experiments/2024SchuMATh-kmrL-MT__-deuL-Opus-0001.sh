#!/bin/bash
# Train neural machine translation with cross-validation using Sockeye

# System: Base
# Direction: kmr-deu

source /media/AllBlue/LanguageData/TOOLS/vSockeye/bin/activate
INPUTDIR="/media/AllBlue/LanguageData/PREP/opustools"

# ku-de → ckb-deu & kmr-deu
# ku-en → ckb-eng & kmr-eng

SRC="ku"
SOURCE="kmr"  # "ckb"
TRG="de"
TARGET="deu"  # "eng"
EXPID="0001"
DATE="20240525"
INPUT="${INPUTDIR}/${SRC}-${TRG}/${DATE}/${SOURCE}-${TARGET}"

SUBWORDDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-MT__-${TARGET}L-Opus-${EXPID}/SubwordNMT"
mkdir "${SUBWORDDIR}" -p
PREPDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-MT__-${TARGET}L-Opus-${EXPID}/Sockeye-prepared"
mkdir "${PREPDIR}" -p
TRAINDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-MT__-${TARGET}L-Opus-${EXPID}/Sockeye-training"
mkdir "${TRAINDIR}" -p
EVALDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-${SOURCE}L-MT__-${TARGET}L-Opus-${EXPID}/Sockeye-evaluation"
mkdir "${EVALDIR}" -p

# Wrapper for cross validation

# This initializes three arrays with values corresponding to the training and testing iterations.
train_it=("1" "2" "3" "4" "5")
train_it2=("4" "5" "1" "2" "3")
test_it=("5" "1" "2" "3" "4")

# This loop goes through each index from 0 to 4, setting variables for the current cross-validation fold, 
# source and target training files, and source and target test files.
for ((i=0;i<=4;i++))
do
    cv_fold="${SRC}-${TRG}${train_it[i]}-${train_it2[i]}"
    source_train="${SRC}${train_it[i]}-${train_it2[i]}"
    target_train="${TRG}${train_it[i]}-${train_it2[i]}"
    source_test="${SRC}-${test_it[i]}"
    target_test="${TRG}-${test_it[i]}"
    echo "CV Fold: $cv_fold"
    mkdir -p "${SUBWORDDIR}/${cv_fold}"
    mkdir -p "${PREPDIR}/${cv_fold}"
    mkdir -p "${TRAINDIR}/${cv_fold}"
    mkdir -p "${EVALDIR}/${cv_fold}"

    # Prepare training files by concatenating the relevant parts
    source_train_concat="${INPUT}/train_${source_train}.txt"
    target_train_concat="${INPUT}/train_${target_train}.txt"

    # Create the concatenated training files
    rm -f $source_train_concat $target_train_concat  # Remove if they already exist
    for part in ${train_it[@]}
    do
        if [[ $part != ${test_it[i]} ]]; then
            cat "${INPUT}/${SRC}-$part" >> $source_train_concat
            cat "${INPUT}/${TRG}-$part" >> $target_train_concat
        fi
    done

    # Ensure the concatenated files exist
    if [[ ! -f $source_train_concat || ! -f $target_train_concat ]]; then
        echo "Error: Concatenated files not created correctly."
        exit 1
    fi

    #echo "Source Train: ${source_train_concat}"
    #echo "Target Train: ${target_train_concat}"
    #echo "Source Test: ${source_test}"
    #echo "Target Test: ${target_test}"

# Learn bpe
    # subword-nmt learn-joint-bpe-and-vocab \
    # -i "${source_train_concat}" "${target_train_concat}" \
    # -o "${SUBWORDDIR}/${cv_fold}/bpe.codes" \
    # -s 30000 \
    # --write-vocabulary "${SUBWORDDIR}/${cv_fold}/bpe.vocab.${SRC}" "${SUBWORDDIR}/${cv_fold}/bpe.vocab.${TRG}"


# Apply bpe

    # subword-nmt apply-bpe -c "${SUBWORDDIR}/${cv_fold}/bpe.codes" \
    # --dropout 0.1 \
    # --vocabulary "${SUBWORDDIR}/${cv_fold}/bpe.vocab.${SRC}" \
    # --vocabulary-threshold 50 \
    # < "${source_train_concat}" > "${SUBWORDDIR}/${cv_fold}/${source_train}.bpe"

    # subword-nmt apply-bpe -c "${SUBWORDDIR}/${cv_fold}/bpe.codes" \
    # --dropout 0.1 \
    # --vocabulary "${SUBWORDDIR}/${cv_fold}/bpe.vocab.${TRG}" \
    # --vocabulary-threshold 50 \
    # < "${target_train_concat}" > "${SUBWORDDIR}/${cv_fold}/${target_train}.bpe"

    # subword-nmt apply-bpe -c "${SUBWORDDIR}/${cv_fold}/bpe.codes" \
    # --vocabulary "${SUBWORDDIR}/${cv_fold}/bpe.vocab.${SRC}" \
    # --vocabulary-threshold 50 \
    # < "${INPUT}/${source_test}" > "${SUBWORDDIR}/${cv_fold}/${source_test}.bpe"

    # subword-nmt apply-bpe -c "${SUBWORDDIR}/${cv_fold}/bpe.codes" \
    # --vocabulary "${SUBWORDDIR}/${cv_fold}/bpe.vocab.${TRG}" \
    # --vocabulary-threshold 50 \
    # < "${INPUT}/${target_test}" > "${SUBWORDDIR}/${cv_fold}/${target_test}.bpe"

# Serialize data

    # sockeye-prepare-data \
    # -s "${SUBWORDDIR}/${cv_fold}/${source_train}.bpe" \
    # -t "${SUBWORDDIR}/${cv_fold}/${target_train}.bpe" \
    # -o "${PREPDIR}/${cv_fold}" \
    # --shared-vocab

# Start training

    # sockeye-train --prepared-data "${PREPDIR}/${cv_fold}" \
    # --validation-source "${SUBWORDDIR}/${cv_fold}/${source_test}.bpe" \
    # --validation-target "${SUBWORDDIR}/${cv_fold}/${target_test}.bpe" \
    # --output "${TRAINDIR}/${cv_fold}" \
    # --encoder transformer \
    # --decoder transformer \
    # --num-layers 6 \
    # --num-embed 512 \
    # --transformer-model-size 512 \
    # --transformer-attention-heads 8 \
    # --transformer-feed-forward-num-hidden 2048 \
    # --max-seq-len 120 \
    # --decode-and-evaluate 500 \
    # --max-num-checkpoint-not-improved 3 \
    # --shared-vocab


# Preprocess test samples:
    #source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate
    #python3 development-latin-parallel-corpus-split-kur-clean-tokenize.py 
    # source /media/AllBlue/LanguageData/TOOLS/vSockeye/bin/activate
    # subword-nmt apply-bpe -c "${SUBWORDDIR}/${cv_fold}/bpe.codes" \
    # < "${EVALDIR}/T06-clean.kob" \
    # > "${EVALDIR}/T06-clean.kob.bpe"


# When training is complete, we translate the preprocessed test set:

    # sockeye-translate \
    # --input "${EVALDIR}/T06-clean.kob.bpe" \
    # --output "${EVALDIR}/${cv_fold}/T06.kob.out" \
    # --model "${TRAINDIR}/${cv_fold}" \
    # --dtype float16 \
    # --beam-size 5 \
    # --batch-size 64



# # We then reverse BPE and score the translations against the reference using sacreBLEU:
# ###############################################################################
    #sed -re 's/(@@ |@@$)//g' < "${EVALDIR}/${cv_fold}/T06.kob.out" > "${EVALDIR}/${cv_fold}/T06-kob.out.tok"
    #sacrebleu "${INPUTDIR}/test.${TARGET}" -i "${EVALDIR}"/out-"${SOURCE}".tok -m bleu chrf ter

done

#sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${SOURCE}".bpe >"${EVALDIR}"/out-"${SOURCE}".tok
#sacrebleu "${INPUTDIR}"/test."${TARGET}" -tok none -i "${EVALDIR}"/out-"${SOURCE}".tok

# sed -re 's/(@@ |@@$)//g' <"${EVALDIR}"/out-"${TARGET}".bpe >"${EVALDIR}"/out-"${TARGET}".tok
# sacrebleu "${INPUTDIR}"/test."${SOURCE}" -tok none -i "${EVALDIR}"/out-"${TARGET}".tok


# SacreBLEU → https://github.com/mjpost/sacreBLEU
#source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate
#sacrebleu "${INPUTDIR}/test.${TARGET}"  -i "${file}" -m bleu chrf ter -w 4


# remove tokenization

#cat translations/test.${SRC}-${TGT}.tok.${TGT} | $MOSES/tokenizer/detokenizer.perl -l "${TGT}" > translations/test.${SRC}-${TGT}.${TGT}


# sacrebleu "${INPUTDIR}/test.${TARGET}" \
#     -i "${EVALDIR}"/out-"${TARGET}".tok \
#     -m bleu chrf ter #-w 4


# sacrebleu "${INPUTDIR}/test.${TARGET}" \
#     -i "${EVALDIR}"/out-"${TARGET}".tok \
#     -tok none \
#     -m bleu chrf ter -w 4









