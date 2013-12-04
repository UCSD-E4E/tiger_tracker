#!/bin/bash

# Filename: compile_list.sh 
# Description: Compiles a vid_paths.txt of paths to clips to be stitched
#              Requires passed in argument of directory path to video paths
# Command: ./file_list.sh path_name

# Compile list of video paths >> vid_paths.txt
#echo '...creating vid_paths.txt'
#for file in $1/*.ts; do 
#    echo "file '$f'" >> vid_paths.txt; 
#done
#ech '...vid_paths.txt created'

# Read in vid_paths.txt and call ffmpeg to concatenate video files
echo '...concatenating video files'
ffmpeg -f concat -i vid_paths.txt -c copy output.ts

