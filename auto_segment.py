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

pygame.init() #user identification
size = width, height = 600, 400 
screen = pygame.display.set_mode(size)
white = (255,255,255)
black = (0,0,0)
pygame.display.set_caption("User Identification")
screen.fill(black)
done = False
clock=pygame.time.Clock()
font = pygame.font.Font(None, 36)
display_instructions = True
instruction_page = 1
screen.fill(black)                
pygame.display.flip()
while done == False and display_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == KEYDOWN and event.key == K_SPACE:
            instruction_page += 1
            if instruction_page == 2:
                done = True                
                display_instructions = False
        elif event.type == KEYDOWN and event.key == K_j:
            user = "j"
            print("Hello Jeremy")
        elif event.type == KEYDOWN and event.key == K_r:
            user = "r"
            print("Hello Riley")
        elif event.type == KEYDOWN and event.key == K_g:
            user = "g"
            print("Hello Gabrielle")
        elif event.type == KEYDOWN and event.key == K_d:
            user = "d"
            print("Hello David")
    if instruction_page == 1:
        text = font.render("Please select the first letter of your first name", True, white)
        screen.blit(text, [10,10])
        text = font.render("Hit 'j' for 'Jeremy'", True, white)
        screen.blit(text, [10,40])
        text = font.render("Hit 'r' for 'Riley'", True, white)
        screen.blit(text, [10,70])
        text = font.render("Hit 'g' for 'Gabrielle'", True, white)
        screen.blit(text, [10,100])
        text = font.render("Hit 'd' for 'David'", True, white)
        screen.blit(text, [10,130])
        text = font.render("Hit the space bar to continue", True, white)
        screen.blit(text, [10,170]) 
    clock.tick(20)
    pygame.display.flip() 
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
            retvalue, img_thresh = cv2.threshold(img_gray, BRIGHTNESS, 255, cv2.THRESH_BINARY)
            blurred = cv2.blur(img_thresh, (1,1))
            #print img_thresh.__class__.__name__
            retvalue, img_thresh2 = cv2.threshold(blurred, BRIGHTNESS, 255, cv2.THRESH_BINARY)
            cv2.imshow("Threshold", img_thresh2)

            contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

            for i in range(0, len(contours)):
                if(i % 2 == 0):
                    cont = contours[i]
                    x, y, w, h = cv2.boundingRect(cont) #calculates dimensions
                    img_seg = img_gray[y:y+h, x:x+w]
                    if w*h > MIN_SIZE:
                        cv2.imshow("Candidates", img_seg)
                        # save segmented image
                        name = user + "img_cand" + str(img_ct).zfill(6) + ".bmp"
                        cv2.imwrite(CAND_DIRECTORY + name, img_seg)
                        # write file name and info to dictionary
                        writer.write(str(name) + "," + str(x) + "," + str(y) + "," + str(w) + "," + str(h) + "\n")
                        img_ct += 1 
                              
        cv2.waitKey(1)
        f, img = cap.read() #read frames from video
    
