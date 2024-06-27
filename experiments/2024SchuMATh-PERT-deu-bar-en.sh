#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: MA-Thesis
# Apply replacement rules (lexicograpic | morphological | syntactical) on text to perturb it 

# Initialize variables and default values
for data_quality in naive clean ; do
    #data_quality="clean" # naive | clean | informed # → Change variable here for each "Phase"
    for feature_validity in guess reason ; do
        #feature_validity="reason" # guess | reason » authentic
        for perturbation_type in lex mor all ; do
            #perturbation_type="" # lex | mor | syn
            input_path="/media/AllBlue/LanguageData/PERTURBS"
            data_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/${data_quality}/English/German/NLLB" # TODO: Split up and make modular for data-sources and language pairs "/media/AllBlue/LanguageData/PREP/opustools/bar-de/naive"
            output_path="/media/AllBlue/LanguageData/EXPERIMENT/2024SchuMATh/Bavarian/${data_quality}/English/German/NLLB/Bavarian"
            current_dir="$(dirname "$0")"
            script_file="../launch/Perturbation_Application.sh"
            script_path="${current_dir}/${script_file}"

            # +++++++++++++++++++++++++++++++++++++++++++++++
            # German - Bavarian 
            src_lang="deu"
            src_name="German"
            trg_lang="bar"
            trg_name="Bavarian"
            data_file_extension="en"
            echo "Perturbing: ${src_name} into ${trg_name} - (${data_quality}, ${feature_validity})"

            bash "${script_path}" \
                -i "${input_path}/${src_name}/${trg_name}" \
                -d "${data_path}" \
                -o "${output_path}/${perturbation_type}" \
                -s "${src_lang}" \
                -a "${src_name}" \
                -t "${trg_lang}" \
                -b "${trg_name}" \
                -m "${perturbation_type}" \
                -n "${data_quality}" \
                -e "${data_file_extension}"
        done
    done
done

# TODO
#perturbation_type="syn"