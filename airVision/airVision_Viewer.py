#!/usr/bin/python
import cv, cv2
import os
import shutil
import glob


# To view AirVision files frame by frame, without OpenCV halting.
class AirVision_Viewer:

    # An AirVision_Viewer will create a temporary
    # directory for re-encoded AirVision Videos 
    # that don't break OpenCV's VideoCapture 
    # functionality.
    def __init__(self, tmp_folder):
        self.tmp_video_folder = tmp_folder
        self.cap = cv2.VideoCapture()        
        self.current_frame = 0
        self.total_frames = 0


    # Open a new AirVision_Viewer.
    # Parameters: path to a video.
    # Return: True if the OpenCV video capture module
    # for this video was sucessfully opened.  False
    # otherwise.
    def open_viewer(self, video):
        # encode as a mp4 to smooth processing    
        new_encoding = self.change_encoding(video, self.tmp_video_folder, "mp4") 
        self.cap.open(new_encoding) 
        self.total_frames = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)  
        self.current_frame = 0     
        return self.cap.isOpened()


    # Checks if there more frames left in the video.
    # This function's return must be checked before 
    # every call to next_frame().
    # Return: True if we haven't read all of the frames.
    # False otherwise.
    def next_frame_available(self):
        # loop until we're out of frames, so OpenCV doesn't hang on last frame                        
        if self.current_frame < self.total_frames:
            return True
        else:
	    # nothing left to see in this current capture object
            self.cap.release() 
	    return False

    # next_frame_available()'s return must be checked before
    # calling this function.  
    # Return: the next frame in our AirVision Video.
    def next_frame(self):
        frame_capt, frame = self.cap.read()
        self.current_frame = self.current_frame + 1 
        cv2.waitKey(1)
        return frame

    # Close our viewer--delete the tmp video directory 
    # we've been using.  
    def close_viewer(self):
        self.cap.release()
        self.delete_directory(self.tmp_video_folder)

    # Given absolute path to a video file, encode it as a .mp4
    # and put it into a new directory.  
    # Parameters: clip--absolute path to the video, dir_name--name
    # of the dir to put the new encoding in, file_extension--the 
    # file extension (like "mp4" or "avi")
    # Return: the path to this newly encoded file
    def change_encoding(self, clip, dir_name, file_extension):
        # make a temporary directory for videos if we don't already have one    
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)   

        # create new file path and name
        new_file = (dir_name + "/" + self.return_only_name(clip) + "." +
		file_extension)
    
        # call ffmpeg to change to encoding
        os.system("ffmpeg -i " + clip + " -y -acodec copy -vcodec copy " +
		new_file)  
        return new_file


    # Delete the directory with the passed in name. 
    def delete_directory(self, name):
        try:    
            shutil.rmtree(name)
        except Exception, e:
            print e

    # Given a file, or a the full path to the file,
    # return only the file name with no file extension.
    def return_only_name(self, full_path):
        path_and_name = os.path.split(full_path)
        name_and_extension = os.path.splitext(path_and_name[1])
        return name_and_extension[0]


    # Given a full path to a file, return everything but
    # the file name.
    def return_only_dir(self, full_path):
        path_and_name = os.path.split(full_path)
        return path_and_name[0]

