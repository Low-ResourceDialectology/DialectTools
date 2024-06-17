
"""
A separate table for each set of languages
"""
import json
import os

def generate_latex_table_start(output_file):
    latex_code = "\\newcommand{\\specialcell}[2][c]{%\n"
    latex_code += "\\begin{tab"
    latex_code += "ular}[#1]{@{}c@{}}#2\\end{tabular}}\n"
    latex_code += " \n"
    with open(output_file, 'w') as file:
        file.write(latex_code)
        file.write("\n")

def generate_latex_table_for_language(language, data, output_file):
    language = language.replace('_','-')
    latex_code = "\\begin{tab"
    latex_code += "le}[h!]"
    latex_code += "\\centering\n"
    latex_code += f"\\caption{{Evaluation Metrics for {language}}}\n"
    latex_code += "\\begin{tabular}{|l|l|l|l|r|r|r|}\n"
    latex_code += "\\hline\n"
    #latex_code += "Data Quality & Feature Validity & Perturbation Type & Experiment & BLEU & chrF2 & TER \\\\\n"
    latex_code += "\\specialcell{Data \\\\Quality} & \\specialcell{Feature \\\\Validity} & \\specialcell{Perturbation \\\\Type} & Experiment & BLEU & chrF2 & TER \\\\\n"
    latex_code += "\\hline\n"

    for quality, validities in data.items():
        for validity, perturbations in validities.items():
            for perturbation, metrics in perturbations.items():
                experiments = set(key.split('_')[0] for key in metrics.keys())
                
                for experiment in experiments:
                    bleu_key = f"{experiment}_BLEU"
                    chrf2_key = f"{experiment}_chrF2"
                    ter_key = f"{experiment}_TER"
                    
                    bleu = metrics.get(bleu_key, "-")
                    chrf2 = metrics.get(chrf2_key, "-")
                    ter = metrics.get(ter_key, "-")

                    latex_code += f"{quality} & {validity} & {perturbation} & {experiment} & {bleu} & {chrf2} & {ter} \\\\\n"
                    latex_code += "\\hline\n"

    latex_code += "\\end{tabular}\n"
    latex_code += "\\end{table}\n"

    with open(output_file, 'a') as file:
        file.write(latex_code)
        file.write("\n")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Convert JSON evaluation data to LaTeX tables.')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input JSON file containing evaluation data.')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Output file to save the LaTeX tables.')

    args = parser.parse_args()

    # Read JSON data
    with open(args.input_file, 'r') as file:
        data = json.load(file)

    # Generate the start of the latex code and the "newcommand" for specialcell, which enables linebreaks inside table cells
    generate_latex_table_start(args.output_file)

    # Create LaTeX tables for each language
    for language, metrics in data.items():
        generate_latex_table_for_language(language, metrics, args.output_file)

if __name__ == '__main__':
    main()


"""
All data in a single table
"""
# import json
# import os

# def json_to_combined_latex_table(data, output_file):
#     latex_code = "\\newcommand{\\specialcell}[2][c]{%\n"
#     latex_code += "\\begin\{tabular\}[#1]{@{}c@{}}#2\\end{tabular}}\n"
#     latex_code += "\\begin{tabular}{|l|l|l|l|l|r|r|r|}\n"
#     latex_code += "\\hline\n"
#     latex_code += "Languages & \\specialcell{Data \\\\Quality} & \\specialcell{Feature \\\\Validity} & \\specialcell{Perturbation \\\\Type} & Experiment & BLEU & chrF2 & TER \\\\\n"
#     latex_code += "\\hline\n"

#     for lang, qualities in data.items():
#         for quality, validities in qualities.items():
#             for validity, perturbations in validities.items():
#                 for perturbation, metrics in perturbations.items():
#                     experiments = set(key.split('_')[0] for key in metrics.keys())
                    
#                     for experiment in experiments:
#                         bleu_key = f"{experiment}_BLEU"
#                         chrf2_key = f"{experiment}_chrF2"
#                         ter_key = f"{experiment}_TER"
                        
#                         bleu = metrics.get(bleu_key, "-")
#                         chrf2 = metrics.get(chrf2_key, "-")
#                         ter = metrics.get(ter_key, "-")

#                         latex_code += f"{lang.replace('_','-')} & {quality} & {validity} & {perturbation} & {experiment} & {bleu} & {chrf2} & {ter} \\\\\n"
#                         latex_code += "\\hline\n"

#     latex_code += "\\end{tabular}\n"

#     with open(output_file, 'w') as file:
#         file.write(latex_code)

# def main():
#     import argparse

#     parser = argparse.ArgumentParser(description='Convert JSON evaluation data to a combined LaTeX table.')
#     parser.add_argument('-i', '--input_file', type=str, required=True, help='Input JSON file containing evaluation data.')
#     parser.add_argument('-o', '--output_file', type=str, required=True, help='Output file to save the combined LaTeX table.')

