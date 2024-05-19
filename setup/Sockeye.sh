#!/bin/bash
# Download parallel data for Sockeye
# Use: cd ./setup
#         bash Sockeye.sh "/media/AllBlue/LanguageData/DOWNLOAD/datasets/2015StanWMTl" "large" 
#         bash Sockeye.sh "/media/AllBlue/LanguageData/DOWNLOAD/datasets/2014StanWMTm" "medium" 
#         bash Sockeye.sh "/media/AllBlue/LanguageData/DOWNLOAD/datasets/2015StanIWSL" "small" 

# Server does not like me → 403 Forbidden . . . 
#--2024-05-18 17:22:39--  https://nlp.stanford.edu/projects/nmt/data/wmt14.en-de/newstest2015.de
#Resolving nlp.stanford.edu (nlp.stanford.edu)... 171.64.67.140
#Connecting to nlp.stanford.edu (nlp.stanford.edu)|171.64.67.140|:443... connected.
#HTTP request sent, awaiting response... 403 Forbidden
#2024-05-18 17:22:40 ERROR 403: Forbidden.


CURRENT="$PWD"

# First input argument
DATADIR="$1"

# Second input argument
SIZE="$2"


# The Stanford NLP Group's Neural Machine Translation → https://nlp.stanford.edu/projects/nmt/
if [[ "${SIZE}" == *"medium"* ]]; then
	# Download medium sized English-German data
	echo "Downloading data to: ${DATADIR}"
	mkdir "${DATADIR}" -p

	wget 'https://nlp.stanford.edu/projects/nmt/data/wmt14.en-de/train.en' -P ${DATADIR} -N
	wget 'https://nlp.stanford.edu/projects/nmt/data/wmt14.en-de/train.de' -P ${DATADIR} -N
	for YEAR in 2012 2013 2014 2015; do
		wget "https://nlp.stanford.edu/projects/nmt/data/wmt14.en-de/newstest${YEAR}.en" -P ${DATADIR} -N
		wget "https://nlp.stanford.edu/projects/nmt/data/wmt14.en-de/newstest${YEAR}.de" -P ${DATADIR} -N
	done
	
	CLEANDIR="${DATADIR/DOWNLOAD/CLEAN}"
	echo "Combine data files and store in: ${CLEANDIR}"
	mkdir "${CLEANDIR}" -p
	#cat newstest{2012,2013}.en >dev.en
	#cat newstest{2012,2013}.de >dev.de
	#cp newstest2014.en test.en
	#cp newstest2014.de test.de

	PREPDIR="${CLEANDIR/CLEAN/PREP}"
	echo "Preprocess data and store in: ${PREPDIR}"
	mkdir "${PREPDIR}" -p
fi




cd "$CURRENT"


