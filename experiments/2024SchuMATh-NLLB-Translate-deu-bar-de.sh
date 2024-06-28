#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Translate standard and dialect text to English

current_dir="$(dirname "$0")"
script_file="$current_dir/../function/translate/NLLB.sh"

input_file="test"
output_file="test"
author_id="facebook"
model_id="nllb-200-3.3B"
model_name="3.3B"

experiment="Baseline-Preprocess-Postprocess"

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Temporary code to run very specific experiment conditions

data_quality="clean"
feature_validity="guess"
perturbation_type="mor"
experiment="baseline"

# Translate German text to English
src_name="Bavarian"
src_lang="bar"

trg_name="German"
trg_lang="de"
input_code="deu_Latn"

translate_name="English"
translate_lang="en"
output_code="eng_Latn"

input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${feature_validity}/${perturbation_type}"
output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${feature_validity}/${perturbation_type}/${translate_name}/NLLB"

echo "Translating ${input_file} via ${model_id} from ${trg_name} to ${translate_name}"; 
echo "${script_file}" \
    -a "${input_path}" \
    -b "${input_file}" \
    -c "${trg_lang}" \
    -d "${input_code}" \
    -e "${output_path}" \
    -f "${output_file}" \
    -g "${translate_lang}" \
    -h "${output_code}" \
    -i "${experiment}" \
    -j "${author_id}" \
    -k "${model_id}" \
    -l "${model_name}"
bash "${script_file}" \
    -a "${input_path}" \
    -b "${input_file}" \
    -c "${trg_lang}" \
    -d "${input_code}" \
    -e "${output_path}" \
    -f "${output_file}" \
    -g "${translate_lang}" \
    -h "${output_code}" \
    -i "${experiment}" \
    -j "${author_id}" \
    -k "${model_id}" \
    -l "${model_name}"





# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Proper Code and Loops below

# for data_set in test ; do # dev train ; do
#     input_file="${data_set}"
#     output_file="${data_set}"

#     for data_quality in clean naive ; do

#         # # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         # # REFERENCE data (Original Bavarian and German text each into English)

#         # # Translate Bavarian text to English
#         # src_name="Bavarian"
#         # src_lang="bar"

#         # trg_name="German"
#         # trg_lang="de"
#         # input_code="deu_Latn"

#         # translate_name="English"
#         # translate_lang="en"
#         # output_code="eng_Latn"

#         # input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
#         # output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${src_name}/${translate_name}/NLLB"

#         # echo "Translating ${input_file} via ${model_id} from ${src_lang} to ${translate_lang}"; 
#         # bash "${script_file}" \
#         #     -a ${input_path} \
#         #     -b ${input_file} \
#         #     -c ${src_lang} \
#         #     -d ${input_code} \
#         #     -e ${output_path} \
#         #     -f ${output_file} \
#         #     -g ${trg_lang} \
#         #     -h ${output_code} \
#         #     -i ${experiment} \
#         #     -j ${author_id} \
#         #     -k ${model_id} \
#         #     -l ${model_name}

#         # # Translate German text to English
#         # src_name="Bavarian"
#         # src_lang="bar"

#         # trg_name="German"
#         # trg_lang="de"
#         # input_code="deu_Latn"

#         # translate_name="English"
#         # translate_lang="en"
#         # output_code="eng_Latn"

#         # input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
#         # output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${trg_name}/${translate_name}/NLLB"

#         # echo "Translating ${input_file} via ${model_id} from ${trg_lang} to ${translate_lang}"; 
#         # bash "${script_file}" \
#         #     -a ${input_path} \
#         #     -b ${input_file} \
#         #     -c ${trg_lang} \
#         #     -d ${input_code} \
#         #     -e ${output_path} \
#         #     -f ${output_file} \
#         #     -g ${trg_lang} \
#         #     -h ${output_code} \
#         #     -i ${experiment} \
#         #     -j ${author_id} \
#         #     -k ${model_id} \
#         #     -l ${model_name}

