#!/usr/bin/python

import cv, cv2
import numpy as np
import os
import glob
import sys,  pygame
import time
from pygame.locals import *

DIRECTORY = "./"
MIN_SIZE = 2000
FRAME_PERIOD = 3

cap = cv2.VideoCapture("wolf2.avi")
cv2.namedWindow("Threshold")
cv2.namedWindow("Candidates")

img_ct = 250;
frame_ct = 0; 
files = {} 

bg_mog = cv2.BackgroundSubtractorMOG()

#get initial frame:
f, img = cap.read() #read frames from video

while (f == True):
    frame_ct += 1
    if (frame_ct % FRAME_PERIOD) == 0: 
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print "Thresholding..." 
        img_thresh = bg_mog.apply(img_gray, None, 0.0001)
        cv2.imshow("Threshold", img_thresh)

        contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

        for i in range(0, len(contours)):
            if(i % 2 == 0):
                cont = contours[i]
                x, y, w, h = cv2.boundingRect(cont) #calculates dimensions
                img_tiger = img_gray[y:y+h, x:x+w]
                if w*h > MIN_SIZE:
                    cv2.imshow("Candidates", img_tiger)
                    # save segmented image
                    name = DIRECTORY + "img_cand" + str(img_ct).zfill(6) + ".bmp"
                    cv2.imwrite(name, img_tiger)
                    # write file name and info to dictionary
                    files[name] = [x, y, w, h] 
                    img_ct += 1
        
    cv2.waitKey(1)
    f, img = cap.read() #read frames from video
        
        #cv2.imshow("Threshold", img_thresh)

########################################################
#create list of positive files
########################################################
poslist = [] 
writer = open('filelist.txt', 'w') 
for pictures in glob.glob('./img_cand*.bmp'):
	writer.write(str(pictures))
	writer.write('\n')
writer.close()

reader = open('filelist.txt')
pygame.init()
size = width, height = 600, 400 
screen = pygame.display.set_mode(size)
pygamer = True
while pygamer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE: #hit "SPACE" to move to next picture
            print("load next picture")
            pic = reader.readline()
            pic = pic[2:-1]
            if (len(pic) > 5):
                l_pic = pygame.image.load(pic) #load picture
            else:
                pygamer = False
            screen.blit(l_pic, (0,0)) #display picture
            pygame.display.flip()
            print(pic)
        elif event.type == KEYDOWN and event.key == K_s: #hit "s" write to positive file list
            poslist.append(pic)
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_f: #hit "f" to finish marking
            pygamer = False  
########################################################
#create descriptor file
########################################################
writer = open('positive.txt', 'w') 
for doc in poslist:
    writer.write(doc + ' ')	
    dimensions = (files[doc])
    dimen = str(dimensions)
    dimen = dimen.replace(",", "")
    writer.write(dimen[1:-1]) 
    writer.write('\n')

    

