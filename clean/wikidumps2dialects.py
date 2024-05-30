# Extracting the dialect tags from wikipedia dump files and creating a frequency dictionary for each language

import bz2
import gzip
import xml.etree.ElementTree as ET
import json
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Clean Wikidumps')
parser.add_argument('--code', type=str, help='language code to process')# "als"
parser.add_argument('--input-dir', type=str, help='input directory')    # /media/AllBlue/LanguageData/CLEAN/wikidumps/naive/als
parser.add_argument('--input-file', type=str, help='input file')        # als-info.json
parser.add_argument('--output-dir', type=str, help='output directory')  # /media/AllBlue/LanguageData/CLEAN/wikidumps/info
parser.add_argument('--output-file', type=str, help='output file')        # als-info.json

args = parser.parse_args()

# Read wikidump file and create dict structure based on articles
def extract_text_and_metadata(xml_file):
    articles = []
    with bz2.open(xml_file, 'rb') as f:
        tree = ET.iterparse(f, events=('start', 'end'))
        article = {}
        for event, elem in tree:
            if event == 'start' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
                article = {}
            elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
                article['title'] = elem.text
            elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}timestamp':
                article['timestamp'] = elem.text
            elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text':
                article['text'] = elem.text
                articles.append(article)
    return articles

# Function to add or update entries in the dialect_info dictionary
def add_dialect_entry(dialect_info, dialect, dialect_sub, dialect_sub_sub):
    dialect_info[dialect][dialect_sub][dialect_sub_sub] += 1

