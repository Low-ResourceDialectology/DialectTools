#!/bin/bash

# Use: 
# bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/Tokenizer.sh 

#cd /media/CrazyProjects/LowResDialectology/DialectTools/clean
source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

INFILE="${1}"
OUTFILE="${2}"
LANG="${3:-'deu'}"
PREPROCESS="${4:-'p'}"
TOKENIZE="${5:-'t'}"
CURRENTDIR="$PWD"

echo "Language defaults to deu"
#python3 "${CURRENTDIR}"/../clean/Tokenizer.py -i "${INFILE}" -o "${OUTFILE}" -l "${LANG}" -"${PREPROCESS}" -"${TOKENIZE}"
echo  "${CURRENTDIR}"/../clean/Tokenizer.py -i "${INFILE}" -o "${OUTFILE}" -l "${LANG}" -"${PREPROCESS}" -"${TOKENIZE}"
