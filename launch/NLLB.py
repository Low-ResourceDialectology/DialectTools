# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Translates a file of sentences (per line) and translates them from source into target language.
#   Input: 
#   Output: 

import argparse
import os
import csv 
import pathlib
import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# source /media/AllBlue/LanguageData/TOOLS/vNLLB/bin/activate
# python3 NLLB.py --input_lang eng_Latn --input_file /media/AllBlue/LanguageData/CLEAN/English/2022NLLBNLLB_devtest.engL --output_lang deu_Latn --output_file /media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh-engL-mult-deuL-NLLB-0001/2022NLLBNLLB-NLLB.deuL
# Newly added: --authorid 
# Newly added: --modelid

# NLLB Models on HuggingFace
# https://huggingface.co/facebook/nllb-200-3.3B
# https://huggingface.co/facebook/nllb-200-1.3B
# https://huggingface.co/facebook/nllb-200-distilled-1.3B
# https://huggingface.co/facebook/nllb-200-distilled-600M

parser = argparse.ArgumentParser(description='Machine Translation via NLLB')
parser.add_argument('--input_code', type=str, help='input language code')
parser.add_argument('--input_file', type=str, help='input file')
parser.add_argument('--output_code', type=str, help='output language code')
parser.add_argument('--output_file', type=str, help='output file')
parser.add_argument('--authorid', type=str, help='author on huggingface', default='facebook')
parser.add_argument('--modelid', type=str, help='model on huggingface', default='nllb-200-distilled-600M')
parser.add_argument("--chunk_size", type=int, default=100, help="Number of sentences to process at a time")

args = parser.parse_args()

#print(f'Args: {args}') # Debugginng
#sys.exit() # Debugginng
""" Check whether directory already exists and create if not """
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

dir_maker(os.path.dirname(args.output_file))

""" Get Tokenizer from HuggingFace """
def get_tokenizer(hugging_tokenizer="facebook/nllb-200-distilled-600M", local_cache_dir='/media/AllBlue/LanguageData/MODELS/HuggingFace/'):
    tokenizer = AutoTokenizer.from_pretrained(hugging_tokenizer, cache_dir=local_cache_dir)
    return tokenizer

""" Get Model from HuggingFace """
def get_model(hugging_model="facebook/nllb-200-distilled-600M", local_cache_dir='/media/AllBlue/LanguageData/MODELS/HuggingFace/'):
    model = AutoModelForSeq2SeqLM.from_pretrained(hugging_model, cache_dir=local_cache_dir).cuda()
    return model

tokenizer = get_tokenizer(hugging_tokenizer=f'{args.authorid}/{args.modelid}')
model = get_model(hugging_model=f'{args.authorid}/{args.modelid}')
model.device

""" Create a translator for language pair"""
def get_translator(model, tokenizer, source_lang, target_lang, max_len=400, number_beams=3, early_stop=True):
    new_translator = pipeline('translation', 
                          model=model, 
                          tokenizer=tokenizer, 
                          src_lang=source_lang, # e.g. 'kmr_Latn'
                          tgt_lang=target_lang, # e.g. 'eng_Latn'
                          device=model.device, 
                          max_length=max_len, 
                          num_beams=number_beams, 
                          early_stopping=early_stop)
    return new_translator

""" List of languages to process """
#language_list = ["Northern Kurdish", "Kobani", "German", "Alemannic", "Bavarian", "Central Kurdish"]
#language_list = ["deu", "als", "bar"]

#source_lang = args.input_code #"deu_Latn"
#target_lang = args.output_code #"eng_Latn"
translator_src2trg = get_translator(model, tokenizer, args.input_code, args.output_code)

""" Function to translate a single file from source to target language """
def translate_file():
    # Check if it is a file
        if os.path.isfile(args.input_file):
            print(f'Translating: {args.input_file}')
            # NOTE: Include check if file already has been translated?
            if os.path.isfile(args.output_file):
                print(f'Translated output file detected, skipping this for the time being.')
            else:
                with open(args.input_file, "r") as f:
                    text = f.read().splitlines()

                    # Print length of input file
                    print(f'Input ({args.input_code}) length: {len(text)}')

                    trans_text = translator_src2trg(text)
                    translated_text = [i["translation_text"] for i in trans_text]

                    # Print length of translation
                    print(f'Output ({args.output_code}) length: {len(translated_text)}')

                    # Save the translation to file
                    with open(args.output_file, "w") as f:
                        f.write("\n".join(translated_text))


""" Function to translate a single file from source to target language chunk-wise to not lose progress when CUDA runs out of memory"""
def translate_in_chunks(input_file, output_file, source_lang, target_lang, chunk_size=100):
    with open(input_file, "r") as f:
        text = f.read().splitlines()

    # Print length of input file
    print(f'Input ({source_lang}) length: {len(text)}')

    with open(output_file, "w") as f:
        #for i in range(0, len(text), chunk_size):
        #for i in range(8300, len(text), chunk_size):
        for i in range(8200, 8250, chunk_size):
            chunk = text[i:i + chunk_size]
            trans_text = translator_src2trg(chunk, src_lang=source_lang, tgt_lang=target_lang)
            translated_text = [i["translation_text"] for i in trans_text]

            # Print progress
            print(f'Translated {min(i + chunk_size, len(text))} of {len(text)} sentences')

            # Save the translation to file
            f.write("\n".join(translated_text) + "\n")

    # Print length of translation
    print(f'Output ({target_lang}) length: {len(text)}')



""" Clunky Version that loses it' shit, once it crashes! """
#translate_file()

""" Deluxe Version that regularly thinks about backups! """
translate_in_chunks(args.input_file, args.output_file, args.input_code, args.output_code, args.chunk_size)

# Fine-Tune?
