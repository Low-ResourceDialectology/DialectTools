
# Text preprocessing of parallel data into training corpus splits

import pandas as pd
import seaborn as sns
import glob
import re
import math
import pathlib
from collections import Counter
import langid
import numpy as np
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

# TODO: Input arguments for more versatility
src_l = 'ku'
trg_l = 'de'
TARGET = "deu"
date_of_experiment = '20240525'
clean_dir = f'/media/AllBlue/LanguageData/CLEAN/opustools/{src_l}-{trg_l}'
prep_dir = f'/media/AllBlue/LanguageData/PREP/opustools/{src_l}-{trg_l}/{date_of_experiment}'
prep_dir_kmr = f'{prep_dir}/kmr-{TARGET}'
prep_dir_ckb = f'{prep_dir}/ckb-{TARGET}'

""" Check whether directory already exists and create if not """
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

dir_maker(prep_dir)
dir_maker(prep_dir_kmr)
dir_maker(prep_dir_ckb)

# Get all files based on language
src_files = glob.glob(f'{clean_dir}/*.{src_l}')
trg_files = glob.glob(f'{clean_dir}/*.{trg_l}')

#print(src_files)
#print(trg_files)


# Reorder parallel files

src_files_reordered = sorted(src_files)
trg_files_reordered = sorted(trg_files)

#print(src_files_reordered)
#print(trg_files_reordered)


# Read files into list as lines
src_lines = []

for file in src_files_reordered:
    with open(file) as f:
        for line in f.readlines():
            src_lines.append(line.rstrip(" \n"))
            
trg_lines = []

for file in trg_files_reordered:
    with open(file) as f:
        for line in f.readlines():
            trg_lines.append(line.rstrip(" \n"))

# Check no. of lines
print("Source Parallel Lines (naive): ", len(src_lines))
print("Target Parallel Lines (naive): ", len(trg_lines))
"""
Source Parallel Lines (naive):  224251
Target Parallel Lines (naive):  224251 
"""


#print("Some Example Parallel Lines (naive): ")
print(src_lines[100:105])
print(trg_lines[100:105])
"""
Some Example Parallel Lines: 
['panela pelrêçan', 'qada xêzkirinê', 'bijarkerê pelan', 'tijeker', 'hilbijêrê curetîpan']
['Verzeichnisleiste', 'Zeichenfeld', 'Dateiwähler', 'Füller', 'Schriftwähler']
"""


# Remove duplicates (source and target side being the same line of text)
# for line in src_lines:
#     if line in trg_lines:
#         src_lines.remove(line)
#         trg_lines.remove(line)
# #Check no. of lines again
# print("Source Parallel Lines (removed src=trg): ", len(src_lines))
# print("Target Parallel Lines (removed src=trg): ", len(trg_lines))
# """
# Source Parallel Lines (removed src=trg):  90129
# Target Parallel Lines (removed src=trg):  90129
# """

#print("Some Example Parallel Lines (removed src=trg): ")
#print(src_lines[100:105])
#print(trg_lines[100:105])
"""
Some Example Parallel Lines (removed src=trg): 
['Eine Auswahl von Arbeiten aus dem Wettbewerb « ... » .', 'An Heiland ( Salvator Mundi ) gibts aa in ondan Religionen .', 'Und darin soll ich Dein Ebenbild sein ?', '( Aserbaidschanisch : Aserbaidschanische Demokratische Republik .', 'Was die Standbesitzer am liebsten kochen .']
['Eine Auswahl von Arbeiten aus dem Wettbewerb « … » .', 'Ihm solle vielmehr im Himmel Göttlichkeit zuteilwerden .', 'Und darin soll ich Dein Ebenbild sein ?', '( Aserbaidschanisch : Aserbaidschanische Demokratische Republik .', 'Was die Standbesitzer am liebsten kochen .']
"""


# transform lists of lines into dataframe

df = pd.DataFrame(src_lines, columns = [src_l])
df[trg_l] = trg_lines
print(df.head())
"""
                        ku                  de
0                    GNOME               GNOME
1  Dirba GNOME ya standard  GNOME-Vorgabethema
2                    GNOME               GNOME
3  Dirba GNOME ya standard  GNOME-Vorgabethema
4                    GNOME               GNOME
"""