#         for feature_validity in reason guess ; do
#             # ++++++++++++++++++++++++++++++++++++++++++
#             # Actual "Phase data" for different combinations of "data_quality" and "feature_validity"

#             #data_quality="clean" # "naive" | "clean" | "informed"
#             experiment="baseline" # "preprocessing" | "postprocessing"

#             for perturbation_type in all ; do # lex mor all ; do
#                 # Translate Bavarian text to English
#                 src_name="Bavarian"
#                 src_lang="bar"

#                 trg_name="German"
#                 trg_lang="de"
#                 input_code="deu_Latn"

#                 translate_name="English"
#                 translate_lang="en"
#                 output_code="eng_Latn"
#                 input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}"
#                 output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${feature_validity}/${perturbation_type}/${translate_name}/NLLB"

#                 echo "Translating ${input_file} via ${model_id} from ${src_name} to ${translate_name}"; 
#                 bash "${script_file}" \
#                     -a ${input_path} \
#                     -b ${input_file} \
#                     -c ${src_lang} \
#                     -d ${input_code} \
#                     -e ${output_path} \
#                     -f ${output_file} \
#                     -g ${translate_lang} \
#                     -h ${output_code} \
#                     -i ${experiment} \
#                     -j ${author_id} \
#                     -k ${model_id} \
#                     -l ${model_name}

#                 # Translate German text to English
#                 src_name="Bavarian"
#                 src_lang="bar"

#                 trg_name="German"
#                 trg_lang="de"
#                 input_code="deu_Latn"

#                 translate_name="English"
#                 translate_lang="en"
#                 output_code="eng_Latn"

#                 input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${feature_validity}/${perturbation_type}"
#                 output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${feature_validity}/${perturbation_type}/${translate_name}/NLLB"

#                 echo "Translating ${input_file} via ${model_id} from ${trg_name} to ${translate_name}"; 
#                 bash "${script_file}" \
#                     -a ${input_path} \
#                     -b ${input_file} \
#                     -c ${trg_lang} \
#                     -d ${input_code} \
#                     -e ${output_path} \
#                     -f ${output_file} \
#                     -g ${translate_lang} \
#                     -h ${output_code} \
#                     -i ${experiment} \
#                     -j ${author_id} \
#                     -k ${model_id} \
#                     -l ${model_name}
#             done
#         done
#     done
# done


# # NOTE: Due to time-constraints, the "re-translation" of the following parts will be pushed to the end of the script.
# #       I actually already translated these- but as is custom → Might be best to redo "all in one neat package" prior to the end?
# #       Let's see what the speed of the GPU has to offer!

# for data_set in test dev train ; do
#     input_file="${data_set}"
#     output_file="${data_set}"

#     for data_quality in clean naive ; do

#         # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         # REFERENCE data (Original Bavarian and German text each into English)

#         # Translate Bavarian text to English
#         src_name="Bavarian"
#         src_lang="bar"

#         trg_name="German"
#         trg_lang="de"
#         input_code="deu_Latn"

#         translate_name="English"
#         translate_lang="en"
#         output_code="eng_Latn"

#         input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
#         output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${src_name}/${translate_name}/NLLB"

#         echo "Translating ${input_file} via ${model_id} from ${src_lang} to ${translate_lang}"; 
#         bash "${script_file}" \
#             -a ${input_path} \
#             -b ${input_file} \
#             -c ${src_lang} \
#             -d ${input_code} \
#             -e ${output_path} \
#             -f ${output_file} \
#             -g ${trg_lang} \
#             -h ${output_code} \
#             -i ${experiment} \
#             -j ${author_id} \
#             -k ${model_id} \
#             -l ${model_name}

#         # Translate German text to English
#         src_name="Bavarian"
#         src_lang="bar"

#         trg_name="German"
#         trg_lang="de"
#         input_code="deu_Latn"

#         translate_name="English"
#         translate_lang="en"
#         output_code="eng_Latn"

#         input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
#         output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${trg_name}/${translate_name}/NLLB"

