#!/usr/bin/python
import cv, cv2
import numpy as np
import os
import glob
import sys,  pygame
import time
from pygame.locals import *

MIN_SIZE = 500
FRAME_PERIOD = 3
BG_LEARN_RATE = 0.0001
BRIGHTNESS = 100

cv2.namedWindow("Threshold")
cv2.namedWindow("Tiger Detection")

img_ct = 0;
frame_ct = 0; 


#get images in directory
for images in glob.glob('./*.avi'):
    cap = cv2.VideoCapture(str(images))
    bg_mog = cv2.BackgroundSubtractorMOG()
    #get initial frame:
    f, img = cap.read() #read frames from video
    width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    writer = cv2.VideoWriter("./tiger_out.avi", 
                             cv2.cv.CV_FOURCC('D', 'I', 'V', 'X'), 
                             fps, (width, height), True)
    
    print writer.open("./tiger_out.avi", 
                             cv2.cv.CV_FOURCC('D', 'I', 'V', 'X'), 
                             fps, (width, height), True)
    
    if writer.isOpened():
        print "writer is open"
    else:
        print "writer is not open"
 
    while (f == True):
        frame_ct = (frame_ct + 1) % FRAME_PERIOD
        if (frame_ct == 0): 
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_thresh = bg_mog.apply(img, None, 0.01) 
            
            
            contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, 
                                                    cv2.CHAIN_APPROX_SIMPLE) 

            for i in range(0, len(contours)):
                if(i % 1 == 0):
                    cont = contours[i]
                    x, y, w, h = cv2.boundingRect(cont) #calculates dimensions
                    img_seg = img[y:y+h, x:x+w]
                    if w*h > MIN_SIZE:
                        color_seg = cv2.inRange(img_seg, (120, 140, 220), (200,
                                                250, 256))
                        
                        if np.count_nonzero(color_seg) > 0.1*w*h:
                            # it's probably a tiger!
                            cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 1)
                            cv2.rectangle(img_thresh, (x, y), (x+w, y+h), (0,0,255), 3)
                            
                              
            cv2.imshow("Tiger Detection", img)
            cv2.imshow("Threshold", img_thresh)
            writer.write(img)
            
        cv2.waitKey(1)
        f, img = cap.read() #read frames from video
    sys.exit() 
