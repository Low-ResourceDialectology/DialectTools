#!/bin/bash
# Project: Any
# Get information of text inside the files of a directory

# NOTE: Translating test-set-files of previously perturbed text data left me clueless as to why they all have differing number of lines now...

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/clean/exclude_long_sentences.py"

# echo "ORIGINAL FILES (opustools)"
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive/blubb.de" \
    -o "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive/test.de" \
    -m 1200
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive/blubb.bar" \
    -o "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive/test.bar" \
    -m 1000

# echo "ORIGINAL FILES (Reference)"
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/Bavarian/English/NLLB/blubb.en" \
    -o "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/Bavarian/English/NLLB/test.en" \
    -m 1054
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB/blubb.en" \
    -o "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB/test.en" \
    -m 1200

# echo "PERTURBED FILES (GERMAN)"
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/all/blubb.de" \
    -o "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/all/test.de" \
    -m 950
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/lex/blubb.de" \
    -o "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/lex/test.de" \
    -m 1200
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/mor/blubb.de" \
    -o "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/mor/test.de" \
    -m 950

# echo "PERTURBED FILES (BAVARIAN)"
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/all/blubb.bar" \
    -o "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/all/test.bar" \
    -m 1960
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/lex/blubb.bar" \
    -o "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/lex/test.bar" \
    -m 1330
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/mor/blubb.bar" \
    -o "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/mor/test.bar" \
    -m 1400

# echo "TRANSLATED FILES (GERMAN)"
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/all/English/NLLB/blubb.en" \
    -o "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/all/English/NLLB/test.en" \
    -m 1150
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/lex/English/NLLB/blubb.en" \
    -o "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/lex/English/NLLB/test.en" \
    -m 1160
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/mor/English/NLLB/blubb.en" \
    -o "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/mor/English/NLLB/test.en" \
    -m 1200

# echo "TRANSLATED FILES (BAVARIAN)"
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/all/English/NLLB/blubb.en" \
    -o "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/all/English/NLLB/test.en" \
    -m 2254
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/lex/English/NLLB/blubb.en" \
    -o "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/lex/English/NLLB/test.en" \
    -m 1750
python3 "${script_file}" \
    -i "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/mor/English/NLLB/blubb.en" \
    -o "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/mor/English/NLLB/test.en" \
    -m 2050

