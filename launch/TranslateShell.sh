#!/bin/bash
# Translate a file from source to target language(s)
# bash TranslateShell.sh "/media/AllBlue/LanguageData/CLEAN/English/2022NLLBNLLB_devtest.engL" "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-engL-mult-deuL-NLLB-0001/2022NLLBNLLB-Goog.deuL" en de google

CURRENT="$PWD"

INFILE="$1"
OUTFILE="$2"
# Languages → https://github.com/soimort/translate-shell/wiki/Languages
SRCLANG="$3"
TRGLANG="$4"
ENGINE="$5" # Available enginges via: trans -S
# aspell, google (default), bing, spell, hunspell, apertium, yandex

# Translate Shell → https://github.com/soimort/translate-shell
trans  file://"${INFILE}" -o "${OUTFILE}" -s "${SRCLANG}" :"${TRGLANG}" -e "${ENGINE}"

