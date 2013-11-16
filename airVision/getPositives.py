from detection_module_tiger import TigerDetector
import cv, cv2
import numpy
import os
import re
import shutil

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


# Delete the directory with the passed in name.
def delete_directory(name):
    try:    
        shutil.rmtree(name)
    except Exception, e:
        print e


# Given a file, or a the full path to the file,
# return only the file name with no file extension.
def return_only_name(full_path):
    path_and_name = os.path.split(full_path)
    name_and_extension = os.path.splitext(path_and_name[1])
    return name_and_extension[0]


# Given a full path to a file, return everything but
# the file name.
def return_only_dir(full_path):
    path_and_name = os.path.split(full_path)
    return path_and_name[0]


# Given absolute path to a video file, encode it as a .mp4
# and put it into a new directory.
# Parameters: clip--absolute path to the video, dir_name--name
# of the dir to put the new encoding in, file_extension--the 
# file extension (like "mp4" or "avi")
# Return: the path to this newly encoded file
def change_encoding(clip, dir_name, file_extension):
    # make a temporary directory for videos if we don't already have one    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)   

    # create new file path and name
    new_file = dir_name + "/" + return_only_name(clip) + "." + file_extension

    # call ffmpeg to change to encoding
    os.system("ffmpeg -i " + clip + " -y -acodec copy -vcodec copy " + new_file)  
    return new_file



# Description: Checks video files in passed directory for tiger hits 
# Params: vid_dir    -- path of directory
#         min_size   -- min size for candidate foreground contours
#         num_hits   -- tiger detection threshold
# Return: tiger_clip -- zipped list of the number of pos frames, and abs paths
def retClips(vid_path, min_size, num_hits):    
    # name of the directory to temporarily hold re-encoded videos
    tmp_video_folder = "tmp_videos"    
    detector = TigerDetector(min_size)
    tiger_clip = []  
    pos_frms = []
    pos_frames = 0  
    clips = os.listdir(vid_path)
    sort_nicely(clips)  # put the clips in temporal order

    # count pos frames in all clips    
    for clip in clips:
        clip = vid_path + "/" + clip    
        pos_frames = count_pos_frames(clip, min_size,num_hits, detector, tmp_video_folder)
        if pos_frames != -1:
            if pos_frames >= num_hits:
                tiger_clip.append(clip)
                pos_frms.append(pos_frames)
    
    zipped = zip(pos_frms, tiger_clip)
    delete_directory(tmp_video_folder) # remove our tmp video folder   
    return zipped


# Description: Checks video clip for tiger
# Params: clip     -- path name of video clip
# min_size -- min size for candidate foreground contours
# detector--the TigerDetecor object
# tmp_video_folder--the name of the directory to temporarily
# hold re-encoded videos 
# Return: Returns # of positive tiger frames.  Or -1 
# if the video could not be opened
def count_pos_frames(clip, min_size, num_hits, detector, tmp_video_folder):
    # encode as a mp4 to smooth processing    
    new_encoding = change_encoding(clip, tmp_video_folder, "mp4")    
    hits = 0
    frame_num = 0
    cap = cv2.VideoCapture(new_encoding)
    if cap.isOpened():
        frame_count = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        # loop until we're out of frames, so OpenCV doesn't hang on last frame        
        while frame_num < frame_count:
            frame_capt, frame = cap.read()
            is_detected, coordinates = detector.process_frame(frame)
            if is_detected == True:
                hits = hits + 1
            frame_num = frame_num + 1
            cv2.waitKey(1)
    else:
        print 'Could not open video file:', clip
        return -1
    return hits





