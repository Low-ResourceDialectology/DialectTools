#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Evaluate the results of machine translation via reference files in sacreBLEU

# NOTE: Reference-data and test-data (after translation by NLLB)
# REFERENCE
# /EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB/test.en
# "Reference" of Bavarian text directly translated into English
# /EXPERIMENT/2024SchuMATh/bar-de/naive/reference/Bavarian/English/NLLB/test.en
# Phase 1: NAIVE & GUESS
# /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/all/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/lex/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/mor/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/all/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/lex/English/NLLB/test.en
# /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/mor/English/NLLB/test.en

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/evaluate/sacreBLEU.sh"

# Initialize variables and default values
input_path_ref=""
input_file_ref=""
input_path_inf=""
input_file_inf=""
output_path=""
output_file=""
metrics="bleu chrf ter"
precision="4"
options=""
data_quality="" # "clean" | "naive" | "informed"
feature_validity="" # "guess" | "reason" | "authentic"


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Temporary code to run very specific experiment conditions → Now with new "relaxed"

        # German Reference and Bavarian Reference
        # ++++++++++++++++++++++++++++++++++++++++++++
        # Evaluate basic differences between original Bavarian text compared to the aligned German text
        # input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/clean" 
        # input_file_ref="test.de"

        # # Evaluate the basic language variety differences
        # src_name="Bavarian"
        # src_lang="bar"
        # trg_name="German"
        # trg_lang="de"

        # echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
        # input_path_inf="/media/AllBlue/LanguageData/PREP/opustools/bar-de/clean"
        # input_file_inf="test.bar"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/none/none"
        # output_file="PERT.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"


        # # German Reference and perturbed Bavarian
        # # ++++++++++++++++++++++++++++++++++++++++++++
        # # Evaluate basic differences between perturbed Bavarian text compared to the aligned German text
        # input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/clean" 
        # input_file_ref="test.de"

        # # Evaluate the basic language variety differences
        # src_name="Bavarian"
        # src_lang="bar"
        # trg_name="German"
        # trg_lang="de"

        # echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
        # input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/relaxed/mor"
        # input_file_inf="test.bar"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/relaxed/mor"
        # output_file="PERT.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

        # echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
        # input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/reason/mor"
        # input_file_inf="test.bar"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/reason/mor"
        # output_file="PERT.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

        # echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
        # input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/guess/mor"
        # input_file_inf="test.bar"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/guess/mor"
        # output_file="PERT.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

        # echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
        # input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/reason/lex"
        # input_file_inf="test.bar"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/reason/lex"
        # output_file="PERT.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

# Bavarian Reference and perturbed German
# ++++++++++++++++++++++++++++++++++++++++++++
# Evaluate basic differences between perturbed German text compared to the aligned Bavarian text
        # input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/clean" 
        # input_file_ref="test.bar"

        # # Evaluate the basic language variety differences
        # src_name="German"
        # src_lang="de"
        # trg_name="Bavarian"
        # trg_lang="bar"

        # echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
        # input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/relaxed/mor"
        # input_file_inf="test.de"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/relaxed/mor"
        # output_file="PERT.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

        # echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
        # input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/reason/mor"
        # input_file_inf="test.de"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/reason/mor"
        # output_file="PERT.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

        # echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
        # input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/guess/mor"
        # input_file_inf="test.de"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/guess/mor"
        # output_file="PERT.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

        # echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
        # input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/German/clean/Bavarian/reason/lex"
        # input_file_inf="test.de"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/reason/lex"
        # output_file="PERT.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

# German Reference English translation and Bavarian Reference English translation

        # ++++++++++++++++++++++++++++++++++++++++++++
        # Evaluate Translation of the original Bavarian text compared to the translation of the aligned German text
        # for data_quality in clean; do # naive clean informed
        #     input_path_ref="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/${data_quality}/reference/German/English/NLLB" 
        #     input_file_ref="test.en"

        #     # Evaluate the translation of Bavarian (standardized) into English
        #     src_name="Bavarian"
        #     src_lang="bar"
        #     trg_name="German"
        #     trg_lang="de"
        #     translate_name="English"
        #     translate_lang="en"

        #     echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
        #     input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/${data_quality}/reference/Bavarian/English/NLLB"
        #     input_file_inf="test.en"
        #     #output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
        #     output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
        #     output_file="NLLB.txt"
        #     bash "${script_file}" \
        #         -a "${input_path_ref}" \
        #         -b "${input_file_ref}" \
        #         -c "${input_path_inf}" \
        #         -d "${input_file_inf}" \
        #         -e "${output_path}" \
        #         -f "${output_file}" \
        #         -h "${metrics}" \
        #         -i "${precision}" \
        #         -j "${options}" 
        # done

