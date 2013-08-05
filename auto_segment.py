#!/usr/bin/python
import cv, cv2
import numpy as np
import os
import glob
import sys,  pygame
import time
from pygame.locals import *

CAND_DIRECTORY = "./"
MIN_SIZE = 2000
FRAME_PERIOD = 3
BG_LEARN_RATE = 0.0001
BRIGHTNESS = 100

cv2.namedWindow("Threshold")
cv2.namedWindow("Candidates")

img_ct = 0;
frame_ct = 0; 
files = {} 

bg_mog = cv2.BackgroundSubtractorMOG()

def segmentBG(img_in, learn_rate):
    img_out = bg_mog.apply(img_gray, None, 0.0001)
    return img_out

def segmentTHR(img_in, brightness):
    img_out = cv2.threshold(img_in, brightness, 255, cv2.THRESH_BINARY)
    return img_out

writer = open(CAND_DIRECTORY + "meta.csv", 'w')

#get images in directory
for images in glob.glob('./*.avi'):
    cap = cv2.VideoCapture(str(images))
    #get initial frame:
    f, img = cap.read() #read frames from video

    while (f == True):
        frame_ct = (frame_ct + 1) % FRAME_PERIOD
        if (frame_ct == 0): 
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            print "Thresholding..." 
            img_thresh = bg_mog.apply(img_gray, None, 0.0001)
            cv2.imshow("Threshold", img_thresh)

            contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

            for i in range(0, len(contours)):
                if(i % 2 == 0):
                    cont = contours[i]
                    x, y, w, h = cv2.boundingRect(cont) #calculates dimensions
                    img_seg = img_gray[y:y+h, x:x+w]
                    if w*h > MIN_SIZE:
                        cv2.imshow("Candidates", img_seg)
                        # save segmented image
                        name = "img_cand" + str(img_ct).zfill(6) + ".bmp"
                        cv2.imwrite(CAND_DIRECTORY + name, img_seg)
                        # write file name and info to dictionary
                        writer.write(str(name) + "," + str(x) + "," + str(y) + "," + str(w) + "," + str(h) + "\n")
                        img_ct += 1 
                              
        cv2.waitKey(1)
        f, img = cap.read() #read frames from video
    
