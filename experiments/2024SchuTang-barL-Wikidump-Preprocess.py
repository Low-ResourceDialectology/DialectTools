# Author: Christian "Doofnase" Schuler
#######################################
# Project: Untangling Language Data
# Preparing (a subset of the Bavarian wikidump) dialect text data for Tangle-Application

import os
import json
import argparse
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
#from scipy.spatial.distance import jaccard
#from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from gensim.models import Word2Vec
#from sklearn.preprocessing import normalize
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import pathlib

"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def load_sentences(input_dir):
    sentences = []
    sentence_to_file = []
    #for input_dir in input_dirs:
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    sentences.extend(lines)
                    sentence_to_file.extend([(line.strip(), file_path) for line in lines])
    return sentences, sentence_to_file

def vectorize_sentences(sentences, method='tfidf', model=None):
    if method == 'tfidf':
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(sentences).toarray()
    elif method == 'count':
        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(sentences).toarray()
    # NOTE: Work in progress
    # elif method == 'word2vec':
    #     # Tokenize sentences
    #     tokenized_sentences = [sentence.split() for sentence in sentences]
    #         # Train Word2Vec model
    #         #w2v_model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)
    #         # Get average vector for each sentence and define data type as np.float64 for high precision and json-serializability (float32 is NOT JSON serializable)
    #         #X = np.array([np.mean([w2v_model.wv[word] for word in words if word in w2v_model.wv] or [np.zeros(100, dtype=np.float64)], axis=0, dtype=np.float64) for words in tokenized_sentences], dtype=np.float64)
    #     # X = np.array([np.mean([model.encode[word] for word in words if word in model.wv] or [np.zeros(100, dtype=np.float64)], axis=0)for words in tokenized_sentences], dtype=np.float64)
    elif method == 'sbert_para_multi_l12_v2':
        #model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # or any other pre-trained model
        #model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2') 
        X = model.encode(sentences)
    else:
        raise ValueError("Unknown vectorization method")
    return X

def compute_similarities(X, metric='cosine'):
    if metric == 'cosine':
        similarities = cosine_similarity(X)
    elif metric == 'euclidean':
        similarities = euclidean_distances(X)
    elif metric == 'manhattan':
        from sklearn.metrics.pairwise import manhattan_distances
        similarities = manhattan_distances(X)
    elif metric == 'jaccard':
        from sklearn.metrics import jaccard_score
        similarities = np.array([[jaccard_score(x, y, average='macro') for y in X] for x in X])
    elif metric == 'hamming':
        from sklearn.metrics import pairwise_distances
        similarities = pairwise_distances(X, metric='hamming')
    else:
        raise ValueError("Unknown similarity metric")
    return similarities

def save_results(similarities, sentences, sentence_to_file, output_file_mapping, output_file_similarities):
    mapping_dict = {
        "sentence_mapping": {i: {"sentence": s, "file": f} for i, (s, f) in enumerate(sentence_to_file)}
    }
    similarity_dict = {
        "similarities": {i: {j: float(similarities[i, j]) for j in range(len(sentences)) if i != j} for i in range(len(sentences))}
    }

    # Save the mapping dictionary to a JSON file
    with open(output_file_mapping, 'w', encoding='utf-8') as mapping_file:
        json.dump(mapping_dict, mapping_file, ensure_ascii=False, indent=4)

    # Save the similarity dictionary to a JSON file
    with open(output_file_similarities, 'w', encoding='utf-8') as similarity_file:
        json.dump(similarity_dict, similarity_file, ensure_ascii=False, indent=4)

#def main(input_dirs, output_file, vectorization_method, similarity_metric):
def main(in_dir, out_dir, tag_levels, sampling_levels, configs):

    # For each configuration  
    for _, config in configs.items():

        vectorization_method = config['vectorization']
        similarity_metric = config['similarity_metric']
        threshold = config['threshold']

        # Load Word2Vec model if needed
        if vectorization_method == 'word2vec':
            model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            # Source: https://huggingface.co/tasks/sentence-similarity
        elif vectorization_method == 'sbert_para_multi_l12_v2':
            model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
            # Source: https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
        # elif OTHER_METHOD == 'other_method':
        # model = LOAD_OTHER_MODEL('path_to_other_model')
        else:
            model = None

        # Directory containing the text files
        for tag_level in tag_levels:
            for sampling_level in sampling_levels:
                input_dir = f'{in_dir}/{tag_level}/{sampling_level}'
                output_dir = f'{out_dir}/{tag_level}/{sampling_level}'
                dir_maker(output_dir)
                output_file_mapping = f'{output_dir}/mapping_{vectorization_method}_{similarity_metric}_{threshold}.json'
                output_file_similarities = f'{output_dir}/similarities_{vectorization_method}_{similarity_metric}_{threshold}.json'

                sentences, sentence_to_file = load_sentences(input_dir)
                print(f"Loaded {len(sentences)} sentences from {input_dir} directory.")
  
                X = vectorize_sentences(sentences, method=vectorization_method, model=model)
                similarities = compute_similarities(X, metric=similarity_metric)
                save_results(similarities, sentences, sentence_to_file, output_file_mapping, output_file_similarities)
                print(f"Results saved to {output_dir}")


if __name__ == "__main__":
    input_dir = '/media/AllBlue/LanguageData/PROJECTS/2024SchuTang/input'
    output_dir = '/media/AllBlue/LanguageData/PROJECTS/2024SchuTang/preprocessed'
    tag_levels = ['silver', 'gold']
    sampling_levels = ['equally', 'proportionally']
    #tag_levels = ['gold']
    #sampling_levels = ['equally']
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
            # NOTE: Work in progress
            # "config004": {
            #     'vectorization': 'word2vec',
            #     'similarity_metric': 'cosine',
            #     'threshold': 0.01
            # },
        # "config005": {
        #     'vectorization': 'sbert_para_multi_l12_v2',
        #     'similarity_metric': 'cosine',
        #     'threshold': 0.01
        # }
    }

    """ NOTE: Info
        'vectorization': 'tfidf',           # Options: 'tfidf', 'count', etc.
        'similarity_metric': 'cosine',      # Options: 'cosine', 'euclidean', etc.
        'threshold': 0.5,                   # Threshold for storing similarities
    """
    
    main(input_dir, output_dir, tag_levels, sampling_levels, configs)


# if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Calculate and store sentence similarities.")
    # parser.add_argument('--input_dirs', nargs='+', required=True, help="Input directories containing text files.")
    # parser.add_argument('--output_file', required=True, help="Output file to save the similarities.")
    # parser.add_argument('--vectorization_method', choices=['tfidf', 'count', 'word2vec', 'sentence_bert'], required=True, help="Vectorization method to use.")
    # parser.add_argument('--similarity_metric', choices=['cosine', 'euclidean', 'manhattan', 'jaccard', 'hamming'], required=True, help="Similarity metric to use.")

    # args = parser.parse_args()

    # main(args.input_dirs, args.output_file, args.vectorization_method, args.similarity_metric)