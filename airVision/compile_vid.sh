#!/bin/bash

<<<<<<< HEAD
# Filename: compile_list.sh 
# Description: Compiles a vid_paths.txt of paths to clips to be stitched
#              Requires passed in argument of directory path to video paths
# Command: ./file_list.sh path_name
=======
# Description: Concatenates video clips into a output video file containing
#              all positive tiger footage from a specific date

>>>>>>> b7bb1e4d11be43b8edbe604697ceaf64ac273137

# Compile list of video paths >> vid_paths.txt
#echo '...creating vid_paths.txt'
#for file in $1/*.ts; do 
#    echo "file '$f'" >> vid_paths.txt; 
#done
<<<<<<< HEAD
#ech '...vid_paths.txt created'
=======
#echo '...vid_paths.txt created'

>>>>>>> b7bb1e4d11be43b8edbe604697ceaf64ac273137

# Read in vid_paths.txt and call ffmpeg to concatenate video files
echo '...concatenating video files'
ffmpeg -f concat -i vid_paths.txt -c copy output.ts
<<<<<<< HEAD

=======
>>>>>>> b7bb1e4d11be43b8edbe604697ceaf64ac273137
