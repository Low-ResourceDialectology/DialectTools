# -*- coding: utf8 -*-
# Plot the counted text content

# NOTE: Formerly "stats_viewer.py"

# Use (outdated)
"""
source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate

python3 /stats/stats_viewer.py --input-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned \
    --log-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned-plots/ --output-file als --mode all
python3 /stats/stats_viewer.py --input-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned \
    --log-dir /media/AllBlue/LanguageData/LOGS/wikidumps-cleaned-plots/ --output-file bar --mode all
    
python3 ./stats/stats_viewer.py --input-dir /media/AllBlue/LanguageData/LOGS/DialectBLI \
    --log-dir /media/AllBlue/LanguageData/LOGS/DialectBLI-plots/ --output-file als --mode all --language als
python3 ./stats/stats_viewer.py --input-dir /media/AllBlue/LanguageData/LOGS/DialectBLI \
    --log-dir /media/AllBlue/LanguageData/LOGS/DialectBLI-plots/ --output-file bar --mode all --language bar
"""

import argparse
import glob
from adjustText import adjust_text
import json
import matplotlib.pyplot as plt
import os
import sys
import seaborn as sns

def plot_text_counts_bar(in_dir, log_dir, out_file, in_file, bar_label):
    """Reads the JSON log file and plots the text counts."""
    try:
        with open(f'{in_dir}/{in_file}.json', 'r', encoding='utf-8') as file:
            text_counts = json.load(file)
        
        files = list(text_counts.keys())
        num_lines = [text_counts[file]['lines'] for file in files]

        # Calculate the total number of lines for percentage calculation
        total_lines = sum(num_lines)

        # Replace underscores with spaces in file names for the plot
        labels = [file.replace('_', ' ') for file in files]
        
        # Plotting the data
        plt.figure(figsize=(12, 8))

        # Use a seaborn color palette for the bars
        colors = sns.color_palette("husl", len(files))
        bars = plt.bar(labels, num_lines, color=colors)

        if bar_label == "percentage":
            # Adding percentage labels on top of the bars
            for i, (bar, value) in enumerate(zip(bars, num_lines)):
                percentage = (value / total_lines) * 100
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, 
                        f'{percentage:.2f}%', ha='center', va='bottom', fontsize=12)
        elif bar_label == "number":
            # Adding number of items as labels on top of the bars
            # TODO
            pass
        elif bar_label == "all":
            # Adding percentage and number labels on top of the bars
            for i, (bar, value) in enumerate(zip(bars, num_lines)):
                percentage = (value / total_lines) * 100
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, 
                        f'{percentage:.2f}%\n({value})', ha='center', va='bottom', fontsize=12)

        #plt.title('Text Counts per File')
        #plt.xlabel(fontsize=20)
        plt.ylabel('Number of Lines', fontsize=20)
        plt.xticks(rotation=45, ha='right', fontsize=20)  # Rotate x-axis labels for better spacing
        plt.yticks(fontsize=20)

        plt.tight_layout()
        #plt.ylim(top = max(num_lines)+18000)
        plt.ylim(top = 180000)
        plt.savefig(f'{log_dir}/{out_file}_bar.png', bbox_inches='tight')
        #plt.show()

    except Exception as e:
        print(f"Error reading JSON file or plotting data: {e}")


