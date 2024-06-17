#!/bin/bash
# Project: Any
# Get information of text inside the files of a directory

# NOTE: Translating test-set-files of previously perturbed text data left me clueless as to why they all have differing number of lines now...

filename_part="test"
thresholds=2000


echo "ORIGINAL FILES (opustools)"
input_path="/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

echo "ORIGINAL FILES (Reference)"
input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/Bavarian/English/NLLB/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

echo "PERTURBED FILES (GERMAN)"
input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/all/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/lex/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/mor/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

echo "PERTURBED FILES (BAVARIAN)"
input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/all/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/lex/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/mor/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

echo "TRANSLATED FILES (GERMAN)"
input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/all/English/NLLB/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/lex/English/NLLB/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/mor/English/NLLB/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

echo "TRANSLATED FILES (BAVARIAN)"
input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/all/English/NLLB/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/lex/English/NLLB/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/mor/English/NLLB/"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"