# German Reference English translation and perturbed Bavarian English translation

        # ++++++++++++++++++++++++++++++++++++++++++++
        # Evaluate Translation of the original Bavarian text compared to the translation of the aligned German text
        # input_path_ref="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/clean/reference/German/English/NLLB" 
        # input_file_ref="test.en"

        # # Evaluate the translation of Bavarian (standardized) into English
        # src_name="Bavarian"
        # src_lang="bar"
        # trg_name="German"
        # trg_lang="de"
        # translate_name="English"
        # translate_lang="en"

        # echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
        # input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/clean/German/relaxed/mor/English/NLLB"
        # input_file_inf="test.en"
        # #output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/relaxed/mor"
        # output_file="NLLB.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

        # echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
        # input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/clean/German/reason/mor/English/NLLB"
        # input_file_inf="test.en"
        # #output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/reason/mor"
        # output_file="NLLB.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

        # echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
        # input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/clean/German/reason/lex/English/NLLB"
        # input_file_inf="test.en"
        # #output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/reason/lex"
        # output_file="NLLB.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"

        # echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
        # input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/clean/German/guess/mor/English/NLLB"
        # input_file_inf="test.en"
        # #output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
        # output_path="/media/AllBlue/LanguageData/EVAL/2024SchuMATh/Pipeline-10/${src_name}/clean/guess/mor"
        # output_file="NLLB.txt"
        # bash "${script_file}" \
        #     -a "${input_path_ref}" \
        #     -b "${input_file_ref}" \
        #     -c "${input_path_inf}" \
        #     -d "${input_file_inf}" \
        #     -e "${output_path}" \
        #     -f "${output_file}" \
        #     -h "${metrics}" \
        #     -i "${precision}" \
        #     -j "${options}"





# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Temporary code to run very specific experiment conditions

# # ++++++++++++++++++++++++++++++++++++++++++++
# # Evaluate Translations
# for data_quality in clean; do # naive clean informed

#     # NOTE: Same reference file for all translations of the same data_quality below
#     input_path_ref="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/${data_quality}/reference/German/English/NLLB" 
#     input_file_ref="test.en"

#     # Evaluate the translation of Bavarian (standardized) into English
#     src_name="Bavarian"
#     src_lang="bar"
#     trg_name="German"
#     trg_lang="de"
#     translate_name="English"
#     translate_lang="en"

#     echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name} for data quality ${data_quality}";
#     for feature_validity in guess reason; do # guess reason authentic
#         for perturbation_type in lex mor all; do
#             input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}/${translate_name}/NLLB"
#             input_file_inf="test.en"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="NLLB.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done

#     # Evaluate the translation of German (dialectized) into English
#     src_name="German"
#     src_lang="de"
#     trg_name="Bavarian"
#     trg_lang="bar"
#     translate_name="English"
#     translate_lang="en"

#     echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name} for data quality ${data_quality}";
#     for feature_validity in guess reason; do # guess reason authentic
#         for perturbation_type in lex mor all; do
#             input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}/${translate_name}/NLLB"
#             input_file_inf="test.en"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="NLLB.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done




# # ++++++++++++++++++++++++++++++++++++++++++++
# # Evaluate Translation of the original Bavarian text compared to the aligned German text
# for data_quality in clean; do # naive clean informed
#     input_path_ref="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/${data_quality}/reference/German/English/NLLB" 
#     input_file_ref="test.en"

#     # Evaluate the translation of Bavarian (standardized) into English
#     src_name="Bavarian"
#     src_lang="bar"
#     trg_name="German"
#     trg_lang="de"
#     translate_name="English"
#     translate_lang="en"

