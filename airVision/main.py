#!/usr/local/bin/python 
# -*- coding: UTF-8 -*-
# ^ so we can print out "check" marks!

import argparse     
import datetime
import video_retriever
import tiger_log
import getPositives
import shutil
import os



# Write a log message to our output file.
# Params: to_log--the string with the message to log.
# file_name--name of the log file to write to
# verbose_arg--the command line arg; should the 
# message be written to stdout as well?
def log_message(to_log, file_name, verbose_arg):
    with open(file_name, "a") as log_file:
        log_file.write(to_log)    
    if verbose_arg == True:
        print to_log


def terminate_main(log_file, verbose):
    log_message("\n\nExiting at: " + str(datetime.datetime.now()), log_file, verbose)
    log_message("\n------------------------------------------------------------", log_file, verbose)
    exit(0) 


# Copy a given file to a new directory--will create that
# directory if it doesn't already exist.
# Paramters: the absolute dir of the file to be copied,
# the new directory for the copied file, 
# the name for the new file.
# Eg: abs_dir = /home/to_copy/copy_me
# new_dir = /home/destination/
# new_name = my_new_file
def copy_file(abs_dir, new_dir, new_name):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)    
    shutil.copy(abs_dir, new_dir + "/" + new_name) 



################
# "Main":
################

# build the command-line parser, parse
parser = argparse.ArgumentParser(description='Process airVision security footage for activity.')
parser.add_argument('video_path', help='Path to airVision Videos directory.')
parser.add_argument('saved_activity', help='Path to directory to save active videos under.')
parser.add_argument('log_file', help='File to put logging messages in.')
parser.add_argument('--verbose', action='store_true', help='If verbose is given, logging messages will be printed to stdout.')
args = parser.parse_args()  

log_message("\n\n\n------------------------------------------------------------", args.log_file, args.verbose)
log_message("\nBeginning: " + str(datetime.datetime.now()), args.log_file, args.verbose)
log_message("\nProcessing airVision data at: " + args.video_path, args.log_file, args.verbose)
log_message("\nSaving positive footage at: " + args.saved_activity, args.log_file, args.verbose)
   

# grab the dates of the videos (2013/10/22/13), camera_ids, and absolut paths
dates, camera_ids, abs_paths = video_retriever.grab_video_dirs(args.video_path)

if len(dates) != len(camera_ids):
    log_message("\nThe number of returned dates from the airVision directory, does not equal the number of camera_ids.  Exiting...", args.log_file, args.verbose)
    terminate_main(args.log_file, args.verbose)
else:
    date_cams_abspaths = zip(dates, camera_ids, abs_paths)

# create the tiger_log table
tiger_log.create_table()

log_message("\n\nUpdating the rows in the tiger_log.db table...", args.log_file, args.verbose)

# update the rows in the table--adding any newly discovered video directories
tiger_log.insert_many_rows(date_cams_abspaths)

log_message("\nSelecting unprocessed rows from tiger_log.db table...", args.log_file, args.verbose)

# grab the abs_paths of the directories that need processing
need_processing = tiger_log.select_unprocessed()

# exit if there's nothing to process
if len(need_processing) == 0:
    log_message("\nNothing to process...", args.log_file, args.verbose)   
    terminate_main(args.log_file, args.verbose)

# loop through all directories that need processing
log_message("\n", args.log_file, args.verbose)
for item in need_processing:
    currently_processing = item[0]
    log_message("\nProcessing this directory: " + currently_processing, args.log_file, args.verbose)
    tiger_count = 0    
    counts_and_dirs = getPositives.retClips(currently_processing,500, 10) # dir, min_size, hits

    # look at all clips that passed our # of positive hits threshold    
    for elements in counts_and_dirs:
        tiger_count = tiger_count + elements[0]
        abs_path = elements[1]
        date_path, file_name = video_retriever.date_and_file_name(abs_path, args.video_path)
        new_dir = args.saved_activity + "/" + date_path
        copy_file(abs_path, new_dir, file_name)
        tiger_log.update_savedat_by_dir(currently_processing, new_dir) # now we know where pos footage was saved at
    
    # update the table for this directory
    tiger_log.update_processed_by_dir(currently_processing, 'Y')
    tiger_log.update_pos_frames_by_dir(currently_processing, tiger_count)
    log_message('\n✓', args.log_file, args.verbose)
        
terminate_main(args.log_file, args.verbose)




    
    
