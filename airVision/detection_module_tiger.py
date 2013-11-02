#!/usr/bin/python
import cv, cv2
import numpy as np

class TigerDetector:
    
    # A TigerDetector has a MOG background subtractor
    # associated with it, along with a minimum size
    # for candidate foreground contours.
    # Parameters: min_size--the minimum size a foreground
    # contour must be to possibly be a tiger.
    def __init__(self, min_size):
        self.bg_mog = cv2.BackgroundSubtractorMOG()
        self.MIN_SIZE = min_size
   

    # Parameters: A frame from a video sequence.
    # Return: False if no tiger is predicted. Otherwise, return
    # True and a list containing [x,y,w,h] of bounding
    # rect for selected "tiger" contour 
    def process_frame(self, frame):
        coordinates = []
        img_thresh = self.bg_mog.apply(frame, None, 0.01) 
        contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

        for i in range(0, len(contours)):
            if(i % 1 == 0):
                cont = contours[i]
                x, y, w, h = cv2.boundingRect(cont) #calculates dimensions
                img_seg = frame[y:y+h, x:x+w]

                if w*h > self.MIN_SIZE:
                    color_seg = cv2.inRange(img_seg, (120, 140, 220), (200,250,256))
                   
                    if np.count_nonzero(color_seg) > 0.1*w*h:
                        # it's probably a tiger!
                        coordinates.insert(0, x)
                        coordinates.insert(1, y)
                        coordinates.insert(2, w)
                        coordinates.insert(3, h)
                        return True, coordinates
                
                    else:
                        return False, coordinates
                    
        return False, coordinates
                            

