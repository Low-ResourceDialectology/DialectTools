#!/bin/bash
# Install all selected tools into target directory
# bash ./install/install_all.sh 
# bash ./install/install_all.sh -d /media/AllBlue/LanguageData
# bash ./install/install_all.sh -t OpusTools Stanza
# bash ./install/install_all.sh -d /media/AllBlue/LanguageData -t ArgosTranslate fairseq fast_align GlotLID KLPT Morfessor NLLB OpusTools SacreBLEU Sockeye spaCy Stanza TextCleaning TranslateLocally Whisper

# TODO: Function that tests if already installed- Then only update?

# TODO: Replace the manual installations → How safe is it to try "sudo installs" via a bash script?

# Function to read config file
read_config() {
    local script_dir="$(dirname "$0")"
    local config_file="$script_dir/config.txt"
    source "$config_file"
}

# Function to perform installations
perform_installations() {
    local script_dir="$(dirname "$0")"
    local target_dir="$1"
    shift
    local tools=("$@")

    # Your operations here
    echo "Performing installations in $target_dir/TOOLS for list of tools:"
    for tool_name in "${tools[@]}"; do
        echo "#### ${tool_name} ####"
        bash "${script_dir}"/tools.sh "${target_dir}/TOOLS" "${tool_name}"
    done
}

# Main function
main() {
    local target_dir=""
    local tools=()
    read_config

    # Parse command line arguments
    while getopts ":d:t:" opt; do
        case $opt in
            d) target_dir="$OPTARG" ;;
            t) tools+=("$OPTARG") ;;
            \?) echo "Invalid option: -$OPTARG" >&2 ;;
        esac
    done
    shift $((OPTIND - 1))

    # If no target directory or string list provided, read from config
    if [ -z "$target_dir" ] || [ ${#tools[@]} -eq 0 ]; then
        target_dir="$data_root_dir"
        tools=($tool_list)
    fi

    # Installing tools
    perform_installations "$target_dir" "${tools[@]}"
}

# Call main function
main "$@"

