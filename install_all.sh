#!/bin/bash
# Install all tools
# Use: bash install_all.sh

CURRENT="$PWD"

mkdir -p "$CURRENT/tools"

bash install_tool.sh "spaCy"
bash install_tool.sh "GlotLID"



cd "$CURRENT"
