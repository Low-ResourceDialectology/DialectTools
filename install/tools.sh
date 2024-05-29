#!/bin/bash
# Install a (by name) specified list of tools into target directory
# bash /install/tools.sh "/media/AllBlue/LanguageData/TOOLS/" "spaCy Morfessor OpusTools" 

CURRENT="$PWD"

# Target directory for the tool to be installed to
TOOLDIR="$1"

# List of tools to be installed
TOOL="$2"

# Apertium → https://github.com/apertium
# Apertium Install → https://wiki.apertium.org/wiki/Installation
# Apertium Install core using packaging → https://wiki.apertium.org/wiki/Install_Apertium_core_using_packaging
if [[ "${TOOL}" == *"Apertium"* ]]; then
	echo "Installing ${TOOL}"
	echo "Note: If you get any errors such as uninstallable unmet dependencies, try updating your ubuntu to the latest normal version."
	cd "${TOOLDIR}"
	mkdir "./${TOOL}"
	cd "./${TOOL}"

	# Add the repository
	curl -sS https://apertium.projectjj.com/apt/install-nightly.sh | sudo bash

	echo "Installation requires the use of suda and should be done manually via:"
	echo "sudo apt-get -f install apertium-all-dev"
	echo "List all available language packages for Apertium via:"
	echo "apt search apertium"
	echo "Install language packages via:"
	echo "sudo apt-get install apertium-eng-deu"

	echo "Apertium Help:"
	echo "lt-proc"

	echo "Use Apertium to translate a sentence:"
	echo "'This is a test sentence' | apertium eo-en "

fi

# Argos Translate → https://github.com/argosopentech/argos-translate
# Argos Translate Files → https://github.com/LibreTranslate/argos-translate-files
if [[ "${TOOL}" == *"ArgosTranslate"* ]]; then
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	

    echo "Installing ${TOOL}"
	cd "${TOOLDIR}"
    git clone git@github.com:argosopentech/argos-translate.git ./${TOOL}
	cd ./${TOOL}
	pip install -e .
	# Install all translation packages
	argospm install translate
	
	# Separate github repository for Argos Translate Files
	cd "${TOOLDIR}"
	git clone git@github.com:LibreTranslate/argos-translate-files.git ./${TOOL}Files
	pip install argos-translate-files
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
    cd ./${TOOL}
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
	cd ./${TOOL}
	mkdir build
	cd build
	cmake ..
	make
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

# NLLB → https://github.com/facebookresearch/fairseq/tree/nllb
# ? Open-NLLB → https://github.com/gordicaleksa/Open-NLLB
if [[ "${TOOL}" == *"NLLB"* ]]; then
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
    pip install transformers
	pip install torch
    
	# TODO: Look into "Open-NLLB" for more development options (?)
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

# SacreBLEU → https://github.com/mjpost/sacreBLEU
if [[ "${TOOL}" == *"SacreBLEU"* ]]; then 
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
	git clone git@github.com:mjpost/sacrebleu.git ./${TOOL}
	
    pip install sacrebleu
fi

# Sockeye → https://github.com/awslabs/sockeye
# subword-nmt → https://github.com/rsennrich/subword-nmt
if [[ "${TOOL}" == *"Sockeye"* ]]; then 
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
	git clone git@github.com:awslabs/sockeye.git ./${TOOL}
	cd ./${TOOL}
    pip install --editable .

	pip install subword-nmt
	pip install tensorboard
	pip install tensorflow
fi

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

# Various Tools and Packages for Cleaning of Text Data
if [[ "${TOOL}" == *"TextCleaning"* ]]; then 
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
    pip install pandas
	pip install seaborn
	pip install numpy
	pip install scikit-learn
	pip install nltk
	pip install langid
fi

