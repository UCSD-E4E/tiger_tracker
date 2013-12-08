from detection_module_tiger import TigerDetector
from airVision_Viewer import AirVision_Viewer
import cv, cv2
import numpy
import os
import re


##############################################
# Sort alphanumerically
def tryint(s):
    try:
        return int(s)
    except:
        return s
    
def alphanum_key(s):
    # if given a tuple, sort on the first element    
    if type(s).__name__ == 'tuple':
        s = s[0]
    return [ tryint(c) for c in re.split('([0-9]+)',s) ]

def sort_nicely(l):
    l.sort(key=alphanum_key)
##############################################



# Description: Checks video files in passed directory for tiger hits 
# Params: vid_dir    -- path of directory
#         min_size   -- min size for candidate foreground contours
#         num_hits   -- tiger detection threshold
# Return: tiger_clip -- zipped list of the number of pos frames, and abs paths
# to corresponding videos
def retClips(vid_path, min_size, num_hits):    
    # name of the directory to temporarily hold re-encoded videos
    tmp_video_folder = "tmp_videos" 
        
    # to view the Airvision video files frame by frame 
    our_viewer = AirVision_Viewer(tmp_video_folder)   
    
    detector = TigerDetector(min_size)
    tiger_clip = []  
    pos_frms = []
    pos_frames = 0  
    clips = os.listdir(vid_path)
    sort_nicely(clips)  # put the clips in temporal order

    # count pos frames in all clips    
    for clip in clips:
        clip = vid_path + "/" + clip    
        pos_frames = count_pos_frames(clip, min_size,num_hits, detector, our_viewer)
        if pos_frames != -1:
            if pos_frames >= num_hits:
                tiger_clip.append(clip)
                pos_frms.append(pos_frames)
    
    zipped = zip(pos_frms, tiger_clip)
    our_viewer.close_viewer()  # Make sure we release our video viewer (deletes the tmp video directory)
    return zipped


# Description: Checks video clip for tiger
# Params: clip-- path to video clip
# min_size -- min size for candidate foreground contours
# detector--the TigerDetecor object
# viewer--airVision video Viewer object
# Return: Returns # of positive tiger frames.  Or -1 
# if the video could not be opened
def count_pos_frames(clip, min_size, num_hits, detector, viewer):
    hits = 0
    is_opened = viewer.open_viewer(clip)
    if is_opened:
        while viewer.next_frame_available():
            frame = viewer.next_frame()
            if frame != None:
                is_detected, coordinates = detector.process_frame(frame)
            if is_detected == True:
                hits = hits + 1
    else:
        print 'Could not open video file:', clip
        return -1
    return hits





