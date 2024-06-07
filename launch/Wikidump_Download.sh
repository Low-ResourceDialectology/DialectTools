#!/bin/bash

current_dir="$(dirname "$0")"
DATE=20240501

echo "TODO: Make the script process a list of codes and not just a single one."
echo "TODO: Make use of the provided date argument to get specific dumps."
echo "TODO: Look into how to work on 'latest' as parameter for date, such as here: https://dumps.wikimedia.org/alswiki/latest/"
echo "Check if newer dumps are available and change the date inside the script: download/wikipedia_dumps.sh"

# TODO: Make the called script process a list of language codes
# bash "${current_dir}"/../download/wikipedia_dumps.sh -d /media/AllBlue/LanguageData -l als bar

for CODE in als bar ku ckb de; do
bash "${current_dir}"/../download/wikipedia_dumps.sh \
    -t /media/AllBlue/LanguageData \
    -l "${CODE}" \
    -d "${DATE}"
done
