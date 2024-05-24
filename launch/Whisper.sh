#!/bin/bash
# Transcribe audio files
# bash Whisper.sh "/media/CrazyProjects/Tools/FROM_GLORY_TO_GOO.mp3" "/media/CrazyProjects/Tools/"

# Whisper → https://github.com/openai/whisper
source /media/AllBlue/LanguageData/TOOLS/vWhisper/bin/activate

INFILE="${1}"
OUTDIR="${2}"
#"2022NLLBNLLB-Argo.deuL"
#"2022NLLBNLLB-Goog.deuL"
#"2022NLLBNLLB-NLLB.deuL"

echo "Supported formats of Whisper are: .flac, .mp3, .wav"
whisper "${INFILE}" --model large-v3 --language Spanish --task translate --output_dir "${OUTDIR}"

