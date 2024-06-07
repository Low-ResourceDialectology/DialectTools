import os
import argparse
from collections import defaultdict

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def remove_existing_output_files(output_path, substrings, extensions):
    for substring in substrings:
        for ext in extensions:
            output_file_name = f"{substring}{ext}"
            output_file_path = os.path.join(output_path, output_file_name)
            if os.path.exists(output_file_path):
                os.remove(output_file_path)

def group_files_by_substring_and_pair(input_path, substrings):
    groups = defaultdict(lambda: defaultdict(list))
    extensions = set()
    
    for file_name in os.listdir(input_path):
        for substring in substrings:
            if substring in file_name:
                base_name, ext = os.path.splitext(file_name)
                groups[substring][base_name].append(file_name)
                extensions.add(ext)
                break
                # Remove the substring and extension to get the actual base name for grouping
                # actual_base_name = base_name.replace(substring, '')
                # groups[substring][actual_base_name].append((file_name, ext))
                # extensions.add(ext)
                # break
    
    return groups, extensions

def process_and_pool_files(input_path, output_path, substrings):
    groups, extensions = group_files_by_substring_and_pair(input_path, substrings)
    
    # Remove existing output files before processing
    remove_existing_output_files(output_path, substrings, extensions)
    
    for substring, file_dict in groups.items():
        for base_name, files in file_dict.items():
            if len(files) != 2:
                print(f"Warning: {base_name} does not have exactly 2 matching files. Skipping.")
                print(files)
                continue

            file1, ext1 = files[0]
            file2, ext2 = files[1]

            lines1 = read_file(os.path.join(input_path, file1))
            lines2 = read_file(os.path.join(input_path, file2))

            if len(lines1) != len(lines2):
                print(f"Warning: Line count mismatch in files {file1} and {file2}. Skipping.")
                continue

            output_file1 = os.path.join(output_path, f"{substring}{ext1}")
            output_file2 = os.path.join(output_path, f"{substring}{ext2}")

            write_file(output_file1, lines1)
            write_file(output_file2, lines2)

        print(f"Content processed for group '{substring}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Group files by substrings and extensions, pool their content while maintaining sentence alignment, and write to new files.")
    parser.add_argument("-i","--input_dir", type=str, help="Path to the directory containing text files")
    parser.add_argument("-o","--output_dir", type=str, help="Directory to save the output files.")
    parser.add_argument("-s","--substrings", type=str, help="List of substrings provided as a string to be parsed to group files by")

    args = parser.parse_args()
    print(f'INFO: Provided substrings for file grouping: {args.substrings}')
    substrings = [str(item) for item in args.substrings.split(',')]
    print(f'INFO: Prased substrings for file grouping: {substrings}')
    try:
        os.makedirs(args.output_dir)
    except FileExistsError:
        # Directory already exists
        pass
    #parser.add_argument("input_path", type=str, help="Path to the directory containing text files")
    #parser.add_argument("substrings", type=str, nargs='+', help="List of substrings to group files by")

    process_and_pool_files(args.input_dir, args.output_dir, substrings)
    print(f'Subsets have been successfully combined and written to: {args.output_dir}.')