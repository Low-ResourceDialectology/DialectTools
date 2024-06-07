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

""" Memory-friendly script to prevent crashing during processing the German wikidump """
def extract_text_and_metadata_memory_friendy_fail(xml_file, out_file):
    article_counter = 0
    with open(out_file, 'w') as temp_txt_file:
        with bz2.open(xml_file, 'rb') as open_xml:
            #for event, elem in ET.iterparse(open_xml, events=('start', 'end')):
            tree = ET.iterparse(open_xml, events=('start', 'end'))
            article_lines = ""
            for event, elem in tree:
                if event == 'start' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
                    article_lines = ""
                #elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}revid':
                #    revid = elem.text
                elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
                    title = elem.text
                elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}timestamp':
                    timestamp = elem.text
                elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text':
                    text = elem.text
                    article_lines = f'{{"title": "{title}", "timestamp": "{timestamp}", "text": "{text}"}}'
                    #article_lines = f'"{revid}":{{"title": "{title}", "timestamp": "{timestamp}", "text": "{text}"}}' # TODO: How to find the revid??? 
                    article_counter = article_counter + 1
                    if (article_counter%10000 == 0):
                        print(article_counter)
                
                # Write current article to file
                temp_txt_file.write(article_lines)    
                # Clear the element to free memory
                elem.clear()
                
                # if event == 'end' and elem.tag == 'page':
                #     # Process the 'page' element here
                #     revid = elem.findtext('revid')
                #     title = elem.findtext('title')
                #     timestamp  = elem.findtext('timestamp')
                #     text = elem.find('revision').findtext('text')
                #     article_lines = f'"{revid}":{{"title": "{title}", "timestamp": "{timestamp}", "text": "{text}"}}'
                #     #temp_txt_file.write(" ".join(article_lines))
                #     temp_txt_file.write(article_lines)
                    
                #     # Clear the element to free memory
                #     elem.clear()


""" Memory-friendly script to prevent crashing during processing the German wikidump """
def extract_text_and_metadata_memory_friendy_fail2(xml_file):
    article_counter = 1
    file_counter = 0
    articles = []
    with bz2.open(xml_file, 'rb') as f:
        tree = ET.iterparse(f, events=('start', 'end'))
        article = {}
        for event, elem in tree:
            if event == 'start' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
                article = {}
            #elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}revid':
                #article['revid'] = elem.text
            elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
                article['title'] = elem.text
            elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}timestamp':
                article['timestamp'] = elem.text
            elif event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text':
                article['text'] = elem.text
                articles.append(article)
                # Clear the element to free memory
                elem.clear()
                article_counter = article_counter + 1
                if (article_counter%50000 == 0):
                    print(article_counter)
                if (len(articles) == 100000):
                    file_counter = file_counter + 1
                    with open(f'{args.output_dir}/{args.code}-info-{str(file_counter)}.json', 'w', encoding='utf-8') as json_file:
                        json.dump(articles, json_file, indent=4, ensure_ascii=False)
                    articles = []
    file_counter = file_counter + 1
    with open(f'{args.output_dir}/{args.code}-info-{str(file_counter)}.json', 'w', encoding='utf-8') as json_file:
        json.dump(articles, json_file, indent=4, ensure_ascii=False)



def main():
    xml_file = f'{args.input_dir}/{args.input_file}'
    
    # NOTE: This function suffices for smaller wikidumps such as Alemannic or Bavarians
    # articles = extract_text_and_metadata(xml_file)

    # with open(f'{args.output_dir}/{args.code}-info.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(articles, json_file, indent=4, ensure_ascii=False)


    # NOTE: This approach aims to manage larger wikidumps such as German
    extract_text_and_metadata_memory_friendy_fail2(xml_file)
    #with open(f'{args.output_dir}/{args.code}-info.json', 'w', encoding='utf-8') as json_file:
    #    json.dump(articles, json_file, indent=4, ensure_ascii=False)

    # NOTE: Below code for an approach in case the text content is too much to be read in one go
    """
    with open(f'{args.output_dir}/{args.code}-info.json', 'w', encoding='utf-8') as json_file:
        articles = {}
        with open(f'{args.output_dir}/{args.code}-TEMP.txt', 'r') as temp_text_file:
            text_content = temp_text_file.readlines()
            # TODO: Add text_content line-by-line to the articles dict
        json.dump(articles, json_file, indent=4, ensure_ascii=False)
    """


if __name__ == "__main__":
    main()
