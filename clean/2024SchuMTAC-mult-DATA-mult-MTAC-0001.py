
# NOTE: Done this previously → Find script and incorporate to here!
#       Located in the TextAsCorpusRep repository: /media/CrazyProjects/LowResDialectology/MTACR/TextAsCorpusRep/scripts

# NOTE: Translators used different media and we ended up with various file formats

# TODO: View and incorporate the various annotation files accruet during the explorative phase of MTACR (i.e. Lazkin)
#       In directory: /previous_potato_annotations_to_be_sorted

###############################################################################
# Text cleaning of collected data


# → Output: A single json file with all the text data (annonymized)



###############################################################################
# Data statistics: For each language → for each dataset (flickr30k & NLLB) → how many annotations (unique and alternatives) → and also aggregated summaries



###############################################################################
# Text preprocessing of parallel data into training corpus splits

# → Input: A single json file with all the text data (annonymized) ← From "Text cleaning of collected data" above
# Temporarily found in "T00-eng-entire-aligned.json"

import json

# NOTE: Temp code until notes from top of this script have been resolved
src = "eng"
trg = "kob"
download_dir='/media/AllBlue/LanguageData/DOWNLOAD/projects/MTACR'
aggregated_file='T00-eng-entire-aligned.json'
aligned_text_file=f'{download_dir}/{aggregated_file}'
clean_dir='/media/AllBlue/LanguageData/CLEAN/projects/MTACR'
source_target_file=f'{clean_dir}/{src}-{trg}'

with open(aligned_text_file, 'r') as f:
    data = json.load(f)

src_trg_data = {}
for id in data.keys():
    if trg in data[id].keys():
        entry_eng = data[id][src]
        entry_kob = data[id][trg]
        src_trg_data[entry_eng] = entry_kob

json_object = json.dumps(src_trg_data, indent=4, ensure_ascii=False)
with open(f'{source_target_file}.json', "w") as outfile:
    outfile.write(json_object)

# → Output: Datasets for specified language pairs






