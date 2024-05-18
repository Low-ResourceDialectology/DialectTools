# Author: Christian "Doofnase" Schuler
#######################################

import argparse
import os
current_working_directory = os.getcwd()

import fasttext
from huggingface_hub import hf_hub_download

"""
Helper Functions
"""
# Check whether directory already exists and create if not
def dir_maker(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print("Folder %s created!" % path)
    else:
        print("Folder %s already exists" % path)

# Parse input argument for cache directory location
parser = argparse.ArgumentParser(description='Target directory for cache')
parser.add_argument('--dir', type=str, default=f'{current_working_directory}/tools/GlotLID')

args = parser.parse_args()
target_dir = args.dir

# Download model and get the model path
model_path = hf_hub_download(repo_id="cis-lmu/glotlid", filename="model.bin", cache_dir=cache_directory)
print("model path:", model_path)