# text preprocessing
def preprocess(text):
    # NOTE: Leave this step for later to check for nouns and such
    #text = str(text).lower()
    
    # remove parenthesized texts
    text = re.sub(r"\(.*?\)", "", text)
    
    # remove brackets
    text = re.sub(r"\[.*?\]", "", text)

    # remove quotation marks
    text = re.sub(r'(\<|\>|"|“|”|„|»|«)*', "", text)

    # remove http websites
    text = re.sub(r"(https?:\/\/)[a-zA-Z1-9_.@?=#\/*]*", "", text)

    # remove other symbols
    text = re.sub(r"(\*|\+|@|#|:|;)*", "", text)
    
    # remove parenthesis again
    text = text.replace("(", "").replace(")", "")

    # trim extra whitespace
    text = re.sub(r' {2,100}', "", text)

    return text

df[src_l] = df[src_l].apply(preprocess)
df[trg_l] = df[trg_l].apply(preprocess)


# TODO: Different approach to truncating long lines than here → Orient on ratio between src_length and trg_length
# plot length of lines
#sns.set_theme(style = "whitegrid")
#sns.set(rc = {'figure.figsize':(7, 11)})
#%config InlineBackend.figure_format = 'retina'
#ax = sns.boxplot(y = "letters", data = df)

# smart truncate sentences so that sentences are not too long
# https://stackoverflow.com/questions/250357/truncate-a-string-without-ending-in-the-middle-of-a-word