# TranslateLocally → https://github.com/XapaJIaMnu/translateLocally
if [[ "${TOOL}" == *"TranslateLocally"* ]]; then
	echo "Make sure to install the build dependencies prior to running the installation script below!"
	# sudo apt-get install -y libxkbcommon-x11-dev libpcre++-dev libvulkan-dev libgl1-mesa-dev qt6-base-dev qt6-base-dev-tools qt6-tools-dev qt6-tools-dev-tools qt6-l10n-tools qt6-translations-l10n libqt6svg6-dev libarchive-dev libpcre2-dev

    # echo "Installing ${TOOL}"
	# cd "${TOOLDIR}"
    # git clone git@github.com:XapaJIaMnu/translateLocally.git ./${TOOL}
	# cd ./${TOOL}
	# mkdir build
	# cd build
	# cmake ..
	# make -j5

	# To start the GUI, run:
	#./translateLocally

	echo "App starts and can be called via CLI- but any time I try to translate something, I get something like -Aborted (core dumped)- and get kicked out..."
fi


# Translate Shell → https://github.com/soimort/translate-shell
if [[ "${TOOL}" == *"TranslateShell"* ]]; then
	echo "Easy install on Ubuntu, just execute in terminal:"
	echo "sudo apt install translate-shell"

	echo "Alternatively: Download the self-contained executable and place it into your path via:"
	echo "wget git.io/trans"
	echo "and then:"
	echo "chmod +x ./trans"
fi



# KLPT → https://github.com/sinaahmadi/klpt
# Cyhunspell → https://pypi.org/project/cyhunspell/
# Hunspell → https://github.com/hunspell/hunspell
if [[ "${TOOL}" == *"KLPT"* ]]; then
	echo "ISSUE: Installing KLTP requires Cyhunspell, which requires Hunspell, which I could not get to work on my system..."
	
	# Part of error message:
	# Building wheel for cyhunspell (setup.py) ... error
  	#error: subprocess-exited-with-error  
  	#× python setup.py bdist_wheel did not run successfully.
  	#│ exit code: 1
  	#╰─> [257 lines of output]
      	#/media/AllBlue/LanguageData/TOOLS/vKLPT/lib/python3.10/site-packages/setuptools/dist.py:723: UserWarning: Usage of dash-separated 'description-file' will not be supported in future versions. Please use the underscore name 'description_file' instead

	#echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	#bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	#cd "${TOOLDIR}"
	#source "./v${TOOL}/bin/activate"	
	
    #echo "Installing ${TOOL}"

	# Cyhunspell requires hunspell → https://github.com/hunspell/hunspell
	# START OF PART TO BE COMMENTED OUT 
	# git clone git@github.com:hunspell/hunspell.git ./Hunspell
	# cd ./Hunspell
	# autoreconf -vfi
	# ./configure
	# make
	# echo "MANUAL PART OF INSTALLATION"
	# echo "Navigate to ${TOOLDIR}/Hunspell and execute: sudo make install"
	# echo "Navigate to ${TOOLDIR}/Hunspell and execute: sudo ldconfig"
	# echo "Open the /DialectTools/install/tools.sh file and comment out the lines for hunspell (above this very line)"
	# echo "Open the /DialectTools/install/tools.sh file and uncomment the lines for cyhunspell and kltp (below this very line)"
	# END OF PART TO BE COMMENTED OUT 

	# NLTK requires cyhunspell version >= 2.0.1 → https://pypi.org/project/cyhunspell/
	#pip install wheel
	#pip install cyhunspell
    #pip install klpt
fi

# Whisper → https://github.com/openai/whisper
if [[ "${TOOL}" == *"Whisper"* ]]; then 
	echo "Installing venv for ${TOOL} in: ${TOOLDIR}"
	bash create_venv.sh "${TOOL}" "${TOOLDIR}"

	cd "${TOOLDIR}"
	source "./v${TOOL}/bin/activate"	
	
    echo "Installing ${TOOL}"
	#git clone git@github.com:openai/whisper.git ./${TOOL}
	#cd ./${TOOL}
	#python3 ./setup.py
	
	pip install git+https://github.com/openai/whisper.git
fi


# URL
#if [[ "${TOOL}" == *"spaCy"* ]]; then
#fi



cd "$CURRENT"


