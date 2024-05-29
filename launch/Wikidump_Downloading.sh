#!/bin/bash

current_dir="$(dirname "$0")"

# TODO: Make the called script process a list of language codes
# bash "${current_dir}"/../download/wikipedia_dumps.sh -d /media/AllBlue/LanguageData -l als bar

for CODE in als bar; do
bash "${current_dir}"/../download/wikipedia_dumps.sh -d /media/AllBlue/LanguageData -l "${CODE}"
done
