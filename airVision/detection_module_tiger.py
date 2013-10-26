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
    # Return: 0 if no tiger is predicted. Otherwise, return
    # 1 and a list containing [x,y,w,h] of bounding
    # rect for selected "tiger" contour 
    def process_frame(self, frame):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_thresh = bg_mog.apply(img, None, 0.01) 
        contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

        for i in range(0, len(contours)):
            if(i % 1 == 0):
                cont = contours[i]
                x, y, w, h = cv2.boundingRect(cont) #calculates dimensions
                img_seg = img[y:y+h, x:x+w]
                
                if w*h > MIN_SIZE:
                    color_seg = cv2.inRange(img_seg, (120, 140, 220), (200,250, 256))
                        
                    if np.count_nonzero(color_seg) > 0.1*w*h:
                        # it's probably a tiger!
                        coordinates = []
                        coordinates.insert(0, x)
                        coordinates.insert(1, y)
                        coordinates.insert(2, w)
                        coordinates.insert(3, h)
                        return 1, coordinates
                
                    else:
                        return 0
                            

