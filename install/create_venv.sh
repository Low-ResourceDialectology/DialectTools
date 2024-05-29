#!/bin/bash
# Automatic creation of virtual Python environments
# Use: bash create_venv.sh "myToolName" "myToolDirectory"

CURRENT="$PWD"

TOOLNAME="$1"
TOOLDIRECTORY="$2"

# Function to create Python venv
create_venv() {
    VENVNAME="$1"
    DIRNAME="$2"
    mkdir -p "${DIRNAME}"
    cd "${DIRNAME}"
    python3 -m venv ./"v${VENVNAME}"
}

create_venv "${TOOLNAME}" "${TOOLDIRECTORY}"

cd "$CURRENT"
