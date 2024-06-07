# NOTE: First attempt- soon to be removed by "split_text.py"

import os
import pandas as pd
import numpy as np
import argparse

def read_sentences_from_csv(directory, column):
    sentences = []
    column = int(column)
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            # Assuming sentences are in the second column (index 1)
            sentences.extend(df.iloc[:, column].dropna().tolist())
    return sentences

def parse_splits(splits_str):
    splits = [float(x) for x in splits_str.split(",")]
    if not np.isclose(sum(splits), 1.0):
        raise ValueError("Splits must sum to 1.0")
    return splits

def split_sentences(sentences, splits):
    np.random.shuffle(sentences)
    split_indices = (np.cumsum(splits) * len(sentences)).astype(int)
    return np.split(sentences, split_indices[:-1])

def write_sentences_to_files(sentences_split, output_dir, splits, language, format):
    splits_string = splits.replace(',0.','_').replace('0.','') # '0.5,0.3,0.2' → 5_3_2
    output_dir = f'{output_dir}/{language}-{splits_string}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if format == "txt":
        for i, sentences in enumerate(sentences_split):
            output_file = os.path.join(output_dir, f"split_{i + 1}.txt")
            with open(output_file, 'w') as f:
                for sentence in sentences:
                    f.write(f"{sentence}\n")
    elif format == "csv":        
        for i, sentences in enumerate(sentences_split):
            output_file = os.path.join(output_dir, f"split_{i + 1}.csv")
            df = pd.DataFrame(sentences, columns=["Sentence"])
            df.to_csv(output_file, index=False)
    else:
        print(f'Output format not recognized!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split sentences from CSV files into subsets.")
    parser.add_argument("--input_dir", type=str, help="Directory containing CSV files with sentences.")
    parser.add_argument("--column", type=str, help="Column of CSV files from which to read sentences.")
    parser.add_argument("--output_dir", type=str, help="Directory to save the output CSV files.")
    parser.add_argument("--proportions", type=str, help="Comma-separated list of split-proportions (e.g., '0.5,0.3,0.2').")
    parser.add_argument("--language", type=str, help="Language code for file naming.")
    parser.add_argument("--format_output", type=str, help="Format of the output files.")

    args = parser.parse_args()
    
    sentences = read_sentences_from_csv(args.input_dir, args.column)
    splits = parse_splits(args.proportions)
    sentences_split = split_sentences(sentences, splits)
    write_sentences_to_files(sentences_split, args.output_dir, args.proportions, args.language, args.format_output)
    
    print("Sentences have been successfully split and written to output files.")
