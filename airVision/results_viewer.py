#!/usr/bin/python

import tiger_log as log
import subprocess
import sqlite3
import argparse
import datetime
import cv, cv2


def process_date(date):
   try:
        date = datetime.datetime.strptime(date,"%Y/%m/%d/%H")
        return True
   except ValueError:
        return False


def prompt_date():
    # Prompt for date
    date = raw_input("\nPlease enter a date-time to be searched (yyyy/mm/dd/hh): ")
    while (True):
        processed = process_date(date)
        if (processed):
           print 'Searching date-time: ', date
           return date
        else:
           date = raw_input("\nError processing date-time. Please re-enter date-time to be searched (yyyy/mm/dd/hh): ")       





date = prompt_date()

try:
    print '\nOpening database to retrieve paths'
    tiger_db, cursor = log.open_data_base()    
    print 'Database opened successfully'

    print '\nSelecting files from date-time: ', date    
    dated = log.select_date(date)
    print dated

    print '\nClosing database'
    log.close_data_base(tiger_db)
    print 'Database closed successfully'

except sqlite3.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)


# Write date paths to vid_paths.txt
for path in dated:
    with open(vid_paths.txt, 'w') as output:
        output.write('file '+ path + '\n')    


# Stitch toegether positve frames using ffmpeg
print '\nRunning compile_list.sh'
subprocess.call("./compile_list.sh", shell=True)
print 'Sucessful.'


# Return stitched videos and play in viewer



