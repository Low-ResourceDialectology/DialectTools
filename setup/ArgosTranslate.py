# Author: Christian "Doofnase" Schuler
#######################################

import argparse
import os
current_working_directory = os.getcwd()

import argostranslate.package
import argostranslate.translate

source_code = "en"
target_code = "es"

# Download and install Argos Translate package
# argostranslate.package.update_package_index()
# available_packages = argostranslate.package.get_available_packages()
# package_to_install = next(
#     filter(
#         lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
#     )
# )
# argostranslate.package.install_from_path(package_to_install.download())

# Translate
translatedText = argostranslate.translate.translate("The dwarf is digging a hole. The ant is digging a home.", source_code, target_code)
print(translatedText)
# '¡Hola Mundo!'
