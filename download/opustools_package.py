import json
import os
import datetime
import opustools_pkg as opus

"""
Download text data and datasets.
Keep a log file of downloads and metadata.
"""

# Load configuration
with open("config.json", 'r') as config_file:
    config = json.load(config_file)

# Function to create the output directory based on the source language
def get_output_directory(source_lang):
    base_dir = config["output_dir"]
    return os.path.join(base_dir, source_lang)

# Function to generate a unique file name based on corpus, source, target, and release
def generate_file_name(corpus_name, source_lang, target_lang, release):
    return f"{corpus_name}-{release}-{source_lang}-{target_lang}"


# Function to download data and log the metadata
def download_opus_data(corpus_name, source_lang, target_lang, release):
    # Get the output directory based on the source language
    output_dir = get_output_directory(source_lang)
    os.makedirs(output_dir, exist_ok=True)

    # Generate the output file name
    file_name = generate_file_name(corpus_name, source_lang, target_lang, release)
    output_file_path = os.path.join(output_dir, file_name)
    
    # Create an OpusGet object to download the dataset
    opus_get = opus.OpusGet(
        source=source_lang,
        target=target_lang,
        directory=corpus_name,
        release=release,
        download_dir=output_file_path
    )

    # Download the dataset
    opus_get.download()
    # TODO: Fix TypeError: OpusGet.download() missing 3 required positional arguments: 'corpora', 'file_n', and 'total_size'
    # → Maybe something like: opus_get.download('OpenSubtitles', 'OpenSubtitles.en-de.txt', 2000)  # Example corpus and file name, adjust as needed
        

    # Log the download information
    log_file = config["log_file"]

    with open(log_file, 'a') as log:
        log.write(
            f"{datetime.datetime.now()}: Downloaded {corpus_name} - {source_lang} to {target_lang} (Release: {release}) in '{output_dir}'\n"
        )

    print(f"Downloaded {corpus_name} - {source_lang} to {target_lang} in '{output_dir}'")

    """ More sophisticated logging in the future """
    # Create log entry
    # log_entry = {}
    # log_entry["Corpus"] = corpus_name
    # log_entry["Source"] = source_lang
    # log_entry["Target"] = target_lang
    # log_entry["Release"] = release
    # log_entry["Directory"] = output_dir
    #
    # # Read previous log file
    # with open(log_file, 'r') as f:
    #     data = json.load(f)
    #
    # # TODO: Check for combinations of "Corpus Name" & "Source Language" & "Target Language" and then update the logs accordingly
    # # if entry in data: ...
    #
    # # Serializing json and write to file
    # json_object = json.dumps(data, indent=4)
    # with open(log_file, "w") as outfile:
    #     outfile.write(json_object)

# Example usage
corpus_name = 'Tatoeba'  # Change to desired corpus
source_lang = 'bar'  # Source language
target_lang = 'de'  # Target language
release = 'latest'  # Change to the desired release version
download_opus_data(corpus_name, source_lang, target_lang, release)
