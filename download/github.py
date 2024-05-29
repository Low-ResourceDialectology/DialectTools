
import json
import os

# TODO: Select languages | datasources | ...
# TODO: Callable from outside (create a main.py ?)
# NOTE: For now just "all" as default

def download_github_repos(config_file_in='./config.json',
                          sources_file_in='./sources/github.json',
                          data_root_dir_in='/media/AllBlue/LanguageData'):
    
    config_file = config_file_in
    sources_file = sources_file_in
    data_root_dir = f'{data_root_dir_in}/DOWNLOAD/githubrepos'

    # Default in function-head vs. input-paramter vs. config-file → Who should take precedence?
    # with open(config_file, 'r') as input_file:
    #     json_data = json.load(input_file)
    #     data_root_dir = json_data["data_root_dir"]


    """ # Example tuples of repository link and target directory
        github_repos_directions = [
            "git@github.com:mainlp/dialect-BLI.git /2023ArteDial",
            "git@github.com:sinaahmadi/CORDI.git /2024AhmaCORD"
        ]
    """

    """ Read github repository information and target directory from json file """
    with open(sources_file, 'r') as input_file:
        json_data = json.load(input_file)
        github_repos_directions = json_data["githubrepos"]


    """ # Entries of githubrepos such that
        "2024AhmaCORD":{
            "URL":"https://github.com/sinaahmadi/CORDI",
            "Authors":"Ahmadi, Sina and Q. Jaff, Daban and Ibn Alam, Md Mahfuz and Anastasopoulos, Antonios",
            "Publications":[
                "Language and Speech Technology for {Central Kurdish} Varieties":"URL_or_DOI"
            ],
            "Languages":["ckb"]
        }
    """

    for repo_dir in github_repos_directions.keys(): # → "2024AhmaCORD"
        url = github_repos_directions[repo_dir]['URL'] # → "https://github.com/sinaahmadi/CORDI"
        user_name = url.split('github.com/')[1].split('/')[0] # → "sinaahmadi"
        repo_name = url.split('github.com/')[1].split('/')[1] # → "CORDI"
        os.system(f'git clone git@github.com:{user_name}/{repo_name}.git {data_root_dir}/{repo_dir}')
        # → git clone git@github.com:sinaahmadi/CORDI.git /media/AllBlue/LanguageData/DOWNLOAD/githubrepos/2024AhmaCORD

download_github_repos()
