# from sacremoses import MosesTokenizer, MosesDetokenizer

# mt, md = MosesTokenizer(lang='en'), MosesDetokenizer(lang='en')
# sent = "This ain't funny. It's actually hillarious, yet double Ls. | [] < > [ ] & You're gonna shake it off? Don't?"
# expected_tokens = ['This', 'ain', '&apos;t', 'funny', '.', 'It', '&apos;s', 'actually', 'hillarious', ',', 'yet', 'double', 'Ls', '.', '&#124;', '&#91;', '&#93;', '&lt;', '&gt;', '&#91;', '&#93;', '&amp;', 'You', '&apos;re', 'gonna', 'shake', 'it', 'off', '?', 'Don', '&apos;t', '?']
# expected_detokens = "This ain't funny. It's actually hillarious, yet double Ls. | [] < > [] & You're gonna shake it off? Don't?"
# mt.tokenize(sent) == expected_tokens


import os
import shutil
from sacremoses import MosesDetokenizer

def backup_file(file_path):
    """
    Creates a backup copy of the file.
    """
    backup_path = file_path + '.bak'
    shutil.copy(file_path, backup_path)
    return backup_path

def detokenize_file(file_path):
    """
    Detokenizes the contents of a file line-by-line.
    """
    # Create a detokenizer
    detokenizer = MosesDetokenizer()

    # Create a backup of the original file
    backup_file(file_path)

    # Read the contents of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Detokenize each line
    detokenized_lines = [detokenizer.detokenize(line.split()) for line in lines]

    # Write the detokenized content back to the original file
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in detokenized_lines:
            file.write(line + '\n')

def process_files(file_paths):
    """
    Processes multiple files by detokenizing them.
    """
    for file_path in file_paths:
        detokenize_file(file_path)
        print(f"Processed and detokenized: {file_path}")

# Example usage
files_to_process = [
    #"/media/AllBlue/LanguageData/PREP/opustools/bar-de/clean/test.de", # Reference Ger-
    #"/media/AllBlue/LanguageData/PREP/opustools/bar-de/clean/test.bar" # Reference Bar-
    #"/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/clean/reference/German/English/NLLB/test.en", # Reference Ger-Eng
    #"/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/clean/reference/Bavarian/English/NLLB/test.en" # Reference Bar-Eng
    
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/relaxed/mor/test.bar", # Perturbed Bar-Ger (relaxed)
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/reason/mor/test.bar", # Perturbed Bar-Ger (reason)
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/reason/lex/test.bar", # Perturbed Bar-Ger (reason)
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/guess/mor/test.bar" # Perturbed Bar-Ger (guess)

    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/relaxed/mor/test.de",
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/reason/mor/test.de",
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/reason/lex/test.de",
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/guess/mor/test.de"

    # "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/clean/German/relaxed/mor/English/NLLB/test.en",
    # "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/clean/German/reason/mor/English/NLLB/test.en",
    # "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/clean/German/reason/lex/English/NLLB/test.en",
    # "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/clean/German/guess/mor/English/NLLB/test.en"

    # NOTE: Prior to sending data to Sina
    # "/media/AllBlue/LanguageData/PREP/opustools/bar-en/clean/test.en", # Reference Ger-
    # "/media/AllBlue/LanguageData/PREP/opustools/bar-en/clean/test.bar" # Reference Bar-
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/reason/all/test.bar",
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/relaxed/all/test.bar"
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/reason/all/test.de",
    # "/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/relaxed/all/test.de"
    "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/clean/Bavarian/reason/lex/English/NLLB/test.en",
    "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/clean/Bavarian/reason/mor/English/NLLB/test.en",
    "/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/German/clean/Bavarian/relaxed/mor/English/NLLB/test.en"
    
    

]



process_files(files_to_process)


