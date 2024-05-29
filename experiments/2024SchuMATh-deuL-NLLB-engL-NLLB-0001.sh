#!/bin/bash

# Use different sizes of NLLB models to translate text from a file.

# bash 2024SchuMATh-deuL-NLLB-engL-NLLB-0001.sh facebook nllb-200-3.3B 3.3B deu_Latn /media/AllBlue/LanguageData/DOWNLOAD/datasets/2022NLLBNLLB/floresp-v2.0-rc.3/dev dev deu_Latn eng_Latn /media/AllBlue/LanguageData/EXPERIMENT 2024SchuMATh-deuL-NLLB-engL-NLLB-0001

#bash 2024SchuMATh-deuL-NLLB-engL-NLLB-0001.sh facebook nllb-200-3.3B 3.3B deu_Latn /media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001 deu test eng_Latn /media/AllBlue/LanguageData/EXPERIMENT deueng 2024SchuMATh-deuL-NLLB-engL-NLLB-0001
#bash 2024SchuMATh-deuL-NLLB-engL-NLLB-0001.sh facebook nllb-200-3.3B 3.3B deu_Latn /media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001 deu dev eng_Latn /media/AllBlue/LanguageData/EXPERIMENT deueng 2024SchuMATh-deuL-NLLB-engL-NLLB-0001
#bash 2024SchuMATh-deuL-NLLB-engL-NLLB-0001.sh facebook nllb-200-3.3B 3.3B deu_Latn /media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001 deu train eng_Latn /media/AllBlue/LanguageData/EXPERIMENT deueng 2024SchuMATh-deuL-NLLB-engL-NLLB-0001

#bash 2024SchuMATh-deuL-NLLB-engL-NLLB-0001.sh facebook nllb-200-3.3B 3.3B deu_Latn /media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001 bar test eng_Latn /media/AllBlue/LanguageData/EXPERIMENT bareng 2024SchuMATh-deuL-NLLB-engL-NLLB-0001
#bash 2024SchuMATh-deuL-NLLB-engL-NLLB-0001.sh facebook nllb-200-3.3B 3.3B deu_Latn /media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001 bar dev eng_Latn /media/AllBlue/LanguageData/EXPERIMENT bareng 2024SchuMATh-deuL-NLLB-engL-NLLB-0001
#bash 2024SchuMATh-deuL-NLLB-engL-NLLB-0001.sh facebook nllb-200-3.3B 3.3B deu_Latn /media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001 bar train eng_Latn /media/AllBlue/LanguageData/EXPERIMENT bareng 2024SchuMATh-deuL-NLLB-engL-NLLB-0001

CURRENTDIR="$PWD"
AUTHORID=${1:-"facebook"}
MODELID=${2:-"nllb-200-3.3B"}
MODELNAME=${3:-"3.3B"}
INLANG=${4:-"deu_Latn"}
INDIR=${5:-"/media/AllBlue/LanguageData/DOWNLOAD/datasets/2022NLLBNLLB/floresp-v2.0-rc.3/dev"}
INFILEEXTENSION=${6:-"deu_Latn"}
INFILENAME=${7:-"dev"}
# → "${INDIR}/${INFILENAME}.${INFILEEXTENSION}"
OUTLANG=${8:-"eng_Latn"}
OUTDIR=${9:-"/media/AllBlue/LanguageData/EXPERIMENT"}
OUTFILEEXTENSION=${10:-"eng_Latn"}
EXPERIMENT=${11:-"DEFAULT_PATH_CHECK_YOUR_INPUT_BUDDY"}
OUTFILE=${12:-"${INFILENAME}.${OUTFILEEXTENSION}"}
#OUTFILE=${12:-"${INFILENAME}-${MODELNAME}-${OUTLANG}.${OUTFILEEXTENSION}"}
# → "${OUTDIR}/${EXPERIMENT}/${OUTFILE}"

# Create output directory and copy input file over prior to translation process
mkdir "${OUTDIR}/${EXPERIMENT}"
cp "${INDIR}/${INFILENAME}.${INFILEEXTENSION}" "${OUTDIR}/${INFILENAME}.${INFILEEXTENSION}"

source /media/AllBlue/LanguageData/TOOLS/vNLLB/bin/activate

python3 "${CURRENTDIR}"/../launch/NLLB.py \
    --input_lang "${INLANG}" \
    --input_file "${INDIR}/${INFILENAME}.${INFILEEXTENSION}" \
    --output_lang "${OUTLANG}" \
    --output_file "${OUTDIR}/${EXPERIMENT}/${OUTFILE}" \
    --authorid "${AUTHORID}" \
    --modelid "${MODELID}"

