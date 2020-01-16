#! /bin/bash
# name-files.sh 
#
# Usage: % name-files.sh <input_dir> <output_dir>
#
# TODO: Update docstring
# This script re-names files in the directories below the ``data/input/pills/``
# directory as ``<trial_number>.csv`` and puts them in ``data/output/pills/``,
# keeping the same directory structure: 
#   ``data/input/pills/<PID_num>-PID/<n_pills>-pills/``.
#
# The full path of output files is:
#   ``data/output/pills/<PID>/<n_pills/trial<num>.csv``.
#
# Author: Matt Sarmiento <msarmiento3@usfca.edu>
#


INPUT_DIR=$1
OUTPUT_DIR=$2

# Regex to match pill subdirectories
REGEX=".*[0-9]\{2\}-pills"
SUBDIRS=$(find $INPUT_DIR -type d -regex $REGEX)

# Loop over PID/pills subdirectories
for file in SUBDIRS/*;
do
    

