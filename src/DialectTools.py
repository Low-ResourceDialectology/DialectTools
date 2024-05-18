# Author: Christian "Doofnase" Schuler
#######################################

# TODO: Some kind of easy interface to all the tools(?)


# Examples

""" Morfessor """

# Generating training data
from nltk.corpus import words

# using nltk word corpus as training data
words = words.words()
outfile = open("words", "w")
for word in words:
    outfile.write(word+"\n")

outfile.close()


# Building the model
import math
import morfessor

# function for adjusting the counts of each compound
def log_func(x):
    return int(round(math.log(x + 1, 2)))

infile = "words"
io = morfessor.MorfessorIO()
train_data = list(io.read_corpus_file(infile))
model = morfessor.BaselineModel()
model.load_data(train_data, count_modifier=log_func)
model.train_batch()
io.write_binary_model_file("model.bin", model)


# Testing the model
import morfessor

model_file = "model.bin"
io = morfessor.MorfessorIO()
model = io.read_binary_model_file(model_file)

word = raw_input("Input word > ")
# for segmenting new words we use the viterbi_segment(compound) method
print model.viterbi_segment(word)[0]



""" NEXT_TOOL """






