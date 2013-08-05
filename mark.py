#!/usr/bin/python

import cv, cv2
import numpy as np
import os
import glob
import sys,  pygame
import time
import csv
from pygame.locals import *


########################################################
#create list of positive files
########################################################
poslist_f = [] 
poslist_b = [] 
poslist_l = []
poslist_r = []  
files = {}
f_num = 0
reader = [row for row in csv.reader(open("metadata.csv", "rb"))]
pygame.init()
size = width, height = 600, 400 
screen = pygame.display.set_mode(size)
backGround = (255,255,255)
pygamer = True
while pygamer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE: #hit "SPACE" to move to next picture
            print("load next picture")
            if (len(reader) > f_num):
                pic = reader[f_num][0] #get file name
                files[pic] = [reader[f_num][1],reader[f_num][2],reader[f_num][3],reader[f_num][4],] #build hash table
                f_num += 1                
                l_pic = pygame.image.load(pic) #load picture
            else:
                pygamer = False
            screen.fill(backGround)#clear screen                
            screen.blit(l_pic, (0,0)) #display picture
            pygame.display.flip()
            print(pic)
        elif event.type == KEYDOWN and event.key == K_DOWN: #hit "f" to save front view
            poslist_f.append(pic)
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_UP: #hit "b" to save back view
            poslist_b.append(pic)
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_LEFT: #hit "l" to save pointing left view
            poslist_l.append(pic)
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_RIGHT: #hit "r" to save pointing right view
            poslist_r.append(pic)
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_d: #hit "d" to finish marking
            pygamer = False  
########################################################
#create descriptor file
########################################################
writer = open('positive_f.txt', 'w') #front view descriptor file
for doc in poslist_f:
    dimensions = (files[doc])
    writer.write(doc + ' ')
    dimen = str(dimensions)
    dimen = dimen.replace(",", "")
    dimen = dimen.replace("'", "")
    writer.write(dimen[1:-1])
    writer.write('\n')

writer = open('positive_b.txt', 'w') #back view descriptor file
for doc in poslist_b:
    dimensions = (files[doc])
    writer.write(doc + ' ')
    dimen = str(dimensions)
    dimen = dimen.replace(",", "")
    dimen = dimen.replace("'", "")
    writer.write(dimen[1:-1])
    writer.write('\n')

writer = open('positive_l.txt', 'w') #pointing left view descriptor file
for doc in poslist_l:
    dimensions = (files[doc])
    writer.write(doc + ' ')
    dimen = str(dimensions)
    dimen = dimen.replace(",", "")
    dimen = dimen.replace("'", "")
    writer.write(dimen[1:-1])
    writer.write('\n')

writer = open('positive_r.txt', 'w') #pointing right view descriptor file
for doc in poslist_r:
    dimensions = (files[doc])
    writer.write(doc + ' ')
    dimen = str(dimensions)
    dimen = dimen.replace(",", "")
    dimen = dimen.replace("'", "")
    writer.write(dimen[1:-1])
    writer.write('\n')

    

