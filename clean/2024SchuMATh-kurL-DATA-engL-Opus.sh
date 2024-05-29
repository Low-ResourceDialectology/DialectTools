#!/bin/bash
# Clean Kurmanji data and prepare training with German and English aligned data


###############################################################################
# Preprocess and clean the text data
source /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate
python3 /media/CrazyProjects/LowResDialectology/DialectTools/clean/development-latin-parallel-corpus-split-kur.py


###############################################################################
# Split text data into train/dev/test
# NOTE: Currently evaluating (and developing) based on the DialectBLI data splits that distinguish between human-annotated and machine-annotated data
# → Remove data designated to be "Test" or "Dev" from the above preprocessed data
#source  /media/AllBlue/LanguageData/TOOLS/vTextCleaning/bin/activate
#python3 /media/CrazyProjects/LowResDialectology/DialectTools/clean/development-latin-parallel-corpus-split-removeDialectBLI.py


#####################################################
# End of data preprocessing, cleaning and splitting #
# Start of training and evaluation parts            #
#####################################################
