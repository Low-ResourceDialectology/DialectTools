# Author: Christian "Doofnase" Schuler
#######################################
# Use: python3 Stanza.py --language-names kmr de en

import argparse
import os
import stanza
current_working_directory = os.getcwd()
data_root_dir = '/media/AllBlue/LanguageData'

# Define a custom argument type for a list of strings
def list_of_strings(arg):
    return arg.split(',')

parser = argparse.ArgumentParser(description='Stanza setup prior first launch')
parser.add_argument('--language-names', type=list_of_strings, help='language names of which models should be downloaded.', default="en")
parser.add_argument('--cache-dir', type=str, help='directory to store downloaded models.', default=f'{data_root_dir}/MODELS/Stanza')
parser.add_argument('--verbosity', type=bool, help='how much info is printed to console.', default=True)

args = parser.parse_args()

print(f'Input languages: {args.language_names}')
print(f'Cache directory: {args.cache_dir}')

"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print("Folder %s created!" % path)
    else:
        print("Folder %s already exists" % path)

""" Download stanzas models for each language """
def download_stanza_models(language_list, cache_dir, verbosity):
	dir_maker(cache_dir)
	for language in language_list:
		print(f'Download models for {language}')
		stanza.download(lang=language, model_dir=cache_dir, verbose=verbosity)

download_stanza_models(args.language_names, args.cache_dir, args.verbosity)
