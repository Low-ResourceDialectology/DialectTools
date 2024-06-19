import argparse
import os
import glob

def analyze_file(file_path, thresholds):
    line_lengths = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line_lengths.append(len(line.strip()))
    
    num_lines = len(line_lengths)
    avg_length = sum(line_lengths) / num_lines if num_lines > 0 else 0

    threshold_counts = {threshold: 0 for threshold in thresholds}
    for length in line_lengths:
        for threshold in thresholds:
            if length > threshold:
                threshold_counts[threshold] += 1

    return num_lines, avg_length, threshold_counts

def main():
    parser = argparse.ArgumentParser(description='Analyze text files in a directory.')
    parser.add_argument('-i', '--input_dir', type=str, required=True, help='Directory containing text files.')
    parser.add_argument('-f', '--filename_part', type=str, required=True, help='Part of text file names.')
    parser.add_argument('-t', '--thresholds', type=str, required=True, help='Comma-separated list of thresholds.')
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    thresholds = list(map(int, args.thresholds.split(',')))

    text_files = glob.glob(os.path.join(input_dir, f'*{args.filename_part}*'))
    
    for text_file in text_files:
        num_lines, avg_length, threshold_counts = analyze_file(text_file, thresholds)
        
        print(f"File: {text_file}")
        print(f"  Number of lines: {num_lines}")
        print(f"  Average line length: {avg_length:.2f}")
        for threshold in thresholds:
            print(f"  Number of lines longer than {threshold} characters: {threshold_counts[threshold]}")
        print()

if __name__ == '__main__':
    main()