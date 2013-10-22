#!/usr/bin/python

import cv, cv2
import numpy as np
import os
import glob
import sys,  pygame
from pygame.locals import *

DIRECTORY = "./"

cap = cv2.VideoCapture("tiger3.avi")
cv2.namedWindow("Threshold")
cv2.namedWindow("Candidates")
#try:
#os.system("mkdir " + DIRECTORY)
#except
 #   continue

img_ct = 0;
frame_ct = 0; 
files = {} 
writer = open('filelist.txt', 'w') 
for pictures in glob.glob('./img_cand*.bmp'):
	img_ct += 1
print img_ct
loop = True
while loop == True:
    f, img = cap.read() #read frames from video
    frame_ct += 1
    if (frame_ct % 3) == 0: 
	if (f == False):        
		loop = False
	else:
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #converts to gray scale
    
        rect = [[75,90], [130, 77], [130, 120], [75, 127]] #making black polygon over rock
        poly = np.array([rect], dtype=np.int32)
        rect2 = [[101, 277], [103, 277], [103, 278], [101, 278]]
        poly2 = np.array([rect2], dtype=np.int32)
     
        cv2.fillPoly(img_gray, poly, 0) 
        cv2.fillPoly(img_gray, poly2, 0)
        retval, img_thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY) 
     
        contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 


        for i in range(0, len(contours)):
            if(i % 2 == 0):
                cont = contours[i]
                x, y, w, h = cv2.boundingRect(cont) #calculates dimensions
                img_tiger = img_gray[y:y+h, x:x+w] 
                if w*h > 4000:
                    cv2.imshow("Candidates", img_tiger)
                    cv2.imwrite(DIRECTORY + "img_cand" + str(img_ct).zfill(6) + ".bmp", img_tiger)# write images to file
		    writer.write(DIRECTORY + "img_cand" + str(img_ct).zfill(6) + ".bmp")
		    writer.write('\n')

		    files["img_cand" + str(img_ct).zfill(6) + ".bmp"] = [x, y, w, h] #add file to dictionary
               	    img_ct += 1

    
        #cv2.imshow("Threshold", img_thresh)
        cv2.waitKey(1)
writer.close()
########################################################
#create list of positive files
########################################################
poslist = [] 
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
	dimensions = (files[doc])
	writer.write(doc + ' ')	
	dimen = str(dimensions)
	dimen = dimen.replace(",", "")
	writer.write(dimen[1:-1]) 
	writer.write('\n')

    

