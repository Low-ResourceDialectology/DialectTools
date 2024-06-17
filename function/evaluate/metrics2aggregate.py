import os
import glob
import json
from collections import defaultdict
import pathlib

def dir_maker(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def collect_evaluation_data(root_dir):
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))

    # Recursively find all txt files (holding JSON-like data)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".txt"):
                file_path = os.path.join(dirpath, filename)
                
                # Extract directory components
                rel_path = os.path.relpath(file_path, root_dir)
                path_parts = rel_path.split(os.sep)
                
                if len(path_parts) < 5:
                    continue  # Skip any files that do not meet the depth criteria

                lang, quality, validity, perturbation, experiment_file = path_parts

                # Read the JSON file
                with open(file_path, 'r') as file:
                    metrics = json.load(file)

                    # Organize data
                    for metric in metrics:
                        metric_name = metric["name"]
                        metric_score = metric["score"]
                        experiment_file_name = os.path.basename(experiment_file).split('.')[0]
                        data[lang][quality][validity][perturbation][f"{experiment_file_name}_{metric_name}"] = metric_score

    return data

def save_aggregated_data(data, output_path, out_name):
    with open(f'{output_path}/{out_name}.json', 'w') as file:
        json.dump(data, file, indent=4)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Collect and aggregate evaluation metrics from text files.')
    parser.add_argument('-i', '--input_dir', type=str, required=True, help='Root directory containing evaluation data.')
    parser.add_argument('-o', '--output_dir', type=str, required=True, help='Output directory to save aggregated data to.')
    parser.add_argument('-f', '--filename', type=str, required=True, help='Name of output file with date for better long-term tracking of results.')

    args = parser.parse_args()
    dir_maker(args.output_dir)

    # Collect data
    aggregated_data = collect_evaluation_data(args.input_dir)

    # Save aggregated data to a JSON file
    save_aggregated_data(aggregated_data, args.output_dir, args.filename)

if __name__ == '__main__':
    main()
