#!/bin/bash

# Description: Concatenates video clips into a output video file containing
#              all positive tiger footage from a specific date


# Compile list of video paths >> vid_paths.txt
#echo '...creating vid_paths.txt'
#for file in $1/*.ts; do 
#    echo "file '$f'" >> vid_paths.txt; 
#done
#echo '...vid_paths.txt created'


# Read in vid_paths.txt and call ffmpeg to concatenate video files
echo '...concatenating video files'
ffmpeg -f concat -i vid_paths.txt -c copy output.ts
