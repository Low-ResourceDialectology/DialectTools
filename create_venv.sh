#!/bin/bash
# Automatical creation of virtual Python environments
# Use: bash create_venv.sh "myToolName"

CURRENT="$PWD"

TARGET="$1"

# Function to create Python venv
create_symlinks() {

    VENVNAME="$1"
    mkdir -p "$CURRENT/venvs"
    cd "$CURRENT/venvs"
    python3 -m venv ./"${VENVNAME}"
}

create_symlinks "${TARGET}"

cd "$CURRENT"