#     echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
#     input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/${data_quality}/reference/Bavarian/English/NLLB"
#     input_file_inf="test.en"
#     output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
#     output_file="NLLB.txt"
#     bash "${script_file}" \
#         -a "${input_path_ref}" \
#         -b "${input_file_ref}" \
#         -c "${input_path_inf}" \
#         -d "${input_file_inf}" \
#         -e "${output_path}" \
#         -f "${output_file}" \
#         -h "${metrics}" \
#         -i "${precision}" \
#         -j "${options}" 
# done

# ++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++






# for data_quality in naive clean ; do
#         # ++++++++++++++++++++++++++++++++++++++++++++
#         # Evaluate basic differences between original Bavarian text compared to the aligned German text
#         input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/${data_quality}" 
#         input_file_ref="test.de"

#         # Evaluate the basic language variety differences
#         src_name="Bavarian"
#         src_lang="bar"
#         trg_name="German"
#         trg_lang="de"

#         echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
#         input_path_inf="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
#         input_file_inf="test.bar"
#         output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
#         output_file="PERT.txt"
#         bash "${script_file}" \
#             -a "${input_path_ref}" \
#             -b "${input_file_ref}" \
#             -c "${input_path_inf}" \
#             -d "${input_file_inf}" \
#             -e "${output_path}" \
#             -f "${output_file}" \
#             -h "${metrics}" \
#             -i "${precision}" \
#             -j "${options}"
# done



# for data_quality in naive clean; # naive clean informed
# do
#     # # ++++++++++++++++++++++++++++++++++++++++++++
#     # # Evaluate Perturbations (How close do we get to the other language variety?)
#     input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/${data_quality}" 
#     input_file_ref="test.de"
#     src_name="Bavarian"
#     src_lang="bar"
#     trg_name="German"
#     trg_lang="de"
#     echo "Evaluating perturbations via sacreBLEU for: ${src_name} to ${trg_name}";

#     for feature_validity in guess reason; # guess reason authentic
#     do
#         for perturbation_type in lex mor all;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}"
#             input_file_inf="test.${src_lang}"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="PERT.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done


#for data_quality in naive clean; # naive clean informed
# for data_quality in clean; # naive clean informed
# do
#     input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/${data_quality}" 
#     input_file_ref="test.de"
#     src_name="German"
#     src_lang="de"
#     trg_name="Bavarian"
#     trg_lang="bar"
#     echo "Evaluating perturbations via sacreBLEU for: ${src_name} to ${trg_name}";
#     for feature_validity in guess reason; # guess reason authentic
#     do
#         for perturbation_type in all lex mor;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}"
#             input_file_inf="test.${src_lang}"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="PERT.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Proper Code and Loops below




# NOTE: All in one for now and controlling the process via the for loop string-variables
# ++++++++++++++++++++++++++++++++++++++++++
# Phase 2 - 
#           Data-Quality: "clean" 
#           Feature-Validity: "guess" 
#           Perturbation-Type: "lex", "mor", "all"

# ++++++++++++++++++++++++++++++++++++++++++
# Phase 1 - 
#           Data-Quality: "naive" 
#           Feature-Validity: "guess" 
#           Perturbation-Type: "lex", "mor", "all"

# TODO: Control directory structure for different "feature validities" → Currently only considered for output, since everything is "guess"

# for data_quality in clean; # naive clean informed
# do
#     # ++++++++++++++++++++++++++++++++++++++++++++
#     # Evaluate basic differences between original Bavarian text compared to the aligned German text
#     input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/${data_quality}" 
#     input_file_ref="test.de"

#     # Evaluate the basic language variety differences
#     src_name="Bavarian"
#     src_lang="bar"
#     trg_name="German"
#     trg_lang="de"

#     echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
#     input_path_inf="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
#     input_file_inf="test.bar"
#     output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
#     output_file="PERT.txt"
#     bash "${script_file}" \
#         -a "${input_path_ref}" \
#         -b "${input_file_ref}" \
#         -c "${input_path_inf}" \
#         -d "${input_file_inf}" \
#         -e "${output_path}" \
#         -f "${output_file}" \
#         -h "${metrics}" \
#         -i "${precision}" \
#         -j "${options}" 
# done

