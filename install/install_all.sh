#!/bin/bash
# Install all tools
# Use: cd ./install
# bash install_all.sh

CURRENT="$PWD"

TOOLDIRIN="${1:-$(jq .data_root_dir ./../config.json)}"
TOOLDIRCLEAN="${TOOLDIRIN//\"/$''}"
TOOLDIR="${TOOLDIRCLEAN}/TOOLS/"

#TOOLDIR="$1"
# TODO: Input argument a list of strings (toolnames)
#TOOL="$2"

# TODO: Function that tests if already installed- Then update?


# Functional
#bash tools.sh "${TOOLDIR}" "ArgosTranslate fairseq fast_align GlotLID KLPT Morfessor NLLB OpusTools SacreBLEU Sockeye spaCy Stanza TextCleaning TranslateLocally Whisper"

#bash tools.sh "${TOOLDIR}" "ArgosTranslate"
#bash tools.sh "${TOOLDIR}" "fairseq" 
#bash tools.sh "${TOOLDIR}" "fast_align"
#bash tools.sh "${TOOLDIR}" "GlotLID"
#bash tools.sh "${TOOLDIR}" "KLPT"
#bash tools.sh "${TOOLDIR}" "Morfessor"
#bash tools.sh "${TOOLDIR}" "NLLB"
#bash tools.sh "${TOOLDIR}" "OpusTools"
#bash tools.sh "${TOOLDIR}" "SacreBLEU"
#bash tools.sh "${TOOLDIR}" "Sockeye"
#bash tools.sh "${TOOLDIR}" "spaCy"
#bash tools.sh "${TOOLDIR}" "Stanza"
#bash tools.sh "${TOOLDIR}" "TextCleaning"
#bash tools.sh "${TOOLDIR}" "TranslateLocally"
#bash tools.sh "${TOOLDIR}" "Whisper"

#bash tools.sh "${TOOLDIR}" ""


# TODO
#bash tools.sh "wikiextractor" "${TOOLDIR}"
#bash tools.sh "${TOOLDIR}" "MarianMT"
#bash tools.sh "${TOOLDIR}" "OpusMT" 
#bash tools.sh "${TOOLDIR}" "SentenceBERT" 
#bash tools.sh "${TOOLDIR}" "whisper" 
#bash tools.sh  "${TOOLDIR}""BARK" 
#bash tools.sh "${TOOLDIR}" "eSpeak" 


cd "$CURRENT"
