
import json
import os

# TODO: Select languages | datasources | ...
# TODO: Callable from outside (create a main.py ?)
# NOTE: For now just "all" as default

# NOTE: Due to inconsistencies among datasets and researcher, each repository will require a manual check-up first.

# TODO: Identify reoccurring patterns and create "cleaning classes" for each to streamline this process across multiple repositories.
# TODO: Create a "cleaning-config" file to store execution-information for this

def clean_github_repos(config_file_in='./config.json',
                       sources_file_in='./sources/github_cleaning.json',
                       data_root_dir_in='/media/AllBlue/LanguageData'):
    
    config_file = config_file_in
    sources_file = sources_file_in
    data_root_dir = f'{data_root_dir_in}/DOWNLOAD/githubrepos'

    # Default in function-head vs. input-paramter vs. config-file → Who should take precedence?
    # with open(config_file, 'r') as input_file:
    #     json_data = json.load(input_file)
    #     data_root_dir = json_data["data_root_dir"]

    """ Go through all downloaded repositories and clean if corresponding repo-key found in "cleaning-config" file """
    print(f'Script-under-construction.')



clean_github_repos()
