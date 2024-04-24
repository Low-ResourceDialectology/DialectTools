import argparse
import csv
from datetime import datetime
import glob
import json
import os
import statistics
import sys

"""
# Use: 
my_processor = TextProcessor(in_dri, out_dir, "read")


"""


class TextProcessor:
    def __init__(self, key):
        self.key = key
        with open(f'structure.json', 'r') as json_file:
            text_structure_info = json_file.read()
            self.key_info = text_structure_info[key]

    def __init__(self, in_dir, out_dir, mode):
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.mode = mode


    # Read text from files
    def ensure_directory_exists(directory):
        """Ensure that the directory exists, create it if it doesn't."""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def read(self, directory, encoding, format):
        self.ensure_directory_exists(directory)
        reader = TextReader(directory+self.key+'.csv',input_type='paragraph')
        intermediate_data = reader.read_csv_column('2,3')
        sentences = reader.process_csv(intermediate_data,input_type='paragraph')
        reader.




    # Write text to files





class TextReader: 
    def __init__(self, input_file, file_format='csv') -> None:
        self.input = input_file
        self.file_format = file_format
        # if self.file_format == 'csv':
            # if mode == 'all':
                # csv_out = self.read_csv()
            # elif mode == 'column':
            # csv_data = self.read_csv_column()
            # self.data = self.process_csv(csv_data, input_type) # a list of sentences
        # elif self.file_format == 'txt':
            # self.read_txt()
        

    def read_csv_column(self, column_index, file_delimiter=','):
        input_file = self.input
        csv_rows_list = []
        column_index = column_index.split(',')
        for index in column_index:
            with open(f'{input_file}.csv', newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=file_delimiter, quotechar='"')
                for row in csv_reader:
                    csv_rows_list.append(row[int(index)])
            return csv_rows_list

    '''
    input: 
    output: a list of sentences as string
    '''
    def process_csv(self, input, input_type):
        assert input_type == 'word' or 'sentence' or 'paragraph'
        if input_type == 'word':
            pass
        elif input_type == 'sentence':
            pass#self.tokenize_into_words(input)
        elif input_type == 'paragraph':
            self.tokenize_into_sentences(input)
        else : 
            pass


    # Clean text that was read


    # Translate into other language


    # Align texts


    # For languages not covered by the nltk package
    def tokenize_into_words(text_lines):
        pass

    # For languages not covered by the nltk package
    '''
    input: a list of paragraphs
    output: a list of sentences
    '''
    def tokenize_into_sentences(text_lines):
        sentences = []
        current_sentence = ""
        sentence_delimiters = [".", "!", "?"]  # You may need to adjust this based on the specific punctuation used in Central Kurdish

        for line in text_lines:
            for char in line:
                current_sentence += char
                if char in sentence_delimiters:
                    sentences.append(current_sentence.strip())
                    current_sentence = ""

        # Append the last sentence if it's not empty
        if current_sentence.strip():
            sentences.append(current_sentence.strip())

        return sentences

