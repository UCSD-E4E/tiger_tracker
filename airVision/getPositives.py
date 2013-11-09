from detection_module_tiger import TigerDetector
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
    return [ tryint(c) for c in re.split('([0-9]+)',s) ]

def sort_nicely(l):
    l.sort(key=alphanum_key)
##############################################




# Description: Checks video files in passed directory for tiger hits 
# Params: vid_dir    -- path of directory
#         min_size   -- min size for candidate foreground contours
#         num_hits   -- tiger detection threshold
# Return: tiger_clip -- zipped list of the number of pos frames, and abs paths
def retClips(vid_path, min_size, num_hits):    
    detector = TigerDetector(min_size)
    tiger_clip = []  
    pos_frms = []
    pos_frames = 0  
    clips = os.listdir(vid_path)
    sort_nicely(clips)
    for clip in clips:
        clip = vid_path + "/" + clip    
        pos_frames = count_pos_frames(clip, min_size,num_hits, detector)
        if pos_frames != -1:
            if pos_frames >= num_hits:
                tiger_clip.append(clip)
                pos_frms.append(pos_frames)
    zipped = zip(pos_frms, tiger_clip)
    return zipped


# Description: Checks video clip for tiger
# Params: clip     -- path name of video clip
#         min_size -- min size for candidate foreground colors
# Return: Returns # of positive tiger frames.  Or -1 
# if the video could not be opened
def count_pos_frames(clip, min_size, num_hits, detector):
    hits = 0
    cap = cv2.VideoCapture(clip)
    if cap.isOpened():
        frame_capt, frame = cap.read()
        while frame_capt:
            is_detected, coordinates = detector.process_frame(frame)
            if is_detected == 1:
                hits += 1
            cv2.waitKey(1)
            # Read the next frame
            frame_capt, frame = cap.read()
    else:
        print 'Could not open video file:', clip
        return -1
    return hits