#         echo "Translating ${input_file} via ${model_id} from ${trg_lang} to ${translate_lang}"; 
#         bash "${script_file}" \
#             -a ${input_path} \
#             -b ${input_file} \
#             -c ${trg_lang} \
#             -d ${input_code} \
#             -e ${output_path} \
#             -f ${output_file} \
#             -g ${trg_lang} \
#             -h ${output_code} \
#             -i ${experiment} \
#             -j ${author_id} \
#             -k ${model_id} \
#             -l ${model_name}
#     done
# done




# Experiment Code from prior to 27.06.2024 found below

# ++++++++++++++++++++++++++++++++++++++++++
# Phase 2 - 
#           Data-Quality: "clean" 
#           Feature-Validity: "guess" 
#           Perturbation-Type: "lex", "mor", "all"


# NOTE: Translating data from → to
# REFERENCE
# /PREP/opustools/bar-de/clean/test.de → /EXPERIMENT/2024SchuMATh/bar-de/clean/reference/German/English/NLLB/test.en
# /PREP/opustools/bar-de/clean/test.bar → /EXPERIMENT/2024SchuMATh/bar-de/clean/reference/Bavarian/English/NLLB/test.en
# Phase 1: NAIVE & GUESS
# /PREP/2024SchuMATh/German/clean/Bavarian/all/test.de → /EXPERIMENT/2024SchuMATh/German/clean/Bavarian/all/English/NLLB/test.en
# /PREP/2024SchuMATh/German/clean/Bavarian/lex/test.de → /EXPERIMENT/2024SchuMATh/German/clean/Bavarian/lex/English/NLLB/test.en
# /PREP/2024SchuMATh/German/clean/Bavarian/mor/test.de → /EXPERIMENT/2024SchuMATh/German/clean/Bavarian/mor/English/NLLB/test.en
# /PREP/2024SchuMATh/Bavarian/clean/German/all/test.de → /EXPERIMENT/2024SchuMATh/Bavarian/clean/German/all/English/NLLB/test.en
# /PREP/2024SchuMATh/Bavarian/clean/German/lex/test.de → /EXPERIMENT/2024SchuMATh/Bavarian/clean/German/lex/English/NLLB/test.en
# /PREP/2024SchuMATh/Bavarian/clean/German/mor/test.de → /EXPERIMENT/2024SchuMATh/Bavarian/clean/German/mor/English/NLLB/test.en

# # ++++++++++++++++++++++++++++++++++++++++++
# # REFERENCE data

# data_quality="clean" # "naive" | "clean" | "informed"
# experiment="baseline" # "preprocessing" | "postprocessing"

# # Translate Bavarian text to English
# src_name="Bavarian"
# src_lang="bar"

# trg_name="German"
# trg_lang="de"
# input_code="deu_Latn"

# translate_name="English"
# translate_lang="en"
# output_code="eng_Latn"

# input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
# output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${src_name}/${translate_name}/NLLB"

# echo "Translating ${input_file} via ${model_id} from ${src_lang} to ${translate_lang}"; 
# bash "${script_file}" \
#     -a ${input_path} \
#     -b ${input_file} \
#     -c ${src_lang} \
#     -d ${input_code} \
#     -e ${output_path} \
#     -f ${output_file} \
#     -g ${trg_lang} \
#     -h ${output_code} \
#     -i ${experiment} \
#     -j ${author_id} \
#     -k ${model_id} \
#     -l ${model_name}


# # Translate German text to English
# src_name="Bavarian"
# src_lang="bar"

# trg_name="German"
# trg_lang="de"
# input_code="deu_Latn"

# translate_name="English"
# translate_lang="en"
# output_code="eng_Latn"

# input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
# output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${trg_name}/${translate_name}/NLLB"

