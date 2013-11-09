#!/usr/local/bin/python 

import argparse     
import datetime
import video_retriever
import tiger_log
import getPositives
import shutil
import os

def terminate_main():
    print "Exiting at",str(datetime.datetime.now())
    exit(0) 


################
# "Main":
################

# build the command-line parser, parse
parser = argparse.ArgumentParser(description='Process airVision security footage for activity.')
parser.add_argument('video_path', help='Path to airVision Videos directory.')
parser.add_argument('saved_activity', help='Path to directory to save active videos under.')

args = parser.parse_args()  

print "\n\nProcessing airVision data at", args.video_path
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

print "Updating the rows in the tiger_log.db table..."

# update the rows in the table--adding any newly discovered video directories
tiger_log.insert_many_rows(date_cams_abspaths)

print "Selecting unprocessed rows from tiger_log.db table..."

# grab the abs_paths of the directories that need processing
need_processing = tiger_log.select_unprocessed()

# exit if there's nothing to process
if len(need_processing) == 0:
    print "Nothing to process..."    
    terminate_main()

# pass the abs paths of our directory to the processor
for item in need_processing:
    print "Processing:",item[0]
    counts_and_dirs = getPositives.retClips(item[0],500, 10) # dir, min_size, hits
    for elements in counts_and_dirs:
        tiger_count = elements[0]
        abs_dir = elements[1]
        rel_name = abs_dir.partition(args.video_path)
        index_of_file_name = rel_name[0].rfind("segment")        
        new_name = rel_name[0][0:index_of_file_name]
        shutil.copy(abs_dir, args.saved_activity + "/" + new_name) 
        tiger_log.update_pos_frames_by_dir(item[0], tiger_count)
    tiger_log.update_processed_by_dir(item[0], 'Y')
        
terminate_main()




    
    
