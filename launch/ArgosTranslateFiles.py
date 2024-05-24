# Author: Christian "Doofnase" Schuler
#######################################
# source /media/AllBlue/LanguageData/TOOLS/vArgosTranslate/bin/activate
# cd /media/CrazyProjects/LowResDialectology/DialectTools/launch
# python3 ArgosTranslateFiles.py --input_lang en --output_lang de --input_file /media/AllBlue/LanguageData/CLEAN/English/2022NLLBNLLB_devtest.engL --output_file /media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-engL-mult-deuL-NLLB-0001/2022NLLBNLLB-Argo.deuL

import argparse
import os
import shutil
current_working_directory = os.getcwd()

import argostranslate.package, argostranslate.translate
import argostranslatefiles
from argostranslatefiles import argostranslatefiles

parser = argparse.ArgumentParser(description='Machine Translation via NLLB')
parser.add_argument('--input_lang', type=str, help='input language code')
parser.add_argument('--input_file', type=str, help='input file')
parser.add_argument('--output_lang', type=str, help='output language code')
parser.add_argument('--output_file', type=str, help='output file')

args = parser.parse_args()

src_code = args.input_lang #"en"
trg_code = args.output_lang #"de"

tis_temp_name_nau_due_to_argos_not_liking_convenience_of_user = f'{args.input_file.replace(".","HOLYSHITSNACKS")}.txt'
shutil.copy(args.input_file, tis_temp_name_nau_due_to_argos_not_liking_convenience_of_user)

installed_languages = argostranslate.translate.get_installed_languages()
src_lang = list(filter(
    lambda x: x.code == src_code,
    installed_languages))[0]
trg_lang = list(filter(
    lambda x: x.code == trg_code,
    installed_languages))[0]
underlying_translation = src_lang.get_translation(trg_lang)

argostranslatefiles.translate_file(underlying_translation, os.path.abspath(tis_temp_name_nau_due_to_argos_not_liking_convenience_of_user))
translated_file_path = tis_temp_name_nau_due_to_argos_not_liking_convenience_of_user.replace('.',f'_{trg_code}.') # → Argos adds "_de" by default

os.rename(f'{translated_file_path}',f'{args.output_file}')
os.remove(tis_temp_name_nau_due_to_argos_not_liking_convenience_of_user)