def smart_truncate(content, length = 120, suffix = '.'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix

# TODO: Better truncating to find treasures in very long text lines?
#print(f'Length Dataframe (pre-smart truncate): {len(df)}')
#df[src_l] = df[src_l].apply(smart_truncate)
#df[trg_l] = df[trg_l].apply(smart_truncate)
#df[src_l] = df[src_l].apply(smart_truncate, result_type='expand')
df[src_l] = df[src_l].apply(smart_truncate)
df[trg_l] = df[trg_l].apply(smart_truncate)
print(f'Length Dataframe (post-smart truncate): {len(df)}')

# determine length of lines
def count_letters(text):
    return len(text)

df["letters"] = df[src_l].apply(count_letters)
"""
Length Dataframe (post-smart truncate): 452085
"""



# Lazy bums declaring everything to be "ku" instead of figuring out which data is "kmr" and which "ckb"...

# Function to detect if a string contains Arabic script characters
def is_arabic_script(text):
    arabic_characters = set("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
    for char in text:
        if char in arabic_characters:
            return True
    return False

# Function to classify Kurdish text into Kurmanji (Latin script) or Sorani (Arabic script)
def classify_kurdish_script(text):
    if is_arabic_script(text):
        return 'Sorani'
    else:
        return 'Kurmanji'

# Split the dataframe based on script detection
# Create a boolean mask where the condition is met
#mask_kmr = (df[df[src_l].apply(classify_kurdish_script) == 'Kurmanji'])
#mask_ckb = (df[df[src_l].apply(classify_kurdish_script) == 'Sorani'])
# Apply the mask to the DataFrame to get the rows where the condition is true
#df_kmr = df[mask_kmr]
#df_ckb = df[mask_ckb]

df_kmr = df[df[src_l].apply(classify_kurdish_script) == 'Kurmanji']
df_ckb = df[df[src_l].apply(classify_kurdish_script) == 'Sorani']




# Remove duplicates and empty lines

df_kmr = df_kmr.dropna()
print(f'Length df_kmr (dropped na): {len(df_kmr)}')
df_ckb = df_ckb.dropna()
print(f'Length df_ckb (dropped na): {len(df_ckb)}')

df_kmr = df_kmr.drop_duplicates(subset = [src_l, trg_l])
print(f'Length df_kmr (dropped duplicates (multiple same source sentence)): {len(df_kmr)}')
df_ckb = df_ckb.drop_duplicates(subset = [src_l, trg_l])
print(f'Length df_ckb (dropped duplicates (multiple same source sentence)): {len(df_ckb)}')

df_kmr_other = df_kmr[(df_kmr[src_l].str.lower() == df_kmr[trg_l].str.lower())]
df_kmr = df_kmr[(df_kmr[src_l].str.lower() != df_kmr[trg_l].str.lower())]
print(f'Length df_kmr (dropped duplicate (source same as target sentence)): {len(df_kmr)}')
df_ckb_other = df_ckb[(df_ckb[src_l].str.lower() == df_ckb[trg_l].str.lower())]
df_ckb = df_ckb[(df_ckb[src_l].str.lower() != df_ckb[trg_l].str.lower())]
print(f'Length df_ckb (dropped duplicate (source same as target sentence)): {len(df_ckb)}')

# Compare length of sentences to reasonably exclude inproportionately sized 'alignment-pairs'

# TODO: Introduce a minimum length criteria to keep alignments where i.e. 1 word fits 2 words
# df[trg_l].str.len() > 5 & ....

# Create a boolean mask where the condition is met
mask = (df_kmr[src_l].str.len() > 2 * df_kmr[trg_l].str.len()) | (df_kmr[src_l].str.len() * 2 < df_kmr[trg_l].str.len())
# Apply the mask to the DataFrame to get the rows where the condition is true
df_kmr_ratio = df_kmr[mask]
mask = (df_ckb[src_l].str.len() > 2 * df_ckb[trg_l].str.len()) | (df_ckb[src_l].str.len() * 2 < df_ckb[trg_l].str.len())
df_ckb_ratio = df_ckb[mask]

mask = (df_kmr[src_l].str.len() < 2 * df_kmr[trg_l].str.len()) & (df_kmr[src_l].str.len() * 2 > df_kmr[trg_l].str.len())
df_kmr = df_kmr[mask]
mask = (df_ckb[src_l].str.len() < 2 * df_ckb[trg_l].str.len()) & (df_ckb[src_l].str.len() * 2 > df_ckb[trg_l].str.len())
df_ckb = df_ckb[mask]

print(f'Length df_kmr (dropped inproportionate length differences (source/target 2 times as long as target/source)): {len(df_kmr)}')
print(f'Length df_ckb (dropped inproportionate length differences (source/target 2 times as long as target/source)): {len(df_ckb)}')
"""
Length df_kmr (dropped na): 289099
Length df_ckb (dropped na): 162986
Length df_kmr (dropped duplicates (multiple same source sentence)): 200830
Length df_ckb (dropped duplicates (multiple same source sentence)): 154620
Length df_kmr (dropped duplicate (source same as target sentence)): 194805
Length df_ckb (dropped duplicate (source same as target sentence)): 154617
Length df_kmr (dropped inproportionate length differences (source/target 2 times as long as target/source)): 163188
Length df_ckb (dropped inproportionate length differences (source/target 2 times as long as target/source)): 143698
"""

# Write the entries excluded in the last two steps to file
with open(f'{prep_dir_kmr}/{src_l}-other','w') as file:
    for line in df_kmr_other[src_l]:
        file.write(line + "\n")
with open(f'{prep_dir_kmr}/{trg_l}-other','w') as file:
    for line in df_kmr_other[trg_l]:
        file.write(line + "\n")

with open(f'{prep_dir_kmr}/{src_l}-ratio','w') as file:
    for line in df_kmr_ratio[src_l]:
        file.write(line + "\n")
with open(f'{prep_dir_kmr}/{trg_l}-ratio','w') as file:
    for line in df_kmr_ratio[trg_l]:
        file.write(line + "\n")

# Write the entries excluded in the last two steps to file
with open(f'{prep_dir_ckb}/{src_l}-other','w') as file:
    for line in df_ckb_other[src_l]:
        file.write(line + "\n")
with open(f'{prep_dir_ckb}/{trg_l}-other','w') as file:
    for line in df_ckb_other[trg_l]:
        file.write(line + "\n")

with open(f'{prep_dir_ckb}/{src_l}-ratio','w') as file:
    for line in df_ckb_ratio[src_l]:
        file.write(line + "\n")
with open(f'{prep_dir_ckb}/{trg_l}-ratio','w') as file:
    for line in df_ckb_ratio[trg_l]:
        file.write(line + "\n")


# calculate cosine similarity → Reasonable for related languages
# https://stackoverflow.com/questions/15173225/calculate-cosine-similarity-given-2-sentence-strings

WORD = re.compile(r"[^ ]")

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)
"""

"""


cosine_values = []

for i in range(len(df_kmr)):
    text1 = df_kmr.iloc[i, 0]
    text2 = df_kmr.iloc[i, 1]
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    cosine = get_cosine(vector1, vector2)
    cosine_values.append(cosine)
df_kmr["cosine"] = cosine_values
#print(df.head())
"""

"""

cosine_values = []

for i in range(len(df_ckb)):
    text1 = df_ckb.iloc[i, 0]
    text2 = df_ckb.iloc[i, 1]
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    cosine = get_cosine(vector1, vector2)
    cosine_values.append(cosine)
df_ckb["cosine"] = cosine_values
#print(df.head())
"""

"""


# remove rows with less probability of parallelity
# which is the long tail of the whisker plot
#print("Length Dataframe (naive):", len(df))
#df = df[df["cosine"] > 0.48]
#print("Length Dataframe (cosine similarity > 0.48):", len(df))
"""

"""


# TODO: What happens when I tokenize a tokenized text again? How clever are modern tokenizers?
# tokenize texts
def nltk_tokenize(text):
    tokenized = word_tokenize(text)
    if len(tokenized[-1]) != 1:
        tokenized.append(".")
    return " ".join(tokenized)

df_kmr[src_l] = df_kmr[src_l].apply(nltk_tokenize)
df_kmr[trg_l] = df_kmr[trg_l].apply(nltk_tokenize)
df_ckb[src_l] = df_ckb[src_l].apply(nltk_tokenize)
df_ckb[trg_l] = df_ckb[trg_l].apply(nltk_tokenize)


# Save all data to a single file for training that does not build on cross-validaton
with open(f'{prep_dir_kmr}/{src_l}-all','w') as file:
    for line in df_kmr[src_l]:
        file.write(line + "\n")
with open(f'{prep_dir_kmr}/{trg_l}-all','w') as file:
    for line in df_kmr[trg_l]:
        file.write(line + "\n")
# Randomize order
df_kmr = df_kmr.sample(frac = 1).reset_index(drop = True)
print(df_kmr.head())
"""

"""

# Save all data to a single file for training that does not build on cross-validaton
with open(f'{prep_dir_ckb}/{src_l}-all','w') as file:
    for line in df_ckb[src_l]:
        file.write(line + "\n")
with open(f'{prep_dir_ckb}/{trg_l}-all','w') as file:
    for line in df_ckb[trg_l]:
        file.write(line + "\n")
# Randomize order
df_ckb = df_ckb.sample(frac = 1).reset_index(drop = True)
print(df_ckb.head())
"""

"""


# TODO: Make the number of splits variable
df_kmr1, df_kmr2, df_kmr3, df_kmr4, df_kmr5 = np.array_split(df_kmr, 5)
data_splits = [df_kmr1, df_kmr2, df_kmr3, df_kmr4, df_kmr5]
for index in [0, 1, 2, 3, 4]:
    print(f'df{index} length: {len(data_splits[index])}')
"""
df0 length: 32638
df1 length: 32638
df2 length: 32638
df3 length: 32637
df4 length: 32637
"""


for index in [0, 1, 2, 3, 4]:
    split_string = str(int(index+1))
    data_splits[index]
    with open(f'{prep_dir_kmr}/{src_l}-{split_string}','w') as file:
        for line in data_splits[index][src_l]:
            file.write(line + "\n")
    with open(f'{prep_dir_kmr}/{trg_l}-{split_string}','w') as file:
        for line in data_splits[index][trg_l]:
            file.write(line + "\n")


# TODO: Make the number of splits variable
df_ckb1, df_ckb2, df_ckb3, df_ckb4, df_ckb5 = np.array_split(df_ckb, 5)
data_splits = [df_ckb1, df_ckb2, df_ckb3, df_ckb4, df_ckb5]
for index in [0, 1, 2, 3, 4]:
    print(f'df{index} length: {len(data_splits[index])}')
"""
df0 length: 28740
df1 length: 28740
df2 length: 28740
df3 length: 28739
df4 length: 28739
"""


for index in [0, 1, 2, 3, 4]:
    split_string = str(int(index+1))
    data_splits[index]
    with open(f'{prep_dir_ckb}/{src_l}-{split_string}','w') as file:
        for line in data_splits[index][src_l]:
            file.write(line + "\n")
    with open(f'{prep_dir_ckb}/{trg_l}-{split_string}','w') as file:
        for line in data_splits[index][trg_l]:
            file.write(line + "\n")