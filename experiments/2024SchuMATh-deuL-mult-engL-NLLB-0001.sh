#!/bin/bash

# Machine translate English text to German
INDIR="/media/AllBlue/LanguageData/CLEAN/German"
INFILE="2022NLLBNLLB_devtest.deuL"
OUTDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-deuL-mult-engL-NLLB-0001"
mkdir "${OUTDIR}"

# Argos Translate → https://github.com/argosopentech/argos-translate
# Argos Translate Files → https://github.com/LibreTranslate/argos-translate-files
source /media/AllBlue/LanguageData/TOOLS/vArgosTranslate/bin/activate
python3 /media/CrazyProjects/LowResDialectology/DialectTools/launch/ArgosTranslateFiles.py --input_lang de --output_lang en --input_file "${INDIR}"/"${INFILE}" --output_file "${OUTDIR}"/2022NLLBNLLB-Argo.engL

# NLLB → https://github.com/facebookresearch/fairseq/tree/nllb
# ? Open-NLLB → https://github.com/gordicaleksa/Open-NLLB
source /media/AllBlue/LanguageData/TOOLS/vNLLB/bin/activate
python3 /media/CrazyProjects/LowResDialectology/DialectTools/launch/NLLB.py --input_lang deu_Latn --input_file "${INDIR}"/"${INFILE}" --output_lang eng_Latn --output_file "${OUTDIR}"/2022NLLBNLLB-NLLB.engL

# Translate Shell → https://github.com/soimort/translate-shell
# Translate Shell (Google Translate) → https://translate.google.com/
bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/TranslateShell.sh "${INDIR}"/"${INFILE}" "${OUTDIR}"/2022NLLBNLLB-Goog.engL de en google
# Translate Shell (aspell) → http://aspell.net/
#bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/TranslateShell.sh "${INDIR}"/"${INFILE}" "${OUTDIR}"/2022NLLBNLLB-Aspe.engL de en aspell
# Translate Shell (bing) → https://www.bing.com/translator
#bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/TranslateShell.sh "${INDIR}"/"${INFILE}" "${OUTDIR}"/2022NLLBNLLB-Bing.engL de en bing
# Translate Shell (spell)
#bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/TranslateShell.sh "${INDIR}"/"${INFILE}" "${OUTDIR}"/2022NLLBNLLB-Spel.engL de en spell
# Translate Shell (hunspell) → http://hunspell.github.io/
#bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/TranslateShell.sh "${INDIR}"/"${INFILE}" "${OUTDIR}"/2022NLLBNLLB-Huns.engL de en hunspell
# Translate Shell (apertium) → https://www.apertium.org/index.eng.html#?dir=eng-epo&q=
#bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/TranslateShell.sh "${INDIR}"/"${INFILE}" "${OUTDIR}"/2022NLLBNLLB-Aper.engL de en apertium
# Translate Shell (yandex) → https://translate.yandex.com/
#bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/TranslateShell.sh "${INDIR}"/"${INFILE}" "${OUTDIR}"/2022NLLBNLLB-Yand.engL de en yandex

# Evaluate the translations

# SacreBLEU → https://github.com/mjpost/sacreBLEU
bash /media/CrazyProjects/LowResDialectology/DialectTools/launch/SacreBLEU.sh "/media/AllBlue/LanguageData/CLEAN/English/2022NLLBNLLB_devtest.engL" "${OUTDIR}"




