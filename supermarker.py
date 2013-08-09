#!/usr/bin/python

import cv, cv2
import numpy as np
import os
import glob
import sys,  pygame
import time
import csv
import fileinput
from pygame.locals import *


########################################################
#create list of positive files
########################################################
poslist_f = [] 
poslist_b = [] 
poslist_l = []
poslist_r = []  
files = {}
f_num = 0 # for save state
g_count = 0 #for finding scores
points = 0

#instruction screen
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
            if instruction_page == 6:
                display_instructions = False
        elif event.type == KEYDOWN and event.key == K_j:
            user = "j"
            username = "Jeremy"
            print("Hello Jeremy")
        elif event.type == KEYDOWN and event.key == K_r:
            user = "r"
            username = "Riley"
            print("Hello Riley")
        elif event.type == KEYDOWN and event.key == K_g:
            user = "g"
            username = "Gabrielle"
            print("Hello Gabrielle")
        elif event.type == KEYDOWN and event.key == K_d:
            user = "d"
            username = "David"
            print("Hello David")
    screen.fill(backGround)    
    if instruction_page == 1:
        text = font.render("Please select the first letter of your first name", True, black)
        screen.blit(text, [10,10])
        text = font.render("Hit 'j' for 'Jeremy'", True, black)
        screen.blit(text, [10,40])
        text = font.render("Hit 'r' for 'Riley'", True, black)
        screen.blit(text, [10,70])
        text = font.render("Hit 'g' for 'Gabrielle'", True, black)
        screen.blit(text, [10,100])
        text = font.render("Hit 'd' for 'David'", True, black)
        screen.blit(text, [10,130])
        text = font.render("Hit the space bar to continue", True, black)
        screen.blit(text, [10,170])  
    if instruction_page == 2:
        text = font.render("Instructions:", True, black)
        screen.blit(text, [10,10])
        text = font.render("Welcome to the Supermarker Safari!", True, black)
        screen.blit(text, [10,40])
        text = font.render("Hit one of the arrow keys to save the image", True, black)
        screen.blit(text, [10,70])
        text = font.render("Only mark an image if there is exactly 1 animal", True, black)
        screen.blit(text, [10,100])
        text = font.render("Hit the space bar to continue", True, black)
        screen.blit(text, [10,170])
    if instruction_page == 3:
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
    if instruction_page == 4:
        text = font.render("Hit the space bar to move to the next picture", True, black)
        screen.blit(text, [10,10])
        text = font.render("To ignore an image do not hit any arrows", True, black)
        screen.blit(text, [10,40])
        text = font.render("If you are finished marking pictures press 'd'", True, black)
        screen.blit(text, [10,70])
        text = font.render("Hit the space bar to continue", True, black)
        screen.blit(text, [10,170])
    if instruction_page == 5:
        text = font.render("Prove yourself a worthy animal marker!", True, black)
        screen.blit(text, [10,10])
        text = font.render("Save them from their plain white background!", True, black)
        screen.blit(text, [10,40])
        text = font.render("There can only be one champion!", True, black)
        screen.blit(text, [10,70])
        text = font.render("Hit the space bar to continue", True, black)
        screen.blit(text, [10,170])
    if instruction_page == 6:
        text = font.render("Begin!", True, black)
        screen.blit(text, [10,10])
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
with open("high_scores.csv", "a") as scorekeeper:
    pass
scorekeeper.close()
reader = open("filelist.txt", "r")
for place in reader: #find save state
    f_num += 1
reader.close()
scorefinder = [row for row in csv.reader(open("high_scores.csv", "rb"))] #find previous score
for score in scorefinder:
    if username == scorefinder[g_count][0]:
        points = int(score[1])
    g_count += 1    
pygamer = True
g_count = 0 #for finding scores
bonus = 1
b_count = 0
reader = [row for row in csv.reader(open("meta.csv", "rb"))]
while pygamer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE: #hit "SPACE" to move to next picture
            print("load next picture")
            if g_count == 100: #bonus round after 100 rounds
                    g_count = 0
                    points += 1000
                    print("Chicago Party!!!!!!!!!!!!!!!!!!!!!" + "\n" + "No Mushrooms!!!!!!!!!!!!!!!!!!!!!") 
            elif (len(reader) > f_num):
                pic = reader[f_num][0] #get file name
                files[pic] = [reader[f_num][1],reader[f_num][2],reader[f_num][3],reader[f_num][4],] #build hash table
                if b_count != bonus: #if marking is not sequential reset bonus
                    bonus = 0
                    b_count = 0
                    print("restart bonus count")
                b_count += 1
                print ("bonus count: " + str(b_count))
                print ("bonus: " + str(bonus))
                g_count += 1 #keep track of number of rounds
                print ("Round number: " + str(g_count))
                print ("points: " + str(points))
                with open("filelist.txt", "a") as writer:                
                    writer.write(pic + '\n')
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
            points += 60
            bonus += 1
            if b_count == bonus and bonus > 2:
                points += 60*bonus
                print ("Bonus!!!!!!!")
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_UP: #hit "up arrow" to save back view
            poslist_b.append(pic)
            points += 100
            bonus += 1
            if b_count == bonus and bonus > 2:
                points += 100*bonus
                print ("Bonus!!!!!!!")
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_LEFT: #hit "left arrow" to save pointing left view
            poslist_l.append(pic)
            points += 70
            bonus += 1
            if b_count == bonus and bonus > 2:
                points += 70*bonus
                print ("Bonus!!!!!!!")
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_RIGHT: #hit "right arrow" to save pointing right view
            poslist_r.append(pic)
            points += 10
            bonus += 1
            if b_count == bonus and bonus > 2:
                points += 10*bonus
                print ("Bonus!!!!!!!")
            print("Picture added")
        elif event.type == KEYDOWN and event.key == K_d: #hit "d" to finish marking
                pygamer = False 
writer.close()
with open("high_scores.csv", "a") as scorekeeper:
    scorekeeper.write(username + "," + str(points) + "\n")
scorekeeper.close()

scorefinder = [row for row in csv.reader(open("high_scores.csv", "rb"))] #find previous score
#high score screen
os.system("clear") 
print("Your Score" + "\n")
print(username + " " + str(points) + "\n")
for score in scorefinder:
    print(str(score) + "\n")
 
              
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
        writer.write("1 0 0" + dimen[7:-1] + "\n")
writer.close()
 
for doc in poslist_b: #back view descriptor file
    dimensions = (files[doc])
    with open("positive_b.txt", "a") as writer:    
        writer.write(doc + ' ')
        dimen = str(dimensions)
        dimen = dimen.replace(",", "")
        dimen = dimen.replace("'", "")
        writer.write("1 0 0" + dimen[7:-1] + "\n")
writer.close()

for doc in poslist_l: #pointing left view descriptor file
    dimensions = (files[doc])
    with open("positive_l.txt", "a") as writer:        
        writer.write(doc + ' ')
        dimen = str(dimensions)
        dimen = dimen.replace(",", "")
        dimen = dimen.replace("'", "")
        writer.write("1 0 0" + dimen[7:-1] + "\n")
writer.close()

for doc in poslist_r: #pointing right view descriptor file
    dimensions = (files[doc])
    with open("positive_r.txt", "a") as writer:      
        writer.write(doc + ' ')
        dimen = str(dimensions)
        dimen = dimen.replace(",", "")
        dimen = dimen.replace("'", "")
        writer.write("1 0 0" + dimen[7:-1] + "\n")
writer.close()

    

