

# Text preprocessing of parallel data into training corpus splits

import pandas as pd
import seaborn as sns
import glob
import re
import math
import pathlib
from collections import Counter
import numpy as np
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

# TODO: Input arguments for more versatility
src_l = 'bar'
trg_l = 'de'
date_of_experiment = '20240524'
clean_dir = f'/media/AllBlue/LanguageData/CLEAN/opustools/{src_l}-{trg_l}'
prep_dir = f'/media/AllBlue/LanguageData/PREP/opustools/{src_l}-{trg_l}/{date_of_experiment}'

""" Check whether directory already exists and create if not """
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

dir_maker(prep_dir)

# Get all files based on language
src_files = glob.glob(f'{clean_dir}/*.{src_l}')
trg_files = glob.glob(f'{clean_dir}/*.{trg_l}')

#print(src_files)
#print(trg_files)
"""
['/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/WikiMatrix-bar-de.bar', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/XLEnt-bar-de.bar', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/Tatoeba-bar-de.bar', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/wikimedia-bar-de.bar']
['/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/WikiMatrix-bar-de.de', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/wikimedia-bar-de.de', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/XLEnt-bar-de.de', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/Tatoeba-bar-de.de']
"""


# Reorder parallel files

src_files_reordered = sorted(src_files)
trg_files_reordered = sorted(trg_files)

#print(src_files_reordered)
#print(trg_files_reordered)
"""
['/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/Tatoeba-bar-de.bar', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/WikiMatrix-bar-de.bar', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/XLEnt-bar-de.bar', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/wikimedia-bar-de.bar']
['/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/Tatoeba-bar-de.de', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/WikiMatrix-bar-de.de', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/XLEnt-bar-de.de', '/media/AllBlue/LanguageData/CLEAN/opustools/bar-de/wikimedia-bar-de.de']
"""


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
#print("Source Parallel Lines (naive): ", len(src_lines))
#print("Target Parallel Lines (naive): ", len(trg_lines))
"""
Source Parallel Lines: 101207
Target Parallel Lines:  101207
"""


#print("Some Example Parallel Lines (naive): ")
#print(src_lines[100:105])
#print(trg_lines[100:105])
"""
Some Example Parallel Lines: 
['Aber was noch wichtiger ist : Sie müssen sich ernsthaft fragen : Was hat das mit diesem Fall zu tun ?', 'Gobi – Die Wüste in mir .', '( Hat Probleme im Vollbildmodus .', 'Morgen kommt der Weihnachtsbär .', '1999 Zu Hause bin ich nur hier : am Theater .']
['Aber was noch wichtiger ist : Sie müssen sich ernsthaft fragen : Was hat das mit diesem Fall zu tun ?', 'Gobi – Die Wüste in mir .', '( Hat Probleme im Vollbildmodus .', 'Morgen kommt der Weihnachtsbär .', '1999 Zu Hause bin ich nur hier : am Theater .']
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
#print(df.head())
"""
                 bar                      de
0    I bin da Jack .        Ich heiße Jack .
1  I bin da Ludwig .  Mein Name ist Ludwig .
2   I bin da Henry .   Mein Name ist Henry .
3        Guadn Dog !             Guten Tag !
4  I bin da Ludwig .      Ich heiße Ludwig .
"""


# text preprocessing
def preprocess(text):
    # NOTE: Leave this step for later to better compare with DialectBLI data
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

"""


# Remove duplicates and empty lines
""" Compare length of sentences to reasonably exclude inproportionately sized 'alignment-pairs' """
def check_sent_length_reasonable(sent_01, sent_02):
    if len(sent_01) > 3 * len(sent_02) or len(sent_02) > 3 * len(sent_01):
        return False
    else:
        return True

df = df.dropna()
print(f'Length Dataframe (dropped na): {len(df)}')

df = df.drop_duplicates(subset = [src_l, trg_l])
print(f'Length Dataframe (dropped duplicates (multiple same source sentence)): {len(df)}')

df_other = df[(df[src_l].str.lower() == df[trg_l].str.lower())]
df = df[(df[src_l].str.lower() != df[trg_l].str.lower())]
print(f'Length Dataframe (dropped duplicate (source same as target sentence)): {len(df)}')

# TODO: KeyError: True .... ?
# df_ratio = df[(check_sent_length_reasonable(df[src_l], df[trg_l]))]
#df_ratio = df[(len(df[src_l]) > 3*len(df[trg_l])) | (len(df[src_l])*3 < len(df[trg_l]))]
# Create a boolean mask where the condition is met
mask = (df[src_l].str.len() > 3 * df[trg_l].str.len()) | (df[src_l].str.len() * 3 < df[trg_l].str.len())
# Apply the mask to the DataFrame to get the rows where the condition is true
df_ratio = df[mask]

