
import json
import argparse

parser = argparse.ArgumentParser(description='Clean Wikidumps')
parser.add_argument('--code', type=str, help='language code to process')# "als"
parser.add_argument('--input-dir', type=str, help='input directory')    # /media/AllBlue/LanguageData/CLEAN/wikidumps/naive/als
parser.add_argument('--input-file', type=str, help='input file')        # als-info.json
parser.add_argument('--output-dir', type=str, help='output directory')  # /media/AllBlue/LanguageData/CLEAN/wikidumps/info
parser.add_argument('--output-file', type=str, help='output file')        # als-info.json

args = parser.parse_args()

out_data = {}
# Read wikidump info from json file
with open(f'{args.input_dir}/{args.input_file}', 'r') as f:
    data = json.load(f)

# Walk through article information to collect dialect information

# NOTE: Because everyone and their uncle is allowed to randomly shit into te bucket called wikipedia, there is no logic to any of it!
#       We could have had a simple "language_variety_tag" for each article and be done with it- but oh no! That would be too conveniant!

if args.code == "als":
    # Process Alemannic wikidump structure
    pass
elif args.code == "bar":
    # Process Bavarian wikidump structure
    pass

# Write collected info to file
json_object = json.dumps(out_data, indent=4, ensure_ascii=False)
with open(f'{args.output_dir}/{args.output_file}', "w") as outfile:
    outfile.write(json_object)



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

def main():
    xml_file = f'{args.input_dir}/{file_name}'
    articles = extract_text_and_metadata(xml_file)

    with open(f'{args.output_dir}/{args.code}-info.json', 'w') as json_file:
        json.dump(articles, json_file, indent=4)

    # with open(f'{args.output_dir}/{args.code}-wikidumppreprocessing.txt', 'w', encoding='utf-8') as txt_file:
    #     for article in articles:
    #         txt_file.write(f"Title: {article['title']}\n")
    #         txt_file.write(f"Timestamp: {article['timestamp']}\n")
    #         txt_file.write(f"Text: {article['text']}\n\n")

if __name__ == "__main__":
    main()