# # ++++++++++++++++++++++++++++++++++++++++++++
# # Evaluate Perturbations (How close do we get to the other language variety?)

# input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/${data_quality}" 
# input_file_ref="test.de"
# src_name="Bavarian"
# src_lang="bar"
# trg_name="German"
# trg_lang="de"
# echo "Evaluating perturbations via sacreBLEU for: ${src_name} to ${trg_name}";

# for data_quality in clean; # naive clean informed
# do
#     for feature_validity in guess; # guess reason authentic
#     do
#         for perturbation_type in all lex mor;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}"
#             input_file_inf="test.${src_lang}"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="PERT.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done

# input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive" 
# input_file_ref="test.de"
# src_name="German"
# src_lang="de"
# trg_name="Bavarian"
# trg_lang="bar"
# echo "Evaluating perturbations via sacreBLEU for: ${src_name} to ${trg_name}";


# for data_quality in clean; # naive clean informed
# do
#     for feature_validity in guess; # guess reason authentic
#     do
#         for perturbation_type in all lex mor;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}"
#             input_file_inf="test.${src_lang}"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="PERT.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done



# # ++++++++++++++++++++++++++++++++++++++++++++
# # Evaluate Translation of the original Bavarian text compared to the aligned German text
# input_path_ref="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/clean/reference/German/English/NLLB" 
# input_file_ref="test.en"

# # Evaluate the translation of Bavarian (standardized) into English
# src_name="Bavarian"
# src_lang="bar"
# trg_name="German"
# trg_lang="de"
# translate_name="English"
# translate_lang="en"

# echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
# input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/clean/reference/Bavarian/English/NLLB"
# input_file_inf="test.en"
# output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/clean/none/none"
# output_file="NLLB.txt"
# bash "${script_file}" \
#     -a "${input_path_ref}" \
#     -b "${input_file_ref}" \
#     -c "${input_path_inf}" \
#     -d "${input_file_inf}" \
#     -e "${output_path}" \
#     -f "${output_file}" \
#     -h "${metrics}" \
#     -i "${precision}" \
#     -j "${options}" 


# # ++++++++++++++++++++++++++++++++++++++++++++
# # Evaluate Translations
# # NOTE: Same reference file for all translations below
# input_path_ref="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/clean/reference/German/English/NLLB" 
# input_file_ref="test.en"

# # Evaluate the translation of Bavarian (standardized) into English
# src_name="Bavarian"
# src_lang="bar"
# trg_name="German"
# trg_lang="de"
# translate_name="English"
# translate_lang="en"

# echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
# for data_quality in clean; # naive clean informed
# do
#     for feature_validity in guess; # guess reason authentic
#     do
#         for perturbation_type in all lex mor;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}/${translate_name}/NLLB"
#             input_file_inf="test.en"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="NLLB.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done

# # Evaluate the translation of German (dialectized) into English
# src_name="German"
# src_lang="de"
# trg_name="Bavarian"
# trg_lang="bar"
# translate_name="English"
# translate_lang="en"

# echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
# for data_quality in clean; # naive clean informed
# do
#     for feature_validity in guess; # guess reason authentic
#     do
#         for perturbation_type in all lex mor;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}/${translate_name}/NLLB"
#             input_file_inf="test.en"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="NLLB.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done















# ++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++
# Script in its initial execution during phase 1 


# # ++++++++++++++++++++++++++++++++++++++++++++
# # Evaluate basic differences between original Bavarian text compared to the aligned German text
# input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/${data_quality}" 
# input_file_ref="test.de"

# # Evaluate the translation of Bavarian (standardized) into English
# src_name="Bavarian"
# src_lang="bar"
# trg_name="German"
# trg_lang="de"

# echo "Evaluating basic difference of language varieties via sacreBLEU for: ${src_name} to ${trg_name}";
# input_path_inf="/media/AllBlue/LanguageData/PREP/opustools/bar-de/${data_quality}"
# input_file_inf="test.bar"
# output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/${data_quality}/none/none"
# output_file="PERT.txt"
# bash "${script_file}" \
#     -a "${input_path_ref}" \
#     -b "${input_file_ref}" \
#     -c "${input_path_inf}" \
#     -d "${input_file_inf}" \
#     -e "${output_path}" \
#     -f "${output_file}" \
#     -h "${metrics}" \
#     -i "${precision}" \
#     -j "${options}" 


