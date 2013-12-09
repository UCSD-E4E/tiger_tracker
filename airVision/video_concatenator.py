#!/usr/local/bin/python 

import argparse     
import datetime
import video_retriever
import tiger_log
import getPositives
import shutil
import os
import fcntl
import sys
import subprocess
import glob


######################################
# Global variables...
lock_file_handle_global = None
######################################


# Determine if another instance of this script is running.
# Parameters: path to the file that should be locked
# Return: True if another instance is running.  False otherwise.
def file_is_locked(file_path):
    global lock_file_handle_global
    lock_file_handle_global = open(file_path, 'w')
    try:
        fcntl.lockf(lock_file_handle_global, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return False
    except IOError:
        # another instance is running
        return True


# Given a directory, sort all the video files
# into temporal order.  Return the absolute paths
# to those files.
def get_and_sort(directory):
    all_files = glob.glob(directory + "/" + "*.ts")
    for i in range(0, len(all_files)):
        all_files[i] = os.path.basename(all_files[i])
    getPositives.sort_nicely(all_files)
    for i in range(0, len(all_files)):
        all_files[i] = directory + "/" + all_files[i]
    return all_files


# Given a  list of files, concatenate them
# with ffmpeg.  Put output file in specified
# destination directory.
def ffmpeg(all_files, dest_directory):    
    to_concat = "|".join(all_files)
    output_path = dest_directory + "/" + "aggregated_output.avi"
    cmd = 'ffmpeg -i "concat:' + to_concat + '" -y ' + output_path + ' -qscale 1' 
    print cmd
    ret_val = os.system(cmd)
    return ret_val



################
# "Main":
################

# Detemine if another instance of this script is already running
lock_file_path = '/var/lock/air_vision_concatenator.py'

# Exit if another instance is already running
if file_is_locked(lock_file_path):
    print 'Another instance is running. Exiting now.'
    sys.exit(0)

# select processed, but not concatenated directories
to_concatenate = tiger_log.select_dirs_with_pos_footage()

for item in to_concatenate:
    currently_processing = item[0]
    temporal_order = get_and_sort(currently_processing) # put clips in temporal order
    ret_val = ffmpeg(temporal_order, currently_processing) # write a concatenated clip
    if ret_val == 0:   
        os.system("rm " + currently_processing + "/*.ts") # clean up this directory
        tiger_log.update_concatenated_by_dir(currently_processing, 'Y') # mark this direcotry as concatenated














