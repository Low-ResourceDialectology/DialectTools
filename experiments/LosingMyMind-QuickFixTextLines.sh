#!/bin/bash
# Author: Christian "Doofnase" Schuler
#######################################
# Project: Any
# Fix some formatting issues such as linebreaks in textprocessing resulting in every second line empty in file.

# bash LosingMyMind-QuickFixTextLines.sh -i /media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/reason/all/test.bar -o /media/AllBlue/LanguageData/PREP/2024SchuMATh/Bavarian/clean/German/reason/all/test.bar -s '@@@' -t /media/AllBlue/TempData/temp.txt

# Function to remove empty lines and specific substrings, then save to a new file
input_file=""
output_file=""
substring=""
temp_file=""

# Function to print usage
usage() {
echo "Usage: $0 -i input_file -o output_file -s substring -t temp_file"
exit 1
}

# Parse command-line options
while getopts ":i:o:s:t:" opt; do
    case $opt in
        i)
            input_file=$OPTARG
            ;;
        o)
            output_file=$OPTARG
            ;;
        s)
            substring=$OPTARG
            ;;
        t)
            temp_file=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

# Check if input file exists
if [[ ! -f "$input_file" ]]; then
    echo "Input file does not exist."
    return 1
fi

# Remove empty lines and specific substrings, then save to the temporary file
grep -v '^$' "$input_file" | sed "s/$substring//g" > "$temp_file"

# Move the temporary file to the output file path
mv "$temp_file" "$output_file"

echo "Empty lines and '$substring' removed and saved to $output_file."


# ++++++++++++++++++++++++++++++++++++++++++++++
# Executable function "from anywhere" code below

# # Function to remove empty lines and specific substrings, then save to a new file
# remove_empty_lines_and_substrings() {
#     local input_file="$1"
#     local output_file="$2"
#     local substring="$3"


#     # Check if input file exists
#     if [[ ! -f "$input_file" ]]; then
#         echo "Input file does not exist."
#         return 1
#     fi

#     # Remove empty lines and specific substrings, then save to the output file
#     grep -v '^$' "$input_file" | sed "s/$substring//g" > "$output_file"

#     echo "Empty lines and '$substring' removed and saved to $output_file."
# }

# Usage example:
# remove_empty_lines_and_substrings input.txt output.txt '@@@'



# 1. Save the Function: Copy the above code and save it to a file, for example, remove_empty_lines.sh.
# 2. Make the Script Executable: Run the following command to make the script executable.
#     chmod +x remove_empty_lines.sh
# 3. Source the Script in Your Shell: To use the function directly from your terminal, you need to source the script.
#     source ./remove_empty_lines.sh
# 4. Call the Function: You can now call the remove_empty_lines function with your input and output file names.
#     remove_empty_lines input.txt output.txt
