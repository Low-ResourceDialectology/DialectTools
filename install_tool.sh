#!/bin/bash
# Install a specific tool by name
# Use: bash install_tool.sh "spaCy"

CURRENT="$PWD"

TOOL="$1"

# Python packages inside default venv
source ./venvs/DialectTools/bin/activate

# TODO: VENV as argument
#VENV="$2"

# spaCy is a library for advanced Natural Language Processing in Python and Cython. 
# https://pypi.org/project/spacy/
if [ "${TOOL}" = "spaCy" ]; 
then
    echo "Installing spaCy"
    pip install -U pip setuptools wheel
    pip install -U 'spacy[cuda12x]'
    python -m spacy download zh_core_web_sm
    python -m spacy download en_core_web_sm
    python -m spacy download de_core_news_sm

# Language Identification with Support for More Than 2000 Labels
# https://github.com/cisnlp/GlotLID
elif [ "${TOOL}" = "GlotLID" ];
then
    echo "Installing GlotLID"
    pip install fasttext
    pip install huggingface_hub

# elif [ "${TOOL}" = "TOOL_NAME" ];
# then

# elif [ "${TOOL}" = "TOOL_NAME" ];
# then

# elif [ "${TOOL}" = "TOOL_NAME" ];
# then

# elif [ "${TOOL}" = "TOOL_NAME" ];
# then

# elif [ "${TOOL}" = "TOOL_NAME" ];
# then

fi



cd "$CURRENT"


