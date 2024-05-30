import bz2
import gzip
import xml.etree.ElementTree as ET
import json
import argparse

parser = argparse.ArgumentParser(description='Extract Wikidumps')
parser.add_argument('--code', type=str, help='language code to process')# "als"
parser.add_argument('--input-dir', type=str, help='input directory')    # /media/AllBlue/LanguageData/CLEAN/wikidumps/naive/als
parser.add_argument('--input-file', type=str, help='input file')        # als-info.json
parser.add_argument('--output-dir', type=str, help='output directory')  # /media/AllBlue/LanguageData/CLEAN/wikidumps/info
parser.add_argument('--output-file', type=str, help='output file')        # als-info.json

args = parser.parse_args()

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
    xml_file = f'{args.input_dir}/{args.input_file}'
    articles = extract_text_and_metadata(xml_file)

    with open(f'{args.output_dir}/{args.code}-info.json', 'w') as json_file:
        json.dump(articles, json_file, indent=4)

    # with open('output.txt', 'w', encoding='utf-8') as txt_file:
    #     for article in articles:
    #         txt_file.write(f"Title: {article['title']}\n")
    #         txt_file.write(f"Timestamp: {article['timestamp']}\n")
    #         txt_file.write(f"Text: {article['text']}\n\n")

if __name__ == "__main__":
    main()
