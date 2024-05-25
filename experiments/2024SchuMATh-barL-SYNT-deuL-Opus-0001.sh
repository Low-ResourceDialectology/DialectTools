#!/bin/bash
# Turning Bavarian into German text

SOURCE="bar"
TARGET="de"
#TARGET="en"

EXPDIR="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-barL-SYNT-mult-Opus-0001/Perturbed"
mkdir "${EXPDIR}" -p

python3 /media/CrazyProjects/LowResDialectology/DialectTools/perturb/development-synth-barL-deuL.py







