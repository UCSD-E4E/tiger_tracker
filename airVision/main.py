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

def terminate_main():
    print "\nExiting at:",str(datetime.datetime.now())
    print "\n------------------------------------------------------------"
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
args = parser.parse_args()  

print "\n------------------------------------------------------------"
print "\nProcessing airVision data at:", args.video_path
print "Saving positive footage at:", args.saved_activity
print "Beginning processing at:",str(datetime.datetime.now())
   

# grab the dates of the videos (2013/10/22/13), camera_ids, and absolut paths
dates, camera_ids, abs_paths = video_retriever.grab_video_dirs(args.video_path)

if len(dates) != len(camera_ids):
    print "The number of returned dates from the airVision directory, does not equal the number of camera_ids.  Exiting..."
    terminate_main()
else:
    date_cams_abspaths = zip(dates, camera_ids, abs_paths)

# create the tiger_log table
tiger_log.create_table()

print "\nUpdating the rows in the tiger_log.db table..."

# update the rows in the table--adding any newly discovered video directories
tiger_log.insert_many_rows(date_cams_abspaths)

print "Selecting unprocessed rows from tiger_log.db table...\n"

# grab the abs_paths of the directories that need processing
need_processing = tiger_log.select_unprocessed()

# exit if there's nothing to process
if len(need_processing) == 0:
    print "Nothing to process..."    
    terminate_main()

# loop through all directories that need processing
for item in need_processing:
    currently_processing = item[0]
    print "Processing this directory:",currently_processing
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
    print '✓\n'
        
terminate_main()




    
    