#     args = parser.parse_args()

#     # Read JSON data
#     with open(args.input_file, 'r') as file:
#         data = json.load(file)

#     # Convert JSON data to a combined LaTeX table
#     json_to_combined_latex_table(data, args.output_file)

# if __name__ == '__main__':
#     main()




"""
Scores are in a single table, but the experiments are not differentiated into their own rows.
"""
# import json
# import os

# def json_to_combined_latex_table(data, output_file):
#     latex_code = "\\begin{tabular}{|l|l|l|l|r|r|r|r|r|r|}\n"
#     latex_code += "\\hline\n"
#     latex_code += "Languages & Data Quality & Feature Validity & Perturbation Type & NLLB BLEU & NLLB chrF2 & NLLB TER & PERT BLEU & PERT chrF2 & PERT TER \\\\\n"
#     latex_code += "\\hline\n"

#     for lang, qualities in data.items():
#         for quality, validities in qualities.items():
#             for validity, perturbations in validities.items():
#                 for perturbation, metrics in perturbations.items():
#                     nllb_bleu = metrics.get("NLLB_BLEU", "-")
#                     nllb_chrf2 = metrics.get("NLLB_chrF2", "-")
#                     nllb_ter = metrics.get("NLLB_TER", "-")
#                     pert_bleu = metrics.get("PERT_BLEU", "-")
#                     pert_chrf2 = metrics.get("PERT_chrF2", "-")
#                     pert_ter = metrics.get("PERT_TER", "-")

#                     latex_code += f"{lang} & {quality} & {validity} & {perturbation} & {nllb_bleu} & {nllb_chrf2} & {nllb_ter} & {pert_bleu} & {pert_chrf2} & {pert_ter} \\\\\n"
#                     latex_code += "\\hline\n"

#     latex_code += "\\end{tabular}\n"

#     with open(output_file, 'w') as file:
#         file.write(latex_code)

# def main():
#     import argparse

#     parser = argparse.ArgumentParser(description='Convert JSON evaluation data to a combined LaTeX table.')
#     parser.add_argument('-i', '--input_file', type=str, required=True, help='Input JSON file containing evaluation data.')
#     parser.add_argument('-o', '--output_file', type=str, required=True, help='Output file to save the combined LaTeX table.')

#     args = parser.parse_args()

#     # Read JSON data
#     with open(args.input_file, 'r') as file:
#         data = json.load(file)

#     # Convert JSON data to a combined LaTeX table
#     json_to_combined_latex_table(data, args.output_file)

# if __name__ == '__main__':
#     main()




"""
Scores are split up in many different tables
"""
# import os
# import glob
# import json
# from collections import defaultdict

# import json
# import os

# def json_to_latex_table(data, output_file):
#     latex_code = ""

#     for lang, qualities in data.items():
#         for quality, validities in qualities.items():
#             for validity, perturbations in validities.items():
#                 latex_code += f"\\section*{{{lang} - {quality} - {validity}}}\n"
#                 for perturbation, metrics in perturbations.items():
#                     latex_code += f"\\subsection*{{{perturbation}}}\n"
#                     latex_code += "\\begin{tabular}{|l|r|r|r|}\n"
#                     latex_code += "\\hline\n"
#                     latex_code += " & NLLB & PERT \\\\\n"
#                     latex_code += "\\hline\n"
                    
#                     metric_names = set()
#                     for metric_key in metrics.keys():
#                         metric_name = metric_key.split('_')[-1]
#                         metric_names.add(metric_name)
                    
#                     for metric_name in sorted(metric_names):
#                         nllb_key = f"NLLB_{metric_name}"
#                         pert_key = f"PERT_{metric_name}"
#                         nllb_score = metrics.get(nllb_key, "-")
#                         pert_score = metrics.get(pert_key, "-")
#                         latex_code += f"{metric_name} & {nllb_score} & {pert_score} \\\\\n"
#                         latex_code += "\\hline\n"

#                     latex_code += "\\end{tabular}\n\n"

#     with open(output_file, 'w') as file:
#         file.write(latex_code)

# def main():
#     import argparse

#     parser = argparse.ArgumentParser(description='Convert JSON evaluation data to LaTeX tables.')
#     parser.add_argument('-i', '--input_file', type=str, required=True, help='Input JSON file containing evaluation data.')
#     parser.add_argument('-o', '--output_file', type=str, required=True, help='Output file to save LaTeX tables.')

#     args = parser.parse_args()

#     # Read JSON data
#     with open(args.input_file, 'r') as file:
#         data = json.load(file)

#     # Convert JSON data to LaTeX tables
#     json_to_latex_table(data, args.output_file)

# if __name__ == '__main__':
#     main()