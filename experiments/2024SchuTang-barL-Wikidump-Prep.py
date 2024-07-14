# Author: Christian "Doofnase" Schuler
#######################################
# Project: Untangling Language Data
# Preparing (a subset of the Bavarian wikidump) dialect text data for Tangle-Application

import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
from scipy.spatial.distance import jaccard
from tqdm import tqdm
from gensim.models import Word2Vec
from sklearn.preprocessing import normalize
import pathlib

"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


# Read Sentences from Files
def read_sentences(input_dir):
    sentences = []
    labels = []
    mapping_dict = {}
    index = 0
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            class_label = filename.replace('_', ' ').replace('.txt', '')
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        sentences.append(line)
                        labels.append(class_label)
                        mapping_dict[index] = {'sentence': line, 'class_label': class_label, 'file': filename}
                        index += 1
    return sentences, labels, mapping_dict

# Vectorization Methods
def vectorize_sentences(sentences, method='tfidf'):
    if method == 'tfidf':
        vectorizer = TfidfVectorizer(max_features=10000)
        X = vectorizer.fit_transform(sentences)
    elif method == 'count':
        vectorizer = CountVectorizer(max_features=10000)
        X = vectorizer.fit_transform(sentences)
    elif method == 'word2vec':
        # Tokenize sentences
        tokenized_sentences = [sentence.split() for sentence in sentences]
        # Train Word2Vec model
        w2v_model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)
        # Get average vector for each sentence and define data type as np.float64 for high precision and json-serializability (float32 is NOT JSON serializable)
        X = np.array([np.mean([w2v_model.wv[word] for word in words if word in w2v_model.wv] or [np.zeros(100, dtype=np.float64)], axis=0, dtype=np.float64) for words in tokenized_sentences], dtype=np.float64)
        # Normalize the vectors
        X = normalize(X)
    else:
        raise ValueError(f"Unknown vectorization method: {method}")
    return X

# Similarity Metrics
def compute_similarity(X, metric='cosine'):
    if metric == 'cosine':
        similarity_matrix = cosine_similarity(X)
    elif metric == 'euclidean':
        similarity_matrix = euclidean_distances(X)
    elif metric == 'manhattan':
        similarity_matrix = manhattan_distances(X)
    elif metric == 'jaccard':
        # Jaccard distance expects binary vectors
        X_binary = (X > 0).astype(int)
        similarity_matrix = np.zeros((X.shape[0], X.shape[0]))
        for i in range(X.shape[0]):
            for j in range(X.shape[0]):
                similarity_matrix[i, j] = 1 - jaccard(X_binary[i], X_binary[j])
    else:
        raise ValueError(f"Unknown similarity metric: {metric}")
    return similarity_matrix

# Main Function
def main(in_dir, out_dir, tag_level, sampling_levels, configs):

    # For each configuration  
    for _, config in configs.items():
        # Directory containing the text files
        for tag_level in tag_levels:
            for sampling_level in sampling_levels:
                input_dir = f'{in_dir}/{tag_level}/{sampling_level}'
                output_dir = f'{out_dir}/{tag_level}/{sampling_level}'
                dir_maker(output_dir)

                # Read sentences, labels, and create mapping dictionary
                sentences, labels, mapping_dict = read_sentences(input_dir)

                # Vectorize sentences
                X = vectorize_sentences(sentences, method=config['vectorization'])

                # Compute similarity
                similarity_matrix = compute_similarity(X, metric=config['similarity_metric'])

                # Store Results
                similarity_dict = {}
                threshold = config['threshold']

                # Save the mapping dictionary to a JSON file
                mapping_file = f'{output_dir}/sentence_mapping_{config["vectorization"]}_{config["similarity_metric"]}_{config["threshold"]}.json'
                with open(mapping_file, 'w', encoding='utf-8') as file:
                    json.dump(mapping_dict, file, ensure_ascii=False, indent=4)

                # Initialize progress bar
                print("Computing similarities...")
                for i in tqdm(range(similarity_matrix.shape[0]), desc="Processing Sentences"):
                    similarity_dict[i] = {}
                    for j in range(similarity_matrix.shape[1]):
                        if similarity_matrix[i, j] > threshold and i != j:
                            similarity_dict[i][j] = similarity_matrix[i, j]

                # Save the similarity dictionary to a JSON file
                output_file = f'{output_dir}/sentence_similarities_{config["vectorization"]}_{config["similarity_metric"]}_{config["threshold"]}.json'
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump({
                        "similarities": similarity_dict
                    }, file, ensure_ascii=False, indent=4)
                    # json.dump({
                    #     "similarities": similarity_dict,
                    #     "labels": labels
                    # }, file, ensure_ascii=False, indent=4)

                
            
            print(f'Similarity calculations and storage completed for {tag_level}-tag quality and {sampling_level}-sampling.')

    

if __name__ == "__main__":
    input_dir = '/media/AllBlue/LanguageData/PROJECTS/2024SchuTang/input'
    output_dir = '/media/AllBlue/LanguageData/PROJECTS/2024SchuTang/preprocessed'
    #tag_levels = ['silver', 'gold']
    #sampling_levels = ['equally', 'proportionally']
    tag_levels = ['silver']
    sampling_levels = ['equally']
    configs = {
        # "config001": {
        #     'vectorization': 'tfidf',
        #     'similarity_metric': 'cosine',
        #     'threshold': 0.5
        # },
        # "config002": {
        #     'vectorization': 'tfidf',
        #     'similarity_metric': 'cosine',
        #     'threshold': 0.1
        # },
        # "config003": {
        #     'vectorization': 'tfidf',
        #     'similarity_metric': 'cosine',
        #     'threshold': 0.01
        # },
        "config004": {
            'vectorization': 'word2vec',
            'similarity_metric': 'cosine',
            'threshold': 0.01
        }
    }

    """ NOTE: Info
        'vectorization': 'tfidf',           # Options: 'tfidf', 'count', etc.
        'similarity_metric': 'cosine',      # Options: 'cosine', 'euclidean', etc.
        'threshold': 0.5,                   # Threshold for storing similarities
    """
    
    main(input_dir, output_dir, tag_levels, sampling_levels, configs)

