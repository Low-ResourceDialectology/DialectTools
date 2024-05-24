#!/bin/bash
# Translate a file from source to target language(s)
# bash SacreBLEU.sh "/media/AllBlue/LanguageData/CLEAN/German/2022NLLBNLLB_devtest.deuL" "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-engL-mult-deuL-NLLB-0001"

# SacreBLEU → https://github.com/mjpost/sacreBLEU
source /media/AllBlue/LanguageData/TOOLS/vSacreBLEU/bin/activate

# SacreBLEU knows about common test sets (as detailed in: sacrebleu --list), 
# but you can also use it to score system outputs with arbitrary references. 
# In this case, do not forget to provide detokenized reference and hypotheses files:

REFFILE="${1}"
TRANSDIR="${2}/*"
#"2022NLLBNLLB-Argo.deuL"
#"2022NLLBNLLB-Goog.deuL"
#"2022NLLBNLLB-NLLB.deuL"

for file in $TRANSDIR
do
    echo "${file}"
    sacrebleu "${REFFILE}" -i "${file}" -m bleu chrf ter -w 4
done

