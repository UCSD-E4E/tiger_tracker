from detection_module_tiger import TigerDetector
import cv, cv2
import fileinput
import os


# Description: Checks video files in passed directory for tiger hits 
# Params: vid_dir   --  path of directory
#         min_size  --  
#         num_hits  -- tiger detection threshold
# Return: list of paths of video clips with tigers detected
def checkClips(vid_dir, min_size, num_hits ):
  tiger_clip = []
  for clip in os.listdir(vid_dir):
      if (checkPos(clip, min_size,num_ hits) != -1):
          tiger_clip.append(clip)
  return tiger_clip
         


# Description: Checks video clip for tiger
# Params: clip     -- path name of video clip
#         min_size -- 
#         num_hits -- tiger detection threshold
# Return: Returns pathname of clip with positive tiger detection
def checkPos(clip, min_size, num_hits):
    hits = 0

    # Open input clip for processing     
    cap = cv2.VideoCapture.open(clip)

    if not cv2.VideoCapture.isOpened():
        print 'Could not open video file:', clip
        return -1 

    detector = TigerDetector(min_size)
  
    while True:
        frame = cap.read()
  
        # Check if end of clip 
        if frame.empty():
            break
    
        # Pass video file to tiger detector
        is_detected, coordinates = process_frame(frame)


        # If is_detected = true && > 10 hits return file name     
        if is_detected:
            hits += 1

        # Read next frame
        cap.read()


    # If more than 10-frame tiger sighting, print file path
    if hits >= num_hits: 
        return clip



## EXIT
