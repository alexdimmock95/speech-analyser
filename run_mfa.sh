#!/bin/bash

acoustic_model="/Users/Jimdymock/Documents/Coding/personal_project/speech_analyser/MFA/acoustic/english_mfa.zip"
dictionary="/Users/Jimdymock/Documents/Coding/personal_project/speech_analyser/MFA/dictionary/english_mfa.dict"

input_dir="$1" # The folder containing the audio and transcription files
output_dir="$2" # The folder where the output will be saved

source /opt/anaconda3/etc/profile.d/conda.sh
conda activate mfa_env

echo "Checking input dir:"
ls -l "$input_dir"

echo "Checking file names and types:"
file "$input_dir"/*

mfa align "$input_dir" "$dictionary" "$acoustic_model" "$output_dir" --clean