#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# cd /media/CrazyProjects/LowResDialectology/DialectTools/setup
# bash TranslateLocally.sh

echo "App starts and can be called via CLI- but any time I try to translate something, I get something like -Aborted (core dumped)- and get kicked out..."

# Translating Sentences
echo "Lillian Diana Gish (October 14, 1893 – February 27, 1993) was an American actress, director and screenwriter." | /media/AllBlue/LanguageData/TOOLS/TranslateLocally/build/translateLocally -m en-de-base
# echo "Lillian Diana Gish (October 14, 1893 – February 27, 1993) was an American actress, director and screenwriter." | ./translateLocally -m en-de-base

# Translating Files

# English to German
#/media/AllBlue/LanguageData/TOOLS/TranslateLocally/build/translateLocally -m en-de-base -i /media/AllBlue/LanguageData/PREP/2024SchuMATh-engL-TrLo-deuL-NLLB-0001/engL.txt -o /media/AllBlue/LanguageData/PREP/2024SchuMATh-engL-TrLo-deuL-NLLB-0001/engL-deuL.txt

# German to English
#/media/AllBlue/LanguageData/TOOLS/TranslateLocally/build/translateLocally -m de-en-base -i /path_to_input_file -o /path_to_output_file


