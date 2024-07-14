# Author: Christian "Doofnase" Schuler
#######################################
# Project: Untangling Language Data
# Transforming (sentence-similarity) json data to csv data for Tangle-Application

import json
import csv
import argparse
import numpy as np
import os

def load_similarities(similarity_file):
    with open(similarity_file, 'r', encoding='utf-8') as f:
        similarities_dict = json.load(f)
        similarities = similarities_dict["similarities"]
    return similarities

def create_similarity_matrix(similarities):
    #print(f'{similarities.keys()}')
    num_sentences = max(int(i) for i in similarities.keys()) + 1  # Determine the size of the matrix
    matrix = np.full((num_sentences, num_sentences), np.nan)  # Initialize matrix with NaNs

    for i, similar_sentences in similarities.items():
        i = int(i)
        matrix[i, i] = 1.0  # Self-similarity is always 1
        for j, similarity in similar_sentences.items():
            j = int(j)
            matrix[i, j] = similarity

    return matrix

def save_matrix_to_csv(matrix, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([''] + [str(i) for i in range(matrix.shape[1])])  # Header
        for i, row in enumerate(matrix):
            writer.writerow([i] + row.tolist())

def main(similarity_file, output_file):
    similarities = load_similarities(similarity_file)
    matrix = create_similarity_matrix(similarities)
    save_matrix_to_csv(matrix, output_file)

if __name__ == "__main__":
    input_dir = '/media/AllBlue/LanguageData/PROJECTS/2024SchuTang/preprocessed'

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.startswith('similarities_') and file.endswith('.json'):
                file_path_json = os.path.join(root, file)
                file_path_csv = file_path_json.replace('.json','.csv')
                print(f'file_path_json: {file_path_json}')

                main(file_path_json, file_path_csv)


    # parser = argparse.ArgumentParser(description="Transform JSON similarity data to CSV format.")
    # parser.add_argument('--similarity_file', required=True, help="Input JSON file with similarities.")
    # parser.add_argument('--output_file', required=True, help="Output CSV file for the similarity matrix.")
    
    # args = parser.parse_args()
    
    # main(args.similarity_file, args.output_file)
