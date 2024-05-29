#!/bin/bash

echo "TODO: Make the script process a list of codes and not just a single one."

# Function to read config file
read_config() {
    local script_dir="$(dirname "$0")"
    local config_file="$script_dir/../config.txt"
    source "$config_file"
}

# Function to perform installations
perform_downloads() {
    local script_dir="$(dirname "$0")"
    local target_dir="$1/DOWNLOAD/wikidumps"
    shift
    local codes=("$@")
    dump_date="20240520"
    # Actual operations here
    echo "Check if newer dumps are available and change the date inside the script: download/wikipedia_dumps.sh"
    echo "Performing downloads to $target_dir/DOWNLOAD/wikidumps for list of language codes:"
    for CODE in "${codes[@]}"; do
        mkdir -p "${target_dir}/${CODE}"
        url="https://dumps.wikimedia.org/${CODE}wiki/${dump_date}/${CODE}wiki-${dump_date}-pages-meta-current.xml.bz2"
        wget -N "${url}" -P "${target_dir}/${CODE}"
    done
}
# All wiki dumps for language Dzongkha with code dz → https://dumps.wikimedia.org/dzwiki/20240520/
# URL of file to download for language Dzongkha with code dz → https://dumps.wikimedia.org/dzwiki/20240520/dzwiki-20240520-pages-meta-current.xml.bz2

# Main function
main() {
    local target_dir=""
    local codes=()
    read_config

    # Parse command line arguments
    while getopts ":d:l:" opt; do
        case $opt in
            d) target_dir="$OPTARG" ;;
            l) codes+=("$OPTARG") ;;
            \?) echo "Invalid option: -$OPTARG" >&2 ;;
        esac
    done
    shift $((OPTIND - 1))

    # If no target directory or string list provided, read from config
    if [ -z "$target_dir" ]; then
        target_dir="$data_root_dir"
    fi
    if [ ${#codes[@]} -eq 0 ]; then
        echo "No language code provided, defaulting to Dzongkha language code dz"
        codes+=('dz')
    fi

    # Downloading wikipedia dumps
    perform_downloads "$target_dir" "${codes[@]}"
}

# Call main function
main "$@"









# # Function to perform installations
# perform_installations() {
#     local script_dir="$(dirname "$0")"
#     local target_dir="$1"
#     shift
#     local tools=("$@")

#     # Your operations here
#     echo "Performing installations in $target_dir/TOOLS for list of tools:"
#     for tool_name in "${tools[@]}"; do
#         echo "#### ${tool_name} ####"
#         bash "${script_dir}"/tools.sh "${target_dir}/TOOLS" "${tool_name}"
#     done
# }


# # Main function
# main() {
#     # Parse command line arguments
#     while getopts ":l:" opt; do
#         case $opt in
#             l) language_codes="$OPTARG" ;;
#             \?) echo "Invalid option: -$OPTARG" >&2 ;;
#         esac
#     done
#     shift $((OPTIND - 1))

#     # If no target directory or string list provided, read from config
#     if [ -z "$target_dir" ]; then
#         target_dir="$data_root_dir"
#     fi
#     if [ ${#tools[@]} -eq 0 ]; then
#         tools=($tool_list)
#     fi

#     # Installing tools
#     perform_installations "$target_dir" "${tools[@]}"
# }

# # Call main function
# main "$@"