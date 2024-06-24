#!/bin/bash
# Project: Any
# Get information of text inside the files of a directory



# ---
# Checking data quantities
filename_part="bar-de"
thresholds=100,200,300,400,500,1000

input_path="/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/clean"
python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"




# ---

# filename_part="bar"
# thresholds=100,200,300,400

# input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/all"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"



# ---

# NOTE: Reasoning for the right threshold to truncate sentences on → Result: 200
# filename_part="bar-de"
# thresholds=100,200,300,400,500,1000

# input_path="/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/naive/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"




# ---

# NOTE: Translating test-set-files of previously perturbed text data left me clueless as to why they all have differing number of lines now...

# filename_part="test"
# thresholds=2000


# Second phase on English-Bavarian noisy data
# → The prepared data of English has one line more than the Bavarian text
#input_path="/media/AllBlue/LanguageData/PREP/opustools/bar-en/naive/"
#python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

# → Looking at the separate datasets of opustools one-by-one
#input_path="/media/AllBlue/LanguageData/CLEAN/opustools/bar-en/naive/"
#python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# → All aligned files have the same number of lines, but one English file has ONE line longer than 2000 which the aligned Bavarian file does NOT
#   /media/AllBlue/LanguageData/CLEAN/opustools/bar-en/naive/wikimedia-bar-en-test.en

# → Looking for a reasonable cut-off threshold to fix this tiny issue
# input_path="/media/AllBlue/LanguageData/PREP/opustools/bar-en/naive/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

# ---

# Very first Phase using German-Bavarian noisy data
# echo "ORIGINAL FILES (opustools)"
# input_path="/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

# echo "ORIGINAL FILES (Reference)"
# input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/Bavarian/English/NLLB/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

# echo "PERTURBED FILES (GERMAN)"
# input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/all/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/lex/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/naive/Bavarian/mor/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

# echo "PERTURBED FILES (BAVARIAN)"
# input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/all/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/lex/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/naive/German/mor/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

# echo "TRANSLATED FILES (GERMAN)"
# input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/all/English/NLLB/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/lex/English/NLLB/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/naive/Bavarian/mor/English/NLLB/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"

# echo "TRANSLATED FILES (BAVARIAN)"
# input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/all/English/NLLB/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/lex/English/NLLB/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"
# input_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/naive/German/mor/English/NLLB/"
# python3 ../function/evaluate/textfiles.py -i "${input_path}" -f "${filename_part}" -t "${thresholds}"