#df = df[(not check_sent_length_reasonable(df[src_l], df[trg_l]))]
#df = df[not (len(df[src_l]) > 3*len(df[trg_l])) | (len(df[src_l])*3 < len(df[trg_l]))]
# Create a boolean mask where the condition is met
mask = (df[src_l].str.len() < 3 * df[trg_l].str.len()) & (df[src_l].str.len() * 3 > df[trg_l].str.len())
# Apply the mask to the DataFrame to get the rows where the condition is true
df = df[mask]

print(f'Length Dataframe (dropped inproportionate length differences (source/target 3 times as long as target/source)): {len(df)}')
"""
Length Dataframe (post-smart truncate): 101207
Length Dataframe (dropped na): 101207
Length Dataframe (dropped duplicates (multiple same source sentence)): 100368
Length Dataframe (dropped duplicate (source same as target sentence)): 84874
Length Dataframe (dropped inproportionate length differences (source/target 3 times as long as target/source)): 82893
"""

# Write the entries excluded in the last two steps to file
with open(f'{prep_dir}/{src_l}-other','w') as file:
    for line in df_other[src_l]:
        file.write(line + "\n")
with open(f'{prep_dir}/{trg_l}-other','w') as file:
    for line in df_other[trg_l]:
        file.write(line + "\n")

with open(f'{prep_dir}/{src_l}-ratio','w') as file:
    for line in df_ratio[src_l]:
        file.write(line + "\n")
with open(f'{prep_dir}/{trg_l}-ratio','w') as file:
    for line in df_ratio[trg_l]:
        file.write(line + "\n")



# calculate cosine similarity
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

for i in range(len(df)):
    text1 = df.iloc[i, 0] # bar
    text2 = df.iloc[i, 1] # de
    
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    cosine = get_cosine(vector1, vector2)
    
#     print(cosine)
    cosine_values.append(cosine)
"""

"""


df["cosine"] = cosine_values
#print(df.head())
"""
                 bar                      de  letters    cosine
0    i bin da jack .        ich heiße jack .       15  0.619780
1  i bin da ludwig .  mein name ist ludwig .       17  0.756978
2   i bin da henry .   mein name ist henry .       16  0.783349
3        guadn dog !             guten tag !       11  0.615385
4  i bin da ludwig .      ich heiße ludwig .       17  0.698297
"""


# remove rows with less probability of parallelity
# which is the long tail of the whisker plot
#print("Length Dataframe (naive):", len(df))
df = df[df["cosine"] > 0.48]
#print("Length Dataframe (cosine similarity > 0.48):", len(df))
"""
Length Dataframe (naive): 84438
Length Dataframe (cosine similarity > 0.48): 77873
"""


# TODO: What happens when I tokenize a tokenized text again? How clever are modern tokenizers?
# tokenize texts
def nltk_tokenize(text):
    tokenized = word_tokenize(text)
    if len(tokenized[-1]) != 1:
        tokenized.append(".")
    return " ".join(tokenized)

df[src_l] = df[src_l].apply(nltk_tokenize)
df[trg_l] = df[trg_l].apply(nltk_tokenize)
"""

"""


# Save all data to a single file for training that does not build on cross-validaton
with open(f'{prep_dir}/{src_l}-all','w') as file:
    for line in df[src_l]:
        file.write(line + "\n")
with open(f'{prep_dir}/{trg_l}-all','w') as file:
    for line in df[trg_l]:
        file.write(line + "\n")
# Randomize order
df = df.sample(frac = 1).reset_index(drop = True)
#print(df.head())
"""
                                                 bar                                                 de  letters    cosine
0                              delbrück einleitung .                                berthold delbrück .       19  0.716115
1  großherzogtum toskana 1 quartuccio = 38 3 / 8 ...  großherzogtum toskana 1 quartuccio = 38 3 / 8 ...      340  0.994558
2  1 2 3 institut national de la statistique et d...  1 2 3 institut national de la statistique et d...       68  0.981090
3                  b. die zittlóder der kranebeter .  am klosterweiherweiher des zisterzienserinnenk...       32  0.809439
4  zum östareichischen bundeslond vorarlberg gher...  zum österreichischen bundesland vorarlberg geh...       83  0.944781
"""



# TODO: Make the number of splits variable
df1, df2, df3, df4, df5 = np.array_split(df, 5)
data_splits = [df1, df2, df3, df4, df5]
for index in [0, 1, 2, 3, 4]:
    print(f'df{index} length: {len(data_splits[index])}')
#print("df1 length: ", len(df1))
#print("df2 length: ", len(df2))
#print("df3 length: ", len(df3))
#print("df4 length: ", len(df4))
#print("df5 length: ", len(df5))
"""
df0 length: 15277
df1 length: 15277
df2 length: 15277
df3 length: 15277
df4 length: 15277
"""

for index in [0, 1, 2, 3, 4]:
    split_string = str(int(index+1))
    data_splits[index]
    with open(f'{prep_dir}/{src_l}-{split_string}','w') as file:
        for line in data_splits[index][src_l]:
            file.write(line + "\n")
    with open(f'{prep_dir}/{trg_l}-{split_string}','w') as file:
        for line in data_splits[index][trg_l]:
            file.write(line + "\n")
"""

"""