def plot_text_counts_pie(in_dir, log_dir, out_file, in_file, adjust_text_flag):
    """Reads the JSON log file and plots the text counts as a pie chart."""
    try:
        with open(f'{in_dir}/{in_file}.json', 'r', encoding='utf-8') as file:
            text_counts = json.load(file)
        
        files = list(text_counts.keys())
        num_lines = [text_counts[file]['lines'] for file in files]

        # Replace underscores with spaces in file names for the plot
        labels = [file.replace('_', ' ') for file in files]
        
        # Use a seaborn color palette for the pie chart
        colors = sns.color_palette("husl", len(files))

        # Plotting the data
        plt.figure(figsize=(12, 8))


        if adjust_text_flag:
            wedges, texts, autotexts = plt.pie(num_lines, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'fontsize': 12})

            # Adjust label positions to avoid overlap
            texts = [text for text in texts]
            for text in texts:
                text.set_fontsize(20)

            autotexts = [autotext for autotext in autotexts]
            for autotext in autotexts:
                autotext.set_fontsize(18)

            # Use adjust_text to avoid overlaps
            adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
            adjust_text(autotexts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

        else:
            wedges, texts, autotexts = plt.pie(num_lines, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'fontsize': 18})
            # Improve label spacing
            for text in texts:
                text.set_fontsize(20)
            for autotext in autotexts:
                autotext.set_fontsize(18)

            plt.pie(num_lines, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'fontsize': 18})

        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.tight_layout()
        plt.savefig(f'{log_dir}/{out_file}_pie.png', bbox_inches='tight')
        #plt.show()

    except Exception as e:
        print(f"Error reading JSON file or plotting data: {e}")


if __name__ == "__main__":
    # For original data (no filtering at all)
    input_dir = '/media/AllBlue/LanguageData/LOGS/wikidumps-cleaned'
    log_dir = '/media/AllBlue/LanguageData/LOGS/wikidumps-cleaned-plots' 
    input_file = 'bar-clean'
    output_file = 'bar-clean'
    adjust_text_flag = False
    bar_label = "all"
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if os.path.isdir(input_dir):
        plot_text_counts_bar(input_dir, log_dir, output_file, input_file, bar_label)
        plot_text_counts_pie(input_dir, log_dir, output_file, input_file, adjust_text_flag)
    else:
        print(f"The provided path '{input_dir}' is not a valid directory.")

    # For "gold" data
    input_dir = '/media/AllBlue/LanguageData/LOGS/wikidumps-cleaned'
    log_dir = '/media/AllBlue/LanguageData/LOGS/wikidumps-cleaned-plots' 
    input_file = 'bar-gold'
    output_file = 'bar-gold'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if os.path.isdir(input_dir):
        plot_text_counts_bar(input_dir, log_dir, output_file, input_file, bar_label)
        plot_text_counts_pie(input_dir, log_dir, output_file, input_file, adjust_text_flag)
    else:
        print(f"The provided path '{input_dir}' is not a valid directory.")

    # For "silver" data
    input_dir = '/media/AllBlue/LanguageData/LOGS/wikidumps-cleaned'
    log_dir = '/media/AllBlue/LanguageData/LOGS/wikidumps-cleaned-plots' 
    input_file = 'bar-silver'
    output_file = 'bar-silver'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if os.path.isdir(input_dir):
        plot_text_counts_bar(input_dir, log_dir, output_file, input_file, bar_label)
        plot_text_counts_pie(input_dir, log_dir, output_file, input_file, adjust_text_flag)
    else:
        print(f"The provided path '{input_dir}' is not a valid directory.")




# if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Get text statistics')
    # parser.add_argument('-i','--input-dir', type=str, help='input directory')
    # parser.add_argument('-l','--log-dir', type=str, help='logging directory')
    # parser.add_argument('-o','--output-file', type=str, help='output filename')
    # parser.add_argument('-m','--mode', type=str, help='counting mode', default="all")
    # parser.add_argument('-c','--language', type=str, help='languegcode of log file')

    # args = parser.parse_args()
    
    # if not os.path.exists(args.log_dir):
    #     os.makedirs(args.log_dir)
    # if os.path.isdir(args.input_dir):
    #     plot_text_counts(args.input_dir, args.log_dir, args.output_file, args.mode, args.language)
    #     #read_files = glob.glob(f'{args.input_dir}*.json')
    #     #for in_file in read_files:
    #     #    plot_text_counts(in_file, args.log_dir, args.output_file, args.mode)
    # else:
    #     print(f"The provided path '{args.input_dir}' is not a valid directory.")