# # ++++++++++++++++++++++++++++++++++++++++++++
# # Evaluate Perturbations (How close do we get to the other language variety?)

# input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/${data_quality}" 
# input_file_ref="test.de"
# src_name="Bavarian"
# src_lang="bar"
# trg_name="German"
# trg_lang="de"
# echo "Evaluating perturbations via sacreBLEU for: ${src_name} to ${trg_name}";

# for data_quality in naive; # naive clean informed
# do
#     for feature_validity in guess; # guess reason authentic
#     do
#         for perturbation_type in all lex mor;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}"
#             input_file_inf="test.${src_lang}"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="PERT.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done

# input_path_ref="/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive" 
# input_file_ref="test.de"
# src_name="German"
# src_lang="de"
# trg_name="Bavarian"
# trg_lang="bar"
# echo "Evaluating perturbations via sacreBLEU for: ${src_name} to ${trg_name}";


# for data_quality in naive; # naive clean informed
# do
#     for feature_validity in guess; # guess reason authentic
#     do
#         for perturbation_type in all lex mor;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}"
#             input_file_inf="test.${src_lang}"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="PERT.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done



# ++++++++++++++++++++++++++++++++++++++++++++
# Evaluate Translation of the original Bavarian text compared to the aligned German text
# input_path_ref="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB" 
# input_file_ref="test.en"

# # Evaluate the translation of Bavarian (standardized) into English
# src_name="Bavarian"
# src_lang="bar"
# trg_name="German"
# trg_lang="de"
# translate_name="English"
# translate_lang="en"

# echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
# input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/Bavarian/English/NLLB"
# input_file_inf="test.en"
# output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}/naive/none/none"
# output_file="NLLB.txt"
# bash "${script_file}" \
#     -a "${input_path_ref}" \
#     -b "${input_file_ref}" \
#     -c "${input_path_inf}" \
#     -d "${input_file_inf}" \
#     -e "${output_path}" \
#     -f "${output_file}" \
#     -h "${metrics}" \
#     -i "${precision}" \
#     -j "${options}" 


# # ++++++++++++++++++++++++++++++++++++++++++++
# # Evaluate Translations
# # NOTE: Same reference file for all translations below
# input_path_ref="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB" 
# input_file_ref="test.en"

# # Evaluate the translation of Bavarian (standardized) into English
# src_name="Bavarian"
# src_lang="bar"
# trg_name="German"
# trg_lang="de"
# translate_name="English"
# translate_lang="en"

# echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
# for data_quality in naive; # naive clean informed
# do
#     for feature_validity in guess; # guess reason authentic
#     do
#         for perturbation_type in all lex mor;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}/${translate_name}/NLLB"
#             input_file_inf="test.en"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="NLLB.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done

# # Evaluate the translation of German (dialectized) into English
# src_name="German"
# src_lang="de"
# trg_name="Bavarian"
# trg_lang="bar"
# translate_name="English"
# translate_lang="en"

# echo "Evaluating machine translation via sacreBLEU for: ${src_name} to ${translate_name}";
# for data_quality in naive; # naive clean informed
# do
#     for feature_validity in guess; # guess reason authentic
#     do
#         for perturbation_type in all lex mor;
#         do
#             input_path_inf="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}/${translate_name}/NLLB"
#             input_file_inf="test.en"
#             output_path="/media/AllBlue/LanguageData/LOGS/2024SchuMATh/Pipeline-10/${src_name}_${trg_name}/${data_quality}/${feature_validity}/${perturbation_type}"
#             output_file="NLLB.txt"
#             bash "${script_file}" \
#                 -a "${input_path_ref}" \
#                 -b "${input_file_ref}" \
#                 -c "${input_path_inf}" \
#                 -d "${input_file_inf}" \
#                 -e "${output_path}" \
#                 -f "${output_file}" \
#                 -h "${metrics}" \
#                 -i "${precision}" \
#                 -j "${options}" 
#         done
#     done
# done





