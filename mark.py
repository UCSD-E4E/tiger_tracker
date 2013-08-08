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


pygame.init()
size = width, height = 600, 400 
screen = pygame.display.set_mode(size)
backGround = (255,255,255)
black = (0,0,0)
pygame.display.set_caption("Instructions")
done = False
clock=pygame.time.Clock()
font = pygame.font.Font(None, 36)
display_instructions = True
instruction_page = 1

while done == False and display_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == KEYDOWN and event.key == K_SPACE:
            instruction_page += 1
            if instruction_page == 3:
                display_instructions = False
        
    if instruction_page == 1:
        text = font.render("Instructions:", True, black)
        screen.blit(text, [10,10])
        text = font.render("Hit one of the arrow keys to save the image", True, black)
        screen.blit(text, [10,40])
        text = font.render("Hit the space bar to continue", True, black)
        screen.blit(text, [10,170])
    if instruction_page == 2:
        text = font.render("Hit left arrow if animal is facing left", True, black)
        screen.blit(text, [10,10])
        text = font.render("Hit right arrow if animal is facing right", True, black)
        screen.blit(text, [10,40])
        text = font.render("Hit up arrow if animal is facing away from camera", True, black)
        screen.blit(text, [10,70])
        text = font.render("Hit down arrow if animal is facing towards camera", True, black)
        screen.blit(text, [10,100])
        text = font.render("Hit the space bar to continue", True, black)
        screen.blit(text, [10,170])
    if instruction_page == 3:
        text = font.render("Hit the space bar to move to the next picture", True, black)
        screen.blit(text, [10,10])
        text = font.render("To ignore an image do not hit any arrows", True, black)
        screen.blit(text, [10,40])
        text = font.render("If you are finished marking pictures press 'd'", True, black)
        screen.blit(text, [10,70])
        text = font.render("Hit the space bar to continue", True, black)
        screen.blit(text, [10,170])
    clock.tick(20)
    pygame.display.flip()
pygame.init()
size = width, height = 600, 400 
screen = pygame.display.set_mode(size)
with open("filelist.txt", "a") as writer:
    pass
writer.close()
reader = open("filelist.txt", "r")
for place in reader: #find save state
    f_num += 1
reader.close()
pygamer = True
reader = [row for row in csv.reader(open("meta.csv", "rb"))]
while pygamer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE: #hit "SPACE" to move to next picture
            print("load next picture")
            if (len(reader) > f_num):
                pic = reader[f_num][0] #get file name
                files[pic] = [reader[f_num][1],reader[f_num][2],reader[f_num][3],reader[f_num][4],] #build hash table 
                with open("filelist.txt", "a") as writer:                
                    writer.write(pic)
                    writer.write('\n')
                    f_num += 1                
                    l_pic = pygame.image.load(pic) #load picture
            else:
                pygamer = False
            screen.fill(backGround)#clear screen                
            screen.blit(l_pic, (0,0)) #display picture
            pygame.display.flip()
            print(pic)
        elif event.type == KEYDOWN and event.key == K_DOWN: #hit "down arrow" to save front view
            poslist_f.append(pic) 
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_UP: #hit "up arrow" to save back view
            poslist_b.append(pic)
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_LEFT: #hit "left arrow" to save pointing left view
            poslist_l.append(pic)
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_RIGHT: #hit "right arrow" to save pointing right view
            poslist_r.append(pic)
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_d: #hit "d" to finish marking
            pygamer = False 
writer.close() 
########################################################
#create descriptor file
########################################################
 
for doc in poslist_f: #front view descriptor file
    dimensions = (files[doc])
    with open("positive_f.txt", "a") as writer:    
        writer.write(doc + ' ')
        dimen = str(dimensions)
        dimen = dimen.replace(",", "")
        dimen = dimen.replace("'", "")
        writer.write(dimen[1:-1] + '\n')
writer.close()
 
for doc in poslist_b: #back view descriptor file
    dimensions = (files[doc])
    with open("positive_b.txt", "a") as writer:    
        writer.write(doc + ' ')
        dimen = str(dimensions)
        dimen = dimen.replace(",", "")
        dimen = dimen.replace("'", "")
       	writer.write(dimen[1:-1] + '\n')
writer.close()

for doc in poslist_l: #pointing left view descriptor file
    dimensions = (files[doc])
    with open("positive_l.txt", "a") as writer:        
        writer.write(doc + ' ')
        dimen = str(dimensions)
        dimen = dimen.replace(",", "")
        dimen = dimen.replace("'", "")
	writer.write(dimen[1:-1] + '\n')
writer.close()

for doc in poslist_r: #pointing right view descriptor file
    dimensions = (files[doc])
    with open("positive_r.txt", "a") as writer:      
        writer.write(doc + ' ')
        dimen = str(dimensions)
        dimen = dimen.replace(",", "")
        dimen = dimen.replace("'", "")
        writer.write(dimen[1:-1] + '\n')
writer.close()

    

