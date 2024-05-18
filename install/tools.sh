#!/bin/bash
# Install a (by name) specified list of tools into target directory
# Use: cd ./install
#         bash tools.sh "/media/AllBlue/LanguageData/TOOLS/" "spaCy Morfessor OpusTools" 

CURRENT="$PWD"

# First input argument
TOOLDIR="$1"

# NOTE: Does not work...
# TOOLDIRIN="${2:-$(echo "jq .data_root_dir ./../config.json")}"
# Check if the input path already points towards the "sub-directory" called /TOOLS
# if [[ "/TOOLS" != *"$TOOLDIRIN"* ]]; then
# 	TOOLDIR="${TOOLDIRIN}/TOOLS/"
# fi

# Second input argument
TOOL="$2"

# TODO: VENV as argument
#VENV="$2"

# spaCy is a library for advanced Natural Language Processing in Python and Cython. 
# https://pypi.org/project/spacy/
if [[ "${TOOL}" == *"spaCy"* ]]; then
	# Create venv for tool to be installed in
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	# Python packages inside default venv
	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"
	
    echo "Installing ${TOOL}"
    pip install -U pip setuptools wheel
    pip install -U 'spacy[cuda12x]'
    # Download a few default files for working with Chinese, English, and German data
    python -m spacy download zh_core_web_sm
    python -m spacy download en_core_web_sm
    python -m spacy download de_core_news_sm
fi

# Language Identification with Support for More Than 2000 Labels
# https://github.com/cisnlp/GlotLID
if [[ "${TOOL}" == *"GlotLID"* ]]; then
#elif [ "${TOOL}" = "GlotLID" ];
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
    git clone git@github.com:cisnlp/GlotLID.git ./${TOOL}
    pip install fasttext
    pip install huggingface_hub
fi

if [[ "${TOOL}" == *"Morfessor"* ]]; then
#elif [ "${TOOL}" = "Morfessor" ];
#then
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
    pip install morfessor
fi

if [[ "${TOOL}" == *"fairseq"* ]]; then
#elif [ "${TOOL}" = "fairseq" ];
#then
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
    #git clone https://github.com/pytorch/fairseq  # According to instructions(?)
    git clone git@github.com:facebookresearch/fairseq.git ./${TOOL}
    cd fairseq
    pip install --editable ./
    
    # Optional - TODO: Test
    #git clone https://github.com/NVIDIA/apex
	#cd apex
	#pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" \
  	#--global-option="--deprecated_fused_adam" --global-option="--xentropy" \
  	#--global-option="--fast_multihead_attn" ./
fi

# https://github.com/clab/fast_align
if [[ "${TOOL}" == *"fast_align"* ]]; then
#elif [ "${TOOL}" = "fast_align" ]; 
#then
	# TODO:    echo "Installing requirements for fast_align"
	# TODO:    sudo apt-get install libgoogle-perftools-dev libsparsehash-dev
    echo "Installing ${TOOL}"
	cd "${TOOLDIR}"
    git clone git@github.com:clab/fast_align.git ./${TOOL}
	cd ./fast_align
	mkdir build
	cd build
	cmake ..
	make
fi

# https://github.com/Helsinki-NLP/OpusTools/tree/master
if [[ "${TOOL}" == *"OpusTools"* ]]; then 
#elif [ "${TOOL}" = "OpusTools" ]; 
#then
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
    pip install opustools[all]
fi

# https://github.com/stanfordnlp/stanza?tab=readme-ov-file
if [[ "${TOOL}" == *"Stanza"* ]]; then 
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
	git clone git@github.com:stanfordnlp/stanza.git ./${TOOL}
	cd ./${TOOL}
    pip install -e .
fi

# URL
#if [[ "${TOOL}" == *"spaCy"* ]]; then
#fi

# URL
#if [[ "${TOOL}" == *"spaCy"* ]]; then
#fi



cd "$CURRENT"


