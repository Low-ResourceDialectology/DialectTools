# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Reads textlines and removes those deemed too long before writing to file again.

import argparse
import os

parser = argparse.ArgumentParser(description='Take care of long sentences by removing them from the data')
parser.add_argument('-i','--input_file', type=str, help='input file')
parser.add_argument('-o','--output_file', type=str, help='output file')
parser.add_argument('-m','--max_length', type=int, default=2000, help="Maximum length of sentences before removing them")

args = parser.parse_args()

excluded_counter = 0
with open(args.output_file, "w") as out_file:
    with open(args.input_file, "r") as in_file:
        # Iterate over each line in the input file
        for input_line in in_file:
            # Remove sentences longer than max_length (default: 2000) characters
            if (len(input_line) <= args.max_length):
                line = input_line.replace("\n","")
                out_file.write(f'{line}\n')
            else:
                #print(f'Exlcuding: {input_line}')
                excluded_counter = excluded_counter + 1

print(f'Number of excluded text lines: {excluded_counter}')