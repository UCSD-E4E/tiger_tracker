import argparse
import datetime
import video_retriever


################
# "Main":
################

# build the command-line parser, parse
parser = argparse.ArgumentParser(description='Process airVision security footage for activity.')
parser.add_argument('video_path', help='Path to airVision Videos directory.')
parser.add_argument('processed_until', help='The relative path of the last video directory processed ( 2013/10/24/16 for example).')
args = parser.parse_args()  

print "Processing Tiger activity from airVision data."
print "Begin:",str(datetime.datetime.now())
   

# get paths to all video containing folders
abs_paths, rel_paths = video_retriever.grab_video_dirs(args.video_path)

# determine the videos directories that need processing
process_list = video_retriever.to_process(args.processed_until, abs_paths, rel_paths)

# exit if there's nothing to process
if len(process_list == 0):
    print "Exiting:"str(datetime.datetime.now())
    exit(0)
    
