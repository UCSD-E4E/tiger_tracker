#!/usr/bin/python

import tiger_log as log
import subprocess
import sqlite3
import argparse
import datetime
import sys


# Description: Parses passed in date in format YYYY/MM/DD/H
# Return: Boolean value indicating whether input was valid
def process_date(date):
   try:
        date = datetime.datetime.strptime(date,"%Y/%m/%d/%H")
        return True
   except ValueError:
        return False


# Description: Prompts for valid date input and parses date
# Return: Parsed date 
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



################################# MAIN ########################################

# Description: Prompts user for date input, then plays appropriate concatenated 
#              footage through video player.
# Requires date input in format (YYYY/MM/DD/H)


# Prompt the user for date input:
date = prompt_date()
# Retrieve the appropriate files from tiger_log.db
try:
    print '\nOpening database to retrieve paths'
    tiger_db, cursor = log.open_data_base()     # in tiger_log.py
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
    with open("vid_paths.txt", 'a') as output:
        output.write('file '+ path + '\n')    


# Stitch toegether positve frames using ffmpeg
print '\nRunning compile_vid.sh'
subprocess.call("sh compile_vid.sh", shell=True)
print 'Sucessful.'


vlc_path = '/usr/bin/vlc'
vid_path =                # path of output.ts created in compile_vid.sh

# Play stitched video in video player (vlc)
subprocess.call([vlc_path, vid_path, '--play-and-exit', '--fullscreen'], shell=True)

# End