# echo "Translating ${input_file} via ${model_id} from ${trg_lang} to ${translate_lang}"; 
# bash "${script_file}" \
#     -a ${input_path} \
#     -b ${input_file} \
#     -c ${trg_lang} \
#     -d ${input_code} \
#     -e ${output_path} \
#     -f ${output_file} \
#     -g ${trg_lang} \
#     -h ${output_code} \
#     -i ${experiment} \
#     -j ${author_id} \
#     -k ${model_id} \
#     -l ${model_name}



# # ++++++++++++++++++++++++++++++++++++++++++
# # Actual "Phase data"

# data_quality="clean" # "naive" | "clean" | "informed"
# experiment="baseline" # "preprocessing" | "postprocessing"

# for perturbation_type in lex mor all;
# do
#     # Translate Bavarian text to English
#     src_name="Bavarian"
#     src_lang="bar"

#     trg_name="German"
#     trg_lang="de"
#     input_code="deu_Latn"

#     translate_name="English"
#     translate_lang="en"
#     output_code="eng_Latn"
#     input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}"
#     output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}/${translate_name}/NLLB"

#     echo "Translating ${input_file} via ${model_id} from ${src_name} to ${translate_name}"; 
#     bash "${script_file}" \
#         -a ${input_path} \
#         -b ${input_file} \
#         -c ${src_lang} \
#         -d ${input_code} \
#         -e ${output_path} \
#         -f ${output_file} \
#         -g ${translate_lang} \
#         -h ${output_code} \
#         -i ${experiment} \
#         -j ${author_id} \
#         -k ${model_id} \
#         -l ${model_name}

#     # Translate German text to English
#     src_name="Bavarian"
#     src_lang="bar"

#     trg_name="German"
#     trg_lang="de"
#     input_code="deu_Latn"

#     translate_name="English"
#     translate_lang="en"
#     output_code="eng_Latn"

#     input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${perturbation_type}"
#     output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${perturbation_type}/${translate_name}/NLLB"

#     echo "Translating ${input_file} via ${model_id} from ${trg_name} to ${translate_name}"; 
#     bash "${script_file}" \
#         -a ${input_path} \
#         -b ${input_file} \
#         -c ${trg_lang} \
#         -d ${input_code} \
#         -e ${output_path} \
#         -f ${output_file} \
#         -g ${translate_lang} \
#         -h ${output_code} \
#         -i ${experiment} \
#         -j ${author_id} \
#         -k ${model_id} \
#         -l ${model_name}
# done




# ++++++++++++++++++++++++++++++++++++++++++
# Phase 1 - 
#           Data-Quality: "naive" 
#           Feature-Validity: "guess" 
#           Perturbation-Type: "lex", "mor", "all"

# NOTE: Translating data from → to
# REFERENCE
# /PREP/opustools/bar-de/naive/test.de → /EXPERIMENT/2024SchuMATh/bar-de/naive/reference/German/English/NLLB/test.en
# /PREP/opustools/bar-de/naive/test.bar → /EXPERIMENT/2024SchuMATh/bar-de/naive/reference/Bavarian/English/NLLB/test.en
# Phase 1: NAIVE & GUESS
# /PREP/2024SchuMATh/German/naive/Bavarian/all/test.de → /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/all/English/NLLB/test.en
# /PREP/2024SchuMATh/German/naive/Bavarian/lex/test.de → /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/lex/English/NLLB/test.en
# /PREP/2024SchuMATh/German/naive/Bavarian/mor/test.de → /EXPERIMENT/2024SchuMATh/German/naive/Bavarian/mor/English/NLLB/test.en
# /PREP/2024SchuMATh/Bavarian/naive/German/all/test.de → /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/all/English/NLLB/test.en
# /PREP/2024SchuMATh/Bavarian/naive/German/lex/test.de → /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/lex/English/NLLB/test.en
# /PREP/2024SchuMATh/Bavarian/naive/German/mor/test.de → /EXPERIMENT/2024SchuMATh/Bavarian/naive/German/mor/English/NLLB/test.en

# ++++++++++++++++++++++++++++++++++++++++++
# REFERENCE data

# data_quality="naive" # "clean" | "informed"
# experiment="baseline" # "preprocessing" | "postprocessing"

