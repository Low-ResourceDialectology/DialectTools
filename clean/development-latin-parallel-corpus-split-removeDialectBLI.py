

# Removing designated data entries according to fit evaluation based on DialectBLI

import os
import re
import math
import pathlib

# TODO: Input arguments for more versatility
src_l = 'bar'
trg_l = 'de'
date_of_experiment = '20240524'
clean_dir = f'/media/AllBlue/LanguageData/CLEAN/opustools/{src_l}-{trg_l}'
prep_dir = f'/media/AllBlue/LanguageData/PREP/opustools/{src_l}-{trg_l}/{date_of_experiment}'
src_file = f'{prep_dir}/{src_l}-all'
trg_file = f'{prep_dir}/{trg_l}-all'
testdev_dir = f'/media/AllBlue/LanguageData/PREP/2024SchuMATh-barL-Sock-deuL-DBLI-0001'
src_dev =  f'{testdev_dir}/dev.{src_l}'
src_test =  f'{testdev_dir}/test.{src_l}'
trg_dev =  f'{testdev_dir}/dev.{trg_l}u'
trg_test =  f'{testdev_dir}/test.{trg_l}u'

src_train_out = f'{prep_dir}/train.{src_l}'
trg_train_out = f'{prep_dir}/train.{trg_l}u'

# Read files into list as lines
src_lines = []
with open(src_file, 'r') as f:
    for line in f.readlines():
        src_lines.append(line.rstrip(" \n"))

src_dev_lines = []
with open(src_dev, 'r') as f:
    for line in f.readlines():
        src_dev_lines.append(line.rstrip(" \n"))

src_test_lines = []
with open(src_test, 'r') as f:
    for line in f.readlines():
        src_test_lines.append(line.rstrip(" \n"))

trg_lines = []
with open(trg_file, 'r') as f:
    for line in f.readlines():
        trg_lines.append(line.rstrip(" \n"))

trg_dev_lines = []
with open(trg_dev, 'r') as f:
    for line in f.readlines():
        trg_dev_lines.append(line.rstrip(" \n"))

trg_test_lines = []
with open(trg_test, 'r') as f:
    for line in f.readlines():
        trg_test_lines.append(line.rstrip(" \n"))

# Check no. of lines
print("Source Parallel Lines (naive): ", len(src_lines))
print("Target Parallel Lines (naive): ", len(trg_lines))
print("Source Parallel Lines (dev): ", len(src_dev_lines))
print("Target Parallel Lines (dev): ", len(trg_dev_lines))
print("Source Parallel Lines (test): ", len(src_test_lines))
print("Target Parallel Lines (test): ", len(trg_test_lines))
"""
Source Parallel Lines (naive):  77776
Target Parallel Lines (naive):  77776
Source Parallel Lines (dev):  1089
Target Parallel Lines (dev):  1089
Source Parallel Lines (test):  179
Target Parallel Lines (test):  179
"""

# print("Some Example Parallel Lines (naive): ")
# print(src_lines[100:101])
# print(trg_lines[100:101])
# print("Some Example Parallel Lines (dev): ")
# print(src_dev_lines[100:101])
# print(trg_dev_lines[100:101])
# print("Some Example Parallel Lines (test): ")
# print(src_test_lines[100:101])
# print(trg_test_lines[100:101])
"""
Some Example Parallel Lines: 

"""

for src_line,trg_line in zip(src_test_lines, trg_test_lines):
    for src_train_line, index in zip(src_lines, range(len(src_lines))):
        if src_line == src_train_line:
            # print(src_line)
            # print(src_lines[index])
            # print(trg_line)
            # print(trg_lines[index])
            # print("")
            src_lines.pop(index)
            trg_lines.pop(index)
print("Source Parallel Lines (dropped test): ", len(src_lines))
print("Target Parallel Lines (dropped test): ", len(trg_lines))
"""
Source Parallel Lines (dropped test):  76354
Target Parallel Lines (dropped test):  76354
"""

for src_line, trg_line in zip(src_dev_lines, trg_dev_lines):
    for src_train_line, index in zip(src_lines, range(len(src_lines))):
        if src_line == src_train_line:
            # print(src_line)
            # print(src_lines[index])
            # print(trg_line)
            # print(trg_lines[index])
            # print("")
            src_lines.pop(index)
            trg_lines.pop(index)
print("Source Parallel Lines (dropped dev): ", len(src_lines))
print("Target Parallel Lines (dropped dev): ", len(trg_lines))
"""
Source Parallel Lines (dropped dev):  76160
Target Parallel Lines (dropped dev):  76160
"""

with open(src_train_out, 'w') as f:
    for line in src_lines:
        f.write(line+'\n')
with open(trg_train_out, 'w') as f:
    for line in trg_lines:
        f.write(line+'\n')