# Walk through article information to collect dialect information
def check_for_dialect_info(articles):
    out_data = {}
    # Initialize the overall information dictionary with default dictionary of dictionaries
    dialect_info = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    # dialect_info = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))) # ???
    #dialect_info = {}
    empty_counter = 0
    empty_text = 0
    problem_counter = 0
    print(f'Number of {args.code} article entries: {len(articles)}')

    # NOTE: Because everyone and their uncle is allowed to randomly shit into te bucket called wikipedia, there is no logic to any of it!
    #       We could have had a simple "language_variety_tag" for each article and be done with it- but oh no! That would be too conveniant!
    if args.code == "als":
        # Process Alemannic wikidump structure
        for article in articles:
            if (len(article) > 0):
                if ("text" in article) and not (type(article["text"]) == type(None)):
                    art_text = article["text"]
                    dialect_info_top = ""
                    if '{{Dialekt|' in art_text:
                        #dialect_info_top = "Dialekt|" + art_text.split('{{Dialekt|')[1].split('}}')[0]
                        dialect_info_top = art_text.split('{{Dialekt|')[1].split('}}')[0]
                        dialect_splits = dialect_info_top.split('|')
                        if len(dialect_splits) == 3:
                            dialect = dialect_splits[0]
                            dialect_sub = dialect_splits[1]
                            dialect_sub_sub = dialect_splits[2]
                        elif len(dialect_splits) == 2:
                            dialect = dialect_splits[0]
                            dialect_sub = dialect_splits[1]
                            dialect_sub_sub = "UNKNOWN"
                        elif len(dialect_splits) == 1:
                            dialect = dialect_splits[0]
                            dialect_sub = "UNKNOWN"
                            dialect_sub_sub = "UNKNOWN"
                        else:
                            print(f"Unexpected number of splits in dialect-information tag found:\n{dialect_info_top}")
                            dialect = "UNKNOWN"
                            dialect_sub = "UNKNOWN"
                            dialect_sub_sub = "UNKNOWN"
                        # Exactly three articles inside the Alemannic Wikipedia do not have 3, but 2 dialect tags in this structure... Of course...
                        # if '|' in dialect_info_top.split('|')[1]:
                        #     dialect_sub = dialect_info_top.split('|')[1].split('|')[0]
                        #     dialect_sub_sub = dialect_info_top.split('|')[1].split('|')[1]
                        # else:
                        #     dialect_sub = dialect_info_top.split('|')[1]
                        #     dialect_sub_sub = "UNKNOWN"
                        
                        #dialect_entry = {dialect: {dialect_sub: dialect_sub_sub}}
                        #if dialect_entry in dialect_info.keys()
                        add_dialect_entry(dialect_info, dialect, dialect_sub, dialect_sub_sub)
                    # Dialect-Information of untagged articles
                    else:
                        dialect = "UNKNOWN"
                        dialect_sub = "UNKNOWN"
                        dialect_sub_sub = "UNKNOWN"
                         
                    # dialect_info_bot = ""
                    # if '[[Kategorie:' in art_text:
                    #     dialect_info_bot = art_text.split('[[Kategorie:')[1]
                    new_entry = {
                        "timestamp":article["timestamp"],
                        "dialect":dialect,
                        "subdialect":dialect_sub,
                        "subsubdialect":dialect_sub_sub,
                        #"text":article["text"] # NOTE: Not like this, since it first has to be cleaned (e.g. Template-Expansion)
                        #"dialect-info-top":dialect_info_top,
                        #"dialect-info-bot":dialect_info_bot
                    }
                    out_data[article["title"]] = new_entry
                else:
                    empty_text = empty_text + 1
            else:
                empty_counter = empty_counter + 1
        print(f'Empty Articles: {empty_counter}')
        print(f'Empty Text: {empty_text}')
        print(f'Problem Articles: {problem_counter}')
        return out_data, dialect_info



    elif args.code == "bar":
        # Process Bavarian wikidump structure
        for article in articles:
            if (len(article) > 0):
                if ("text" in article) and not (type(article["text"]) == type(None)):
                    art_text = article["text"]
                    dialect_info_top = ""
                    if '{{Dialekt-oben|' in art_text:
                        #dialect_info_top = "Dialekt|" + art_text.split('{{Dialekt|')[1].split('}}')[0]
                        dialect_info_top = art_text.split('{{Dialekt-oben|')[1].split('}}')[0].replace('\n','')
                        dialect_splits = dialect_info_top.split('|')
                        if len(dialect_splits) == 3:
                            dialect = dialect_splits[0]
                            dialect_sub = dialect_splits[1]
                            dialect_sub_sub = dialect_splits[2]
                        elif len(dialect_splits) == 2:
                            dialect = dialect_splits[0]
                            dialect_sub = dialect_splits[1]
                            dialect_sub_sub = "UNKNOWN"
                        elif len(dialect_splits) == 1:
                            dialect = dialect_splits[0]
                            dialect_sub = "UNKNOWN"
                            dialect_sub_sub = "UNKNOWN"
                        else:
                            print("Unexpected number of splits in dialect-information tag found.")
                            dialect = "UNKNOWN"
                            dialect_sub = "UNKNOWN"
                            dialect_sub_sub = "UNKNOWN"
                        # Exactly three articles inside the Alemannic Wikipedia do not have 3, but 2 dialect tags in this structure... Of course...
                        # if '|' in dialect_info_top.split('|')[1]:
                        #     dialect_sub = dialect_info_top.split('|')[1].split('|')[0]
                        #     dialect_sub_sub = dialect_info_top.split('|')[1].split('|')[1]
                        # else:
                        #     dialect_sub = dialect_info_top.split('|')[1]
                        #     dialect_sub_sub = "UNKNOWN"
                        
                        #dialect_entry = {dialect: {dialect_sub: dialect_sub_sub}}
                        #if dialect_entry in dialect_info.keys()
                        add_dialect_entry(dialect_info, dialect, dialect_sub, dialect_sub_sub)
                    # Dialect-Information of untagged articles
                    else:
                        dialect = "UNKNOWN"
                        dialect_sub = "UNKNOWN"
                        dialect_sub_sub = "UNKNOWN"
                         
                    # dialect_info_bot = ""
                    # if '[[Kategorie:' in art_text:
                    #     dialect_info_bot = art_text.split('[[Kategorie:')[1]
                    new_entry = {
                        "timestamp":article["timestamp"],
                        "dialect":dialect,
                        "subdialect":dialect_sub,
                        "subsubdialect":dialect_sub_sub,
                        #"text":article["text"] # NOTE: Not like this, since it first has to be cleaned (e.g. Template-Expansion)
                        #"dialect-info-top":dialect_info_top,
                        #"dialect-info-bot":dialect_info_bot
                    }
                    out_data[article["title"]] = new_entry
                else:
                    empty_text = empty_text + 1
            else:
                empty_counter = empty_counter + 1
        print(f'Empty Articles: {empty_counter}')
        print(f'Empty Text: {empty_text}')
        print(f'Problem Articles: {problem_counter}')
        return out_data, dialect_info

    




def main():
    xml_file = f'{args.input_dir}/{args.input_file}'
    articles = extract_text_and_metadata(xml_file)

    out_data, dialect_info = check_for_dialect_info(articles)

    # Write collected info to file
    json_object = json.dumps(out_data, indent=4, ensure_ascii=False)
    with open(f'{args.output_dir}/{args.output_file}', "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(dialect_info, indent=4, ensure_ascii=False)
    with open(f'{args.output_dir}/{args.output_file}-freq', "w") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":
    main()