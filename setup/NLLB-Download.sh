#!/bin/bash

# Download NLLB models from HuggingFace an run them once to translate a sentence.

# bash NLLB-Download.sh facebook nllb-200-3.3B 3.3B
# bash NLLB-Download.sh facebook nllb-200-1.3B 1.3B
# bash NLLB-Download.sh facebook nllb-200-distilled-1.3B dist1.3B
# bash NLLB-Download.sh facebook nllb-200-distilled-600M dist600M

AUTHOR=${1:-"facebook"}
MODEL=${2:-"nllb-200-1.3B"}
NAME=${3:-"1.3B"}
CURRENTDIR="$PWD"

source /media/AllBlue/LanguageData/TOOLS/vNLLB/bin/activate

python3 "${CURRENTDIR}"/../launch/NLLB.py \
    --input_lang eng_Latn \
    --input_file /media/AllBlue/LanguageData/TEST/testsent.eng \
    --output_lang deu_Latn \
    --output_file /media/AllBlue/LanguageData/TEST/testsent.eng-"${NAME}".deu \
    --authorid "${AUTHOR}" \
    --modelid "${MODEL}"

# NLLB Models on HuggingFace
# https://huggingface.co/facebook/nllb-200-3.3B
# https://huggingface.co/facebook/nllb-200-1.3B
# https://huggingface.co/facebook/nllb-200-distilled-1.3B
# https://huggingface.co/facebook/nllb-200-distilled-600M

# echo  "${CURRENTDIR}"/../launch/NLLB.py \
#     --input_lang eng_Latn \
#     --input_file /media/AllBlue/LanguageData/TEST/testsent.eng \
#     --output_lang deu_Latn \
#     --output_file /media/AllBlue/LanguageData/TEST/testsent.eng-"${NAME}".deu \
#     --authorid "${AUTHOR}" \
#     --modelid "${MODEL}"

