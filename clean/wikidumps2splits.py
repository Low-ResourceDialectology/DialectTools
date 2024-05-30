# Splitting the Wikipedia dump file based on previously extracted dialect tags

import argparse
import glob
import json
import os
from collections import defaultdict

parser = argparse.ArgumentParser(description='Clean Wikidumps')
parser.add_argument('--code', type=str, help='language code to process')
parser.add_argument('--input-dir01', type=str, help='input directory')
parser.add_argument('--input-dir02', type=str, help='input directory')
parser.add_argument('--input-file', type=str, help='input file')
parser.add_argument('--input-file-freq', type=str, help='input file with dialect frequencies')
parser.add_argument('--output-dir', type=str, help='output directory')
parser.add_argument('--output-file', type=str, help='output file')
parser.add_argument('--sort-level', type=str, help='dialect level of sorting: 1=dialect, 2=subdialect, 3=subsubdialect')
parser.add_argument('--freq-dir', type=str, help='output directory for frequency dictionaries')

args = parser.parse_args()

# Read dialect information of articles previously extracted via /clean/wididumps2extract.py
def read_dialect_info_from_file(dialect_info_file):
    with open(dialect_info_file, 'r') as f:
        data = json.load(f)
        return data

# For all text files previously extracted via wikiextractor 
def process_wikiextractor_output(input_path_of_extracts, dialect_info, dialect_names, sort_level=1):
    read_files = glob.glob(f'{input_path_of_extracts}/*')

    # Structure for storing the split and sorted data
    out_data = {}
    if sort_level == 1:
        for key in dialect_names.keys():
            if not key in ['Dialektname auf Hochdeutsch (Link zum Artikel)', '<Link>', 'Wort:Verwaltungshauptargumente', 'VY OND GO,A ima te ']:
                out_data[key] = {}
    elif sort_level == 2:
        for key in dialect_names.keys():
            for sub_key in dialect_names[key]:
                out_data[f'{key}-{sub_key}'] = {}
    elif sort_level == 3: # May the gods show mercy upon your soul, if you ever come back to continue work on this level!
        for key in dialect_names.keys():
            for sub_key in dialect_names[key]:
                for sub_sub_key in dialect_names[key][sub_key]:
                    out_data[f'{key}-{sub_key}-{sub_sub_key}'] = {}
    else:
        print(f'Unexpected sorting behaviour!')
    out_data["UNKNOWN"] = {}
    print(f'Number of dialects for {args.code}: {len(out_data)}')
    print(f'Number of files extracted from dump for: {len(read_files)}')
    number_of_articles = 0
    for f in read_files:
        with open(f, "r") as infile:
            # Read all articles
            current_extract = infile.readlines() # Each line an article
            for article in current_extract:
                number_of_articles = number_of_articles + 1
                # art_id = article["id"]
                # art_revid = article["revid"]
                # art_url = article["url"]
                # art_title = article["title"]
                # art_text = article["text"]
                art_id = article.split('"id": "')[1].split('", "')[0]
                art_revid = article.split('"revid": "')[1].split('", "')[0]
                art_url = article.split('"url": "')[1].split('", "')[0]
                art_title = article.split('"title": "')[1].split('", "')[0]
                art_text = article.split('"text": "')[1].split('", "')[0]
                # Look up the corresponding dialect-info via "title" content
                if art_title in dialect_info.keys():
                    art_dialect = dialect_info[art_title]["dialect"]
                    art_subdialect = dialect_info[art_title]["subdialect"]
                    art_subsubdialect = dialect_info[art_title]["subsubdialect"]
                if sort_level == 1:
                    new_entry = {
                        "dialect":art_dialect,
                        "subdialect":art_subdialect,
                        "subsubdialect":art_subsubdialect,
                        "id":art_id,
                        "revid":art_revid,
                        "url":art_url,
                        "title":art_title,
                        "text":art_text
                    }
                    if art_dialect not in out_data.keys():
                        print(f'Why is this dialect missing?! {art_dialect}')
                    else:
                        if art_id in out_data[art_dialect].keys():
                            print(f'Duplicated Entry??:\n {new_entry}')
                        else:
                        #out_data[art_dialect][art_title] = {}
                            out_data[art_dialect][art_id] = new_entry
                elif sort_level == 2:
                    print(f'This second level of sorting has not been implemented yet.')
                elif sort_level == 3: 
                    print(f'This third level of sorting has not been implemented yet.')
    
    print(f'Number of articles from extracted files: {number_of_articles}')
    dialect_frequencies = {}
    # Safe in corresponding output file to create dialect-splits
    for dialect_key in out_data.keys():
        dialect_frequencies[dialect_key] = len(out_data[dialect_key])
        json_object = json.dumps(out_data[dialect_key], indent=4, ensure_ascii=False)
        with open(f'{args.output_dir}/{dialect_key}.json', "w") as outfile:
            outfile.write(json_object)
        
    # NOTE: Storing the frequency dictionary in the same directory is silly and crashes later scripts!
    json_object = json.dumps(dialect_frequencies, indent=4, ensure_ascii=False)
    with open(f'{args.freq_dir}/{args.output_file.replace(".json","-freq.json")}', "w") as outfile:
        outfile.write(json_object)


def main():
    dialect_info_file = f'{args.input_dir01}/{args.input_file}'
    dialect_info = read_dialect_info_from_file(dialect_info_file)

    dialect_names_file = f'{args.input_dir01}/{args.input_file_freq}'
    dialect_names = read_dialect_info_from_file(dialect_names_file)

    input_path_of_extracts = f'{args.input_dir02}'
    process_wikiextractor_output(input_path_of_extracts, dialect_info, dialect_names, int(args.sort_level))

if __name__ == "__main__":
    main()