# # Translate Bavarian text to English
# src_name="Bavarian"
# src_lang="bar"

# trg_name="German"
# trg_lang="de"
# input_code="deu_Latn"

# translate_name="English"
# translate_lang="en"
# output_code="eng_Latn"

# input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
# output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${src_name}/${translate_name}/NLLB"

# echo "Translating ${input_file} via ${model_id} from ${src_lang} to ${translate_lang}"; 
# bash "${script_file}" \
#     -a ${input_path} \
#     -b ${input_file} \
#     -c ${src_lang} \
#     -d ${input_code} \
#     -e ${output_path} \
#     -f ${output_file} \
#     -g ${trg_lang} \
#     -h ${output_code} \
#     -i ${experiment} \
#     -j ${author_id} \
#     -k ${model_id} \
#     -l ${model_name}


# # Translate German text to English
# src_name="Bavarian"
# src_lang="bar"

# trg_name="German"
# trg_lang="de"
# input_code="deu_Latn"

# translate_name="English"
# translate_lang="en"
# output_code="eng_Latn"

# input_path="/media/AllBlue/LanguageData/PREP/opustools/${src_lang}-${trg_lang}/${data_quality}"
# output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_lang}-${trg_lang}/${data_quality}/reference/${trg_name}/${translate_name}/NLLB"

# echo "Translating ${input_file} via ${model_id} from ${trg_lang} to ${translate_lang}"; 
# bash "${script_file}" \
#     -a ${input_path} \
#     -b ${input_file} \
#     -c ${trg_lang} \
#     -d ${input_code} \
#     -e ${output_path} \
#     -f ${output_file} \
#     -g ${trg_lang} \
#     -h ${output_code} \
#     -i ${experiment} \
#     -j ${author_id} \
#     -k ${model_id} \
#     -l ${model_name}



# # ++++++++++++++++++++++++++++++++++++++++++
# # Actual "Phase data"

# data_quality="naive" # "clean" | "informed"
# experiment="baseline" # "preprocessing" | "postprocessing"

# for perturbation_type in lex mor all;
# do
#     # Translate Bavarian text to English
#     src_name="Bavarian"
#     src_lang="bar"

#     trg_name="German"
#     trg_lang="de"
#     input_code="deu_Latn"

#     translate_name="English"
#     translate_lang="en"
#     output_code="eng_Latn"
#     input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}"
#     output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${src_name}/${data_quality}/${trg_name}/${perturbation_type}/${translate_name}/NLLB"

#     echo "Translating ${input_file} via ${model_id} from ${src_name} to ${translate_name}"; 
#     bash "${script_file}" \
#         -a ${input_path} \
#         -b ${input_file} \
#         -c ${src_lang} \
#         -d ${input_code} \
#         -e ${output_path} \
#         -f ${output_file} \
#         -g ${translate_lang} \
#         -h ${output_code} \
#         -i ${experiment} \
#         -j ${author_id} \
#         -k ${model_id} \
#         -l ${model_name}

#     # Translate German text to English
#     src_name="Bavarian"
#     src_lang="bar"

#     trg_name="German"
#     trg_lang="de"
#     input_code="deu_Latn"

#     translate_name="English"
#     translate_lang="en"
#     output_code="eng_Latn"

#     input_path="/media/AllBlue/LanguageData/PREP/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${perturbation_type}"
#     output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/${trg_name}/${data_quality}/${src_name}/${perturbation_type}/${translate_name}/NLLB"

#     echo "Translating ${input_file} via ${model_id} from ${trg_name} to ${translate_name}"; 
#     bash "${script_file}" \
#         -a ${input_path} \
#         -b ${input_file} \
#         -c ${trg_lang} \
#         -d ${input_code} \
#         -e ${output_path} \
#         -f ${output_file} \
#         -g ${translate_lang} \
#         -h ${output_code} \
#         -i ${experiment} \
#         -j ${author_id} \
#         -k ${model_id} \
#         -l ${model_name}
# done


