import pygame

import os
import sys
import player as p
import maps as m
import blocks
import time as t
import random
import ghost as g
import math




#sprites fertigstellen
#Escape schriften richtig hinstellen
#

#######################Initialisierung Pygame + Window###########################################
pygame.init()
clock=pygame.time.Clock()
runtime=t.perf_counter()
collectablestarttime=runtime
screenWidth=1000
screenHeight=500
gameWindow=pygame.display.set_mode([screenWidth,screenHeight])
pygame.display.set_caption("PacMan")
windowRunning=True
menuRunning=True
pauseMenuRunning=False
gameRunning = False
editorRunning = False
customGameRunning=False
nextLevelScreen=False
endScreen=False
gamemode=""
gameBackground = pygame.image.load("Graphics/Background/background.png")
gamebar=pygame.Rect((0,0, 1000, 60))
pygametimedelay=120
currentmode=""
pausemenudisplay=False
mapselection=1
mapauthor="##"
customgamepage=0
mapnumber=m.getAllMapDataSingleInfo()
showhitboxes=False
selecteditem = 1
selecteditemsprite = m.selectSprite(1)
movedirection=1
npcblockwall = blocks.Wall(m.hub.x, m.hub.y + (m.hub.width * 3))
game = False

#################################################################################################

fonttype="arial"
fontrange=60 #max font size for higher comfort
font=[]
fontcolour=(255,255,255)#fontcolour for the game
font.append("")
for i in range(fontrange+1):
    font.append (pygame.font.SysFont(fonttype, (i)))








# Windowsystem with multiple
while windowRunning:

    pygame.time.delay(pygametimedelay) #Delay for Inputs

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                windowRunning=False
                
    while gameRunning == True   :
        clock.tick(60) #sets frames to 60 FPS
        
        #pygame.time.delay(pygametimedelay) #not used because of clocktick


        #standatised system for text:

        numbertext = 6
        #initilasation text
        text = []
        text_rect = []
        for i in range(numbertext):
            text.append(font[60].render("Init", True, fontcolour))
            text_rect.append(text[i].get_rect(center=((screenWidth / 2), screenHeight / 2)))

        #setting values for all text in one while loop
        text[0] = font[20].render("Pause", True, (fontcolour))
        text_rect[0] = text[0].get_rect(center=((screenWidth / 35), screenHeight / 30))
        text[1] = font[20].render("Menu (Esc)", True, fontcolour)
        text_rect[1] = text[1].get_rect(center=((screenWidth / 20), screenHeight / 12))
        text[2] = font[20].render("Score", True, fontcolour)
        text_rect[2] = text[2].get_rect(center=((2 * screenWidth / 5), screenHeight / 30))
        text[3] = font[20].render(p1.getScore(), True, fontcolour)
        text_rect[3] = text[3].get_rect(center=((2 * screenWidth / 5), screenHeight / 12))
        text[4] = font[20].render("Lifes", True, fontcolour)
        text_rect[4] = text[4].get_rect(center=((3 * screenWidth / 5), screenHeight / 30))
        text[5] = font[20].render("Collectables", True, fontcolour)
        text_rect[5] = text[5].get_rect(center=((113 * screenWidth / 120), screenHeight / 30))

        #check for win an starting nextlevel/endscreen
        if p1.checkForWin()==True:
            if gamemode=="normal":
                p1.level+=1
                blocks.currentlevel+=1
                wingame = True
                pausemenudisplay = False
                nextLevelScreen = True
                gameRunning = False

            if gamemode=="custom":
                wingame = True
                pausemenudisplay = False
                endScreen = True
                gameRunning = False

        # check for win an starting endscreen
        if p1.lifes<=0:

            endScreen=True
            gameRunning=False
            wingame = False

        # countdown for dis-/appering of colletables
        if int(t.perf_counter()-collectablestarttime) ==10:
            if p1.cherrys[p1.level-1]==False:
                if m.collectablespawned==False:
                    m.mapdata[m.collectableposy][m.collectableposx].changeItem(3)
                    m.collectablespawned = True
                elif m.collectablespawned==True:
                    m.mapdata[m.collectableposy][m.collectableposx].changeItem(0)
                    m.collectablespawned = False
            collectablestarttime=t.perf_counter()

        # countdown for enabling controll of player (so the player can't kill himself befor the game even started)
        if int(t.perf_counter()-p1.controllablestarttime) ==1:
            p1.controllable=True

        # countdown for start of npcs and creation of ghostblock, so the npc leaves in the middle
        for i in range(4):
            if int(t.perf_counter()-g.npc[i].starttime) ==g.npc[i].countdowntilstart :
                if g.npc[i].started == False:
                    if i == 0:
                        g.npc[i].movedirection=2
                        npcblockwall=blocks.Wall(m.hub.x,m.hub.y + (m.hub.width * 3))
                        g.npc[i].starttime=t.perf_counter()
                    elif i == 1:
                        g.npc[i].movedirection=2
                        npcblockwall=blocks.Wall(m.hub.x,m.hub.y + (m.hub.width * 3))
                        g.npc[i].starttime = t.perf_counter()
                    elif i == 2:
                        g.npc[i].movedirection=0
                        npcblockwall=blocks.Wall(m.hub.x,m.hub.y + (m.hub.width * 1))
                        g.npc[i].starttime = t.perf_counter()
                    elif i == 3:
                        g.npc[i].movedirection=0
                        npcblockwall=blocks.Wall(m.hub.x,m.hub.y + (m.hub.width * 1))
                        g.npc[i].starttime = t.perf_counter()
                    g.npc[i].countdowntilstart = 7
                else:
                    g.npc[i].starttime = t.perf_counter()






        if p1.boost == False:
            # Collitiondetection if ghost kills player and reset if he does
            collition=False
            for i in range(4):
                if p1.checkCollition(2) == i and g.npc[i].vulnerable==False:
                    collition=True
                if g.npc[i].vulnerable == True:
                    g.npc[i].changeVulnerableState()
            if collition==True:
                p1.getDamage()
                runtime = t.perf_counter()

                movedirection = 1

                p1.vel = 2
                p1.boosttimer = 0
                p1.outofhub = False
                p1.x = m.hub.spawnplayery
                p1.y = m.hub.spawnplayerx
                p1.updateHitbox()
                p1.starttime = runtime
                p1.controllablestarttime = runtime
                p1.controllable=False
                movedirection = 1
                p1.boost = False
                p1.walkcount = 0
                p1.walktimer = 0
                p1.boost = False

                for i in range(4):
                    g.npc[i].starttime = runtime
                    if g.npc[i].npcnumber == 0 or g.npc[i].npcnumber == 1:
                            g.npc[i].movedirection = 4
                    elif g.npc[i].npcnumber == 2 or g.npc[i].npcnumber == 3:
                        g.npc[i].movedirection = 4
                    g.npc[i].direction = 4
                    g.npc[i].countdowntilstart = (i + 1) * 7
                    g.npc[i].outofhub = False
                    g.npc[i].x = m.hub.spawnnpcy[i]
                    g.npc[i].y = m.hub.spawnnpcx[i]
                    g.npc[i].updateHitbox()
                    g.npc[i].started = False
                collition = False

        elif p1.boost==True:
            #Collisiondetection if player hits ghost and if so resets the ghost and increase score
            for i in range(4):
                if p1.checkCollition(2)==i and g.npc[i].vulnerable==True:
                    p1.score+=200

                    g.npc[i].starttime = runtime
                    if g.npc[i].npcnumber == 0 or g.npc[i].npcnumber == 1:
                        g.npc[i].movedirection = 4
                    elif g.npc[i].npcnumber == 2 or g.npc[i].npcnumber == 3:
                        g.npc[i].movedirection = 4
                    g.npc[i].direction = 4
                    g.npc[i].outofhub = False
                    g.npc[i].x = m.hub.spawnnpcy[i]
                    g.npc[i].y = m.hub.spawnnpcx[i]
                    g.npc[i].updateHitbox()
                    g.npc[i].started = False
                    g.npc[i].changeVulnerableState()
                    g.npc[i].starttime=t.perf_counter()


            #changes sprite in the last secounds before boost ends
            for i in range(70,95,15):

                if round(t.perf_counter()-p1.boosttimer,1) ==(i/10):
                    if i%10==5:
                        for i in range(4):
                            if g.npc[i].vulnerable == True:
                                g.npc[i].sprite=pygame.image.load("Graphics\Ghosts\ghost_vulnerable_warning.png")
                    if i%10==0:
                        for i in range(4):
                            if g.npc[i].vulnerable == True:
                                g.npc[i].sprite=pygame.image.load("Graphics\Ghosts\ghost_vulnerable.png")


            #countdown till boost ends

            if int(t.perf_counter()-p1.boosttimer) ==10:
                for i in range(4):
                    if g.npc[i].vulnerable == True:
                        g.npc[i].changeVulnerableState()
                p1.boost = False





        # playercontrolls
        for event in pygame.event.get():
            #for closing window with windows close button
            if event.type == pygame.QUIT:
                windowRunning=False
                gameRunning=False

        #change of the movedirection: real direction will change if theres no block in this direction, just like in the real pacman
        #0=left 1=up 2=right 3=down
        keys= pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and p1.controllable:
            movedirection=0
        
        if keys[pygame.K_RIGHT]and p1.controllable:
            movedirection=2
        
        if keys[pygame.K_UP]:
            movedirection=1
        
        if keys[pygame.K_DOWN]and p1.controllable:
            movedirection=3


        #show hitboxes for hitboxes (works more or less)
        if keys[pygame.K_h]:
            if showhitboxes==False:
                showhitboxes=True
            elif showhitboxes==True:
                showhitboxes=False

        #Open the pause menu and pause the gameLoop
        if keys[pygame.K_ESCAPE]:
            currentmode="game"
            pausemenudisplay=False
            pauseMenuRunning=True
            gameRunning=False		


        #checks if playerinput (movedirection) is executable, or if theres a wall and when its possible moves
        #creates a copy of the playerhitbox and puts it 1px front in the 0=left 1=up 2=right 3=down
        p1.createGhostHitbox(0)
        #and checks this ghosthitbox with all blocks on the map if false -->movement will go to the next stage to get exicutes
        if movedirection == 0 and p1.checkCollition(0) == False:
            p1.direction=0

        p1.createGhostHitbox(2)
        if movedirection == 2 and p1.checkCollition(0) == False:
            p1.direction=2

        p1.createGhostHitbox(1)
        if movedirection == 1 and p1.checkCollition(0) == False:
            p1.direction=1

        p1.createGhostHitbox(3)
        if movedirection == 3 and p1.checkCollition(0) == False:
            p1.direction=3



        #executes the movement, stops if theres a block in the way and if out of screen teleports to the other side
        if p1.direction==0:
            if p1.x < -p1.width+p1.vel:
                p1.x=screenWidth
            p1.createGhostHitbox(0)
            if p1.checkCollition(0)==False:
                p1.x-=p1.vel

        if p1.direction==2:
            if p1.x > screenWidth -p1.vel:
                p1.x=-p1.width

            p1.createGhostHitbox(2)
            if p1.checkCollition(0) == False:
                p1.x+=p1.vel

        if p1.direction==1:
            if  p1.y < (-p1.height+p1.vel)+m.fieldstarty:
                p1.y=screenHeight

            p1.createGhostHitbox(1)
            if p1.checkCollition(0) == False:
                p1.y-=p1.vel

        if p1.direction==3:
            if  p1.y > screenHeight - p1.vel :
                p1.y= (-p1.width)+m.fieldstarty

            p1.createGhostHitbox(3)
            if p1.checkCollition(0) == False:
                p1.y+=p1.vel



        #checks colliton with Item and if theres one collects it
        p1.pickupItem(p1.checkCollition(1))


        #movement of npc passive or active: 0=random 1=aggressive and 2=defensive
        for i in range(4):
        #Select movedirection (same mechanism as player only that input is given by these blocks of code)
            if g.npc[i].passiveoractive==0:
            #Random movedirection selection
                if g.npc[i].movedirection == 0:

                    blockhit=False
                    # if the npc hits a wall infront of him, a random direction is selected
                    g.npc[i].createGhostHitbox(0)
                    #checkColliton is also creating a list of movable direction, that excludes the one of the opposite direction thats input --> npc don't just go back and forth that often
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True:
                        g.npc[i].movedirection =  random.choice(g.npc[i].movabledirections)
                        blockhit = True
                    # if the npc doesnt hit a wall, and a possible way is open (e.g. an opening thats not an edge) a random direction is selected
                    g.npc[i].createGhostHitbox(1)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit==False:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)
                    g.npc[i].createGhostHitbox(3)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)

                elif g.npc[i].movedirection == 1:
                    blockhit = False

                    g.npc[i].createGhostHitbox(1)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)
                        blockhit = True
                    g.npc[i].createGhostHitbox(2)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit==False:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)
                    g.npc[i].createGhostHitbox(0)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)

                elif g.npc[i].movedirection == 2:
                    blockhit = False

                    g.npc[i].createGhostHitbox(2)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)
                        blockhit = True
                    g.npc[i].createGhostHitbox(1)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)
                    g.npc[i].createGhostHitbox(3)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)

                elif g.npc[i].movedirection == 3:
                    blockhit = False

                    g.npc[i].createGhostHitbox(3)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)
                        blockhit = True
                    g.npc[i].createGhostHitbox(0)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)
                    g.npc[i].createGhostHitbox(2)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        g.npc[i].movedirection = random.choice(g.npc[i].movabledirections)






            elif g.npc[i].passiveoractive==1 or g.npc[i].passiveoractive==2:
            ######################################Agressive/Defensive Movedirection selection###########################
                ####################################################################################################
                if g.npc[i].movedirection==0:
                    blockhit = False
                    #same mechanism as above only here the direction is determend by the x and y cordinate of the player
                    g.npc[i].createGhostHitbox(0)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.y>g.npc[i].y:
                        if g.npc[i].passiveoractive==1:
                            g.npc[i].movedirection =  3
                            blockhit = True
                        elif g.npc[i].passiveoractive==2:
                            g.npc[i].movedirection =  1
                            blockhit = True
                    elif g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.y<=g.npc[i].y:
                        if g.npc[i].passiveoractive==1:
                            g.npc[i].movedirection = 1
                            blockhit = True
                        elif g.npc[i].passiveoractive==2:
                            g.npc[i].movedirection = 3
                            blockhit = True

                    g.npc[i].createGhostHitbox(3)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        if p1.y > g.npc[i].y:
                            if g.npc[i].passiveoractive == 1:
                                g.npc[i].movedirection = 3
                            elif g.npc[i].passiveoractive == 2:
                                g.npc[i].movedirection = 1

                    g.npc[i].createGhostHitbox(1)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        if p1.y <= g.npc[i].y:
                            if g.npc[i].passiveoractive==1:
                                g.npc[i].movedirection = 1
                            elif g.npc[i].passiveoractive==2:
                                g.npc[i].movedirection = 3

                ####################################################################################################
                if g.npc[i].movedirection == 2:
                    blockhit = False

                    g.npc[i].createGhostHitbox(2)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.y > g.npc[i].y:
                        if g.npc[i].passiveoractive == 1:
                            g.npc[i].movedirection = 3
                            blockhit = True
                        elif g.npc[i].passiveoractive == 2:
                            g.npc[i].movedirection = 1
                            blockhit = True
                    elif g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.y <= g.npc[i].y:
                        if g.npc[i].passiveoractive == 1:
                            g.npc[i].movedirection = 1
                            blockhit = True
                        elif g.npc[i].passiveoractive == 2:
                            g.npc[i].movedirection = 3
                            blockhit = True

                    g.npc[i].createGhostHitbox(3)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        if p1.y > g.npc[i].y:
                            if g.npc[i].passiveoractive == 1:
                                g.npc[i].movedirection = 3
                            elif g.npc[i].passiveoractive == 2:
                                g.npc[i].movedirection = 1

                    g.npc[i].createGhostHitbox(1)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        if p1.y <= g.npc[i].y:
                            if g.npc[i].passiveoractive == 1:
                                g.npc[i].movedirection = 1
                            elif g.npc[i].passiveoractive == 2:
                                g.npc[i].movedirection = 3

                ####################################################################################################
                if g.npc[i].movedirection == 1:
                    blockhit = False

                    g.npc[i].createGhostHitbox(1)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.x > g.npc[i].x:
                        if g.npc[i].passiveoractive == 1:
                            g.npc[i].movedirection = 2
                            blockhit = True
                        elif g.npc[i].passiveoractive == 2:
                            g.npc[i].movedirection = 0
                            blockhit = True
                    elif g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.x <= g.npc[i].x:
                        if g.npc[i].passiveoractive == 1:
                            g.npc[i].movedirection = 0
                            blockhit = True
                        elif g.npc[i].passiveoractive == 2:
                            g.npc[i].movedirection = 2
                            blockhit = True

                    g.npc[i].createGhostHitbox(2)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        if p1.x > g.npc[i].x:
                            if g.npc[i].passiveoractive == 1:
                                g.npc[i].movedirection = 2
                            elif g.npc[i].passiveoractive == 2:
                                g.npc[i].movedirection = 0

                    g.npc[i].createGhostHitbox(0)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        if p1.x <= g.npc[i].x:
                            if g.npc[i].passiveoractive == 1:
                                g.npc[i].movedirection = 0
                            elif g.npc[i].passiveoractive == 2:
                                g.npc[i].movedirection = 2

                ####################################################################################################
                if g.npc[i].movedirection == 3:
                    blockhit = False

                    g.npc[i].createGhostHitbox(3)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.x > g.npc[i].x:
                        if g.npc[i].passiveoractive == 1:
                            g.npc[i].movedirection = 2
                            blockhit = True
                        elif g.npc[i].passiveoractive == 2:
                            g.npc[i].movedirection = 0
                            blockhit = True
                    elif g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.x <= g.npc[i].x:
                        if g.npc[i].passiveoractive == 1:
                            g.npc[i].movedirection = 0
                            blockhit = True
                        elif g.npc[i].passiveoractive == 2:
                            g.npc[i].movedirection = 2
                            blockhit = True

                    g.npc[i].createGhostHitbox(2)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        if p1.x > g.npc[i].x:
                            if g.npc[i].passiveoractive == 1:
                                g.npc[i].movedirection = 2
                            elif g.npc[i].passiveoractive == 2:
                                g.npc[i].movedirection = 0

                    g.npc[i].createGhostHitbox(0)
                    if g.npc[i].checkCollition(0) == False and g.npc[i].started == True and blockhit == False:
                        if p1.x <= g.npc[i].x:
                            if g.npc[i].passiveoractive == 1:
                                g.npc[i].movedirection = 0
                            elif g.npc[i].passiveoractive == 2:
                                g.npc[i].movedirection = 2


                ################################################################################################

                #first unsuccessfull try
                '''
                elif g.npc[i].movedirection == 1:
                    g.npc[i].createGhostHitbox(1)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.x > g.npc[i].x:
                        if g.npc[i].passiveoractive==1:
                            g.npc[i].movedirection = 2
                        elif g.npc[i].passiveoractive==2:
                            g.npc[i].movedirection = 0
                    elif g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.x <= g.npc[i].x:
                        if g.npc[i].passiveoractive==1:
                            g.npc[i].movedirection = 0
                        elif g.npc[i].passiveoractive==2:
                            g.npc[i].movedirection = 2

                elif g.npc[i].movedirection == 2:
                    g.npc[i].createGhostHitbox(2)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.y > g.npc[i].y:
                        if g.npc[i].passiveoractive==1:
                            g.npc[i].movedirection = 3
                        elif g.npc[i].passiveoractive==2:
                            g.npc[i].movedirection = 1
                    elif g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.y <= g.npc[i].y:
                        if g.npc[i].passiveoractive==1:
                            g.npc[i].movedirection = 1
                        elif g.npc[i].passiveoractive==2:
                            g.npc[i].movedirection = 3

                elif g.npc[i].movedirection == 3:
                    g.npc[i].createGhostHitbox(3)
                    if g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.x > g.npc[i].x:
                        if g.npc[i].passiveoractive==1:
                            g.npc[i].movedirection = 2
                        elif g.npc[i].passiveoractive==2:
                            g.npc[i].movedirection = 0
                    elif g.npc[i].checkCollition(0) == True and g.npc[i].started == True and p1.x <= g.npc[i].x:
                        if g.npc[i].passiveoractive==1:
                            g.npc[i].movedirection = 0
                        elif g.npc[i].passiveoractive==2:
                            g.npc[i].movedirection = 2

                '''



        #Check if movment is possible and if yes sets direction (basicly same as player exept checks if npc is started and checks collision with the ghost block and changes direction accordingly, so the npc is leaving the hub in the middle)
            g.npc[i].createGhostHitbox(0)
            if g.npc[i].movedirection == 0 and g.npc[i].checkCollition(0) == False and g.npc[i].started==True:
                g.npc[i].direction = 0
            if g.npc[i].movedirection == 0 and g.npc[i].started==False:
                g.npc[i].direction = 0
                if g.npc[i].ghosthitbox.colliderect(npcblockwall.hitbox):
                    g.npc[i].direction = 1

            g.npc[i].createGhostHitbox(2)
            if g.npc[i].movedirection == 2 and g.npc[i].checkCollition(0) == False and g.npc[i].started==True:
                g.npc[i].direction = 2
            if g.npc[i].movedirection == 2  and g.npc[i].started==False:
                g.npc[i].direction = 2
                if g.npc[i].ghosthitbox.colliderect(npcblockwall.hitbox):
                    g.npc[i].direction = 1


            g.npc[i].createGhostHitbox(1)
            if g.npc[i].movedirection == 1 and g.npc[i].checkCollition(0) == False and g.npc[i].started==True:
                g.npc[i].direction = 1



            g.npc[i].createGhostHitbox(3)
            if g.npc[i].movedirection == 3 and g.npc[i].checkCollition(0) == False and g.npc[i].started==True:
                g.npc[i].direction = 3






        #takes direction input and moves the ghost (also when out of screesn) (basicly same as player)
            if g.npc[i].direction == 0:

                if g.npc[i].x < -g.npc[i].width + g.npc[i].vel:
                    g.npc[i].x = screenWidth

                g.npc[i].createGhostHitbox(0)
                if g.npc[i].checkCollition(0) == False:
                    g.npc[i].x -= g.npc[i].vel

            if g.npc[i].direction == 2:
                if g.npc[i].x > screenWidth - g.npc[i].vel:
                    g.npc[i].x = -g.npc[i].width

                g.npc[i].createGhostHitbox(2)
                if g.npc[i].checkCollition(0) == False:
                    g.npc[i].x += g.npc[i].vel

            if g.npc[i].direction == 1:
                if g.npc[i].y < (-g.npc[i].height + g.npc[i].vel) + m.fieldstarty:
                    g.npc[i].y = screenHeight

                g.npc[i].createGhostHitbox(1)
                if g.npc[i].checkCollition(0) == False:
                    g.npc[i].y -= g.npc[i].vel

                #delay for ghost (so they don't bug in the hub)
                if g.npc[i].started == False:
                    g.npc[i].ghostdelay += 1
                    if g.npc[i].ghostdelay == 20:
                        g.npc[i].ghostdelay = 0
                        g.npc[i].started = True

            if g.npc[i].direction == 3:
                if g.npc[i].y > screenHeight - g.npc[i].vel:
                    g.npc[i].y = (-g.npc[i].width) + m.fieldstarty

                g.npc[i].createGhostHitbox(3)
                if g.npc[i].checkCollition(0) == False:
                    g.npc[i].y += g.npc[i].vel


        ####################################################################################################################






        ##################################Prints screen content#############################################################

        gameWindow.blit(gameBackground, (0,0))


        #draws map and hitbox if activated
        for i in range(m.mapydirection): 
                for j in range (m.mapxdirection):
                    gameWindow.blit(m.mapdata[i][j].sprite, (m.mapdata[i][j].y,m.mapdata[i][j].x))
                    if m.mapdata[i][j].blocktype =="Empty":
                        gameWindow.blit(m.mapdata[i][j].itemsprite, (m.mapdata[i][j].y, m.mapdata[i][j].x))

                    if showhitboxes == True:
                        if m.mapdata[i][j].blocktype == "Empty":
                            pass
                            #pygame.draw.rect(gameWindow, (255, 0, 0), m.mapdata[i][j].itemhitbox, 2)
                        pygame.draw.rect(gameWindow, (255, 0, 0), m.mapdata[i][j].hitbox, 2)



        #animation of player  based on the 60FPS framerate
        if p1.walkcount+1>=60:
            p1.walkcount=0
        if p1.direction==0:
            gameWindow.blit((p1.sprite[0][p1.walkcount//12]),(p1.x,p1.y))
            p1.walkcount+=1
        elif p1.direction==1:
            gameWindow.blit((p1.sprite[1][p1.walkcount//12]),(p1.x,p1.y))
            p1.walkcount+=1
        elif p1.direction==2:
            gameWindow.blit((p1.sprite[2][p1.walkcount//12]),(p1.x,p1.y))
            p1.walkcount+=1
        elif p1.direction==3:
            gameWindow.blit((p1.sprite[3][p1.walkcount//12]),(p1.x,p1.y))
            p1.walkcount+=1
        else:
            gameWindow.blit((p1.sprite[4][0]),(p1.x,p1.y))
            p1.walkcount+=1

        #draws ghost sprites
        for i in range(4):
            gameWindow.blit(g.npc[i].sprite, (g.npc[i].x, g.npc[i].y))

        #draws gamebar above the playfield
        pygame.draw.rect(gameWindow, (0, 0, 0), gamebar, 0)
        pygame.draw.rect(gameWindow, (11, 3, 251), gamebar, 2)

        #draws hitboxes of player and npcs if eneabled
        if showhitboxes == True:
            pygame.draw.rect(gameWindow, (255, 0, 0), p1.hitbox, 2)
            for i in range(4):
                pygame.draw.rect(gameWindow, (255, 0, 0), g.npc[i].hitbox, 2)

        #draws sprites in gamebar
        collectablesprite = [pygame.image.load("Graphics/Items/item_3_cherry.png"),pygame.image.load("Graphics/Items/item_3_strawberry.png"),pygame.image.load("Graphics/Items/item_3_banana.png") ]
        for i in range (p1.level):
            if p1.cherrys[i-1]:
                gameWindow.blit(collectablesprite[i], (((107+(4*i)) * screenWidth / 120), screenHeight / 23))

        # draws lifes in gamebar
        lifesprite = pygame.image.load("Graphics/Menus/lifes_symbol.png")
        for i in range (p1.lifes):
            gameWindow.blit(lifesprite, (((132+(8*i)) * screenWidth / 240), screenHeight / 23))

        #draws hub in gamebar
        gameWindow.blit(m.hub.sprite, (m.hub.y, m.hub.x))

        #draws textboxes
        for i in range(numbertext):
            gameWindow.blit(text[i], text_rect[i])


        #updates the display and draws game
        pygame.display.flip()

        ####################################################################################################################

    #loop for the menu (structure basicly the same as all loops here)
    while menuRunning==True:
        #delay for inputs
        pygame.time.delay(pygametimedelay)

        #initilisation of text boxes (see the beginning of code for explanation)
        numbertext=5
        text=[]
        text_rect=[]
        for i in range(numbertext):
            text.append(font[60].render("Init", True,fontcolour))
            text_rect.append(text[i].get_rect(center=((screenWidth/2),screenHeight/2)))
        text[0]=font[60].render("PacMan", True,fontcolour)
        text_rect[0] = text[0].get_rect(center=((screenWidth/2),screenHeight/6))
        
        text[1]=font[30].render("Start Game (1)", True,fontcolour)
        text_rect[1] = text[1].get_rect(center=((screenWidth/2),3*(screenHeight/7)))
        
        text[2]=font[30].render("Load Custom Game (2)", True,fontcolour)
        text_rect[2] = text[2].get_rect(center=((screenWidth/2),4*(screenHeight/7)))
        
        text[3]=font[30].render("Map Editor (0)", True,fontcolour)
        text_rect[3] = text[3].get_rect(center=((screenWidth/2),5*(screenHeight/7)))

        text[4]=font[30].render("Exit Game (Esc)", True,fontcolour)
        text_rect[4]=text[4].get_rect(center=((screenWidth/9),2*(screenHeight/70)))


        #keyinputs for menuselection (see the beginning of code for explanation)
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                windowRunning=False
                menuRunning=False

        keys= pygame.key.get_pressed()
        if keys[pygame.K_1]:
            #open Map opens the selected map from the maps.txt file
            m.openMap(2)
            #sets the value used for the countdowns
            runtime = t.perf_counter()
            collectablestarttime = runtime
            #gamemode mainly for pausemenu
            gamemode = "normal"
            movedirection = 1
            p1 = p.Player(m.hub.spawnplayery, m.hub.spawnplayerx, runtime)
            g.npc = []
            for i in range(4):
                g.npc.append(g.Ghost(m.hub.spawnnpcy[i], m.hub.spawnnpcx[i], runtime, i, i % 2))

            gameRunning=True
            menuRunning=False

        if keys[pygame.K_2]:
            m.getAllMapDataSingleInfo()
            customgamepage=0
            customGameRunning=True
            menuRunning=False
            
        if keys[pygame.K_0]:
            m.openMap(0)
            gamemode = "editor"
            selecteditem = 1
            selecteditemsprite = m.selectSprite(1)
            editorRunning=True
            menuRunning=False
            
            
        if keys[pygame.K_ESCAPE]:
            windowRunning=False
            menuRunning=False
            
            
        gameWindow.blit(gameBackground, (0, 0))
        for i in range(numbertext):
            gameWindow.blit(text[i], text_rect[i])
        
        pygame.display.flip()

    # loop for the menu between the levels and for starting the next stage (structure basicly the same as all loops here)
    while nextLevelScreen:

        #if the player already finished stage 3 he gets connected to the endscreen
        if p1.level>=4:
            endScreen=True
            nextLevelScreen=False



        else:
            pygame.time.delay(pygametimedelay)
            menubackground = pygame.image.load("Graphics/Menus/pausemenubackground.png")

            # initilisation of text boxes (see the beginning of code for explanation)
            numbertext = 8
            text = []
            text_rect = []
            for i in range(numbertext):
                text.append(font[60].render("Init", True, fontcolour))
                text_rect.append(text[i].get_rect(center=((screenWidth / 2), screenHeight / 2)))

            text[0] = font[50].render("Stage "+str((p1.level-1)), True, fontcolour)
            text_rect[0] = text[0].get_rect(center=((screenWidth / 2), screenHeight / 6))

            text[7] = font[50].render("Completed", True, fontcolour)
            text_rect[7] = text[7].get_rect(center=((screenWidth / 2), 3*screenHeight / 12))

            text[1] = font[25].render("Score:", True, fontcolour)
            text_rect[1] = text[1].get_rect(center=((screenWidth / 2), 7 * (screenHeight / 20)))

            text[2] = font[25].render(p1.getScore(), True, fontcolour)
            text_rect[2] = text[2].get_rect(center=((screenWidth / 2), 8 * (screenHeight / 20)))

            text[3] = font[18].render("Continue", True, fontcolour)
            text_rect[3] = text[3].get_rect(center=((screenWidth / 2), 10 * (screenHeight / 20)))

            text[4] = font[18].render("to Stage {} (Space)".format((p1.level)), True, fontcolour)
            text_rect[4] = text[4].get_rect(center=((screenWidth / 2), 11 * (screenHeight / 20)))

            text[5] = font[18].render("Exit to Main Menu", True, fontcolour)
            text_rect[5] = text[5].get_rect(center=((screenWidth / 2), 13 * (screenHeight / 20)))

            text[6] = font[18].render("(Progress will be lost)(q)", True, fontcolour)
            text_rect[6] = text[6].get_rect(center=((screenWidth / 2), 14 * (screenHeight / 20)))




            # keyinputs for controll of menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    windowRunning = False
                    pauseMenuRunning = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_q]:
                menuRunning = True
                nextLevelScreen = False

            if keys[pygame.K_SPACE]:
                m.openMap(p1.level+1)
                runtime = t.perf_counter()
                collectablestarttime = runtime
                movedirection=1
                #reset of relevant variables
                p1.vel=2
                p1.boosttimer = 0
                p1.outofhub=False
                p1.x=m.hub.spawnplayery
                p1.y=m.hub.spawnplayerx
                p1.updateHitbox()
                p1.starttime=runtime
                p1.controllablestarttime = runtime
                p1.controllable = False
                movedirection=1
                p1.walkcount = 0
                p1.walktimer = 0
                p1.boost = False
                for i in range(4):
                    g.npc[i].starttime=runtime
                    if g.npc[i].npcnumber == 0 or g.npc[i].npcnumber == 1:
                        g.npc[i].movedirection = 4
                    elif g.npc[i].npcnumber == 2 or g.npc[i].npcnumber == 3:
                        g.npc[i].movedirection = 4
                    g.npc[i].countdowntilstart = (i + 1) * 7
                    g.npc[i].direction=4
                    g.npc[i].outofhub=False
                    g.npc[i].x = m.hub.spawnnpcy[i]
                    g.npc[i].y = m.hub.spawnnpcx[i]
                    g.npc[i].updateHitbox()
                    g.npc[i].started = False
                nextLevelScreen=False
                gameRunning=True




            #print screen
            gameWindow.blit(menubackground, (350, 25))
            # wird Menu schon angezeigt
            for i in range(numbertext):
                gameWindow.blit(text[i], text_rect[i])
            #for updating only one time, so background of menu is still seethroug
            if pausemenudisplay == False:
                pygame.display.flip()
                pausemenudisplay = True

    while endScreen:

        pygame.time.delay(pygametimedelay)
        menubackground = pygame.image.load("Graphics/Menus/pausemenubackground.png")
        numbertext = 8
        text = []
        text_rect = []
        for i in range(numbertext):
            text.append(font[60].render("Init", True, fontcolour))
            text_rect.append(text[i].get_rect(center=((screenWidth / 2), screenHeight / 2)))

        text[0] = font[50].render("Game", True, fontcolour)
        text_rect[0] = text[0].get_rect(center=((screenWidth / 2), screenHeight / 6))

        text[7] = font[50].render("Over", True, fontcolour)
        text_rect[7] = text[7].get_rect(center=((screenWidth / 2), 3 * screenHeight / 12))

        text[1] = font[25].render("Score:", True, fontcolour)
        text_rect[1] = text[1].get_rect(center=((screenWidth / 2), 7 * (screenHeight / 20)))

        text[2] = font[25].render(p1.getScore(), True, fontcolour)
        text_rect[2] = text[2].get_rect(center=((screenWidth / 2), 8 * (screenHeight / 20)))

        text[3] = font[18].render("Collectables:", True, fontcolour)
        text_rect[3] = text[3].get_rect(center=((screenWidth / 2), 10 * (screenHeight / 20)))

        collectablesprite = [pygame.image.load("Graphics/Items/item_3_cherry.png"),
                             pygame.image.load("Graphics/Items/item_3_strawberry.png"),
                             pygame.image.load("Graphics/Items/item_3_banana.png")]
        for i in range(p1.cherrysnumber):
            gameWindow.blit(collectablesprite[i], (((54 + (4 * i)) * screenWidth / 120), 41*(screenHeight / 80)))

        text[4] = font[18].render("", True, fontcolour)
        text_rect[4] = text[4].get_rect(center=((screenWidth / 2), 11 * (screenHeight / 20)))

        text[5] = font[18].render("Completed Stages: "+str(p1.level), True, fontcolour)
        text_rect[5] = text[5].get_rect(center=((screenWidth / 2), 13 * (screenHeight / 20)))

        text[6] = font[18].render("Exit to Main Menu (q)", True, fontcolour)
        text_rect[6] = text[6].get_rect(center=((screenWidth / 2), 14 * (screenHeight / 20)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                windowRunning = False
            pauseMenuRunning = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            menuRunning = True
            endScreen = False


        gameWindow.blit(menubackground, (350, 25))
        # wird Menu schon angezeigt
        for i in range(numbertext):
            gameWindow.blit(text[i], text_rect[i])
        if pausemenudisplay == False:
            pygame.display.flip()
            pausemenudisplay = True




    while pauseMenuRunning:
        pygame.time.delay(pygametimedelay)
        menubackground=pygame.image.load("Graphics/Menus/pausemenubackground.png")
        numbertext=3
        text=[]
        text_rect=[]
        for i in range(numbertext):
            text.append(font[60].render("Init", True,fontcolour))
            text_rect.append(text[i].get_rect(center=((screenWidth/2),screenHeight/2)))

        text[0]=font[50].render("Pause", True,fontcolour)
        text_rect[0]=text[0].get_rect(center=((screenWidth/2),screenHeight/6))
        
        if currentmode=="editor": 
            text[1]=font[18].render("Save and Exit to Main Menu (s)", True,fontcolour)
            text_rect[1]=text[1].get_rect(center=((screenWidth/2),4*(screenHeight/7)))

            text[2]=font[18].render("Exit to Main Menu without saving (q)", True,fontcolour)
            text_rect[2]=text[2].get_rect(center=((screenWidth/2),3*(screenHeight/7)))

        if currentmode=="game":
            text[1]=font[18].render("Exit to Main Menu", True,fontcolour)
            text_rect[1]=text[1].get_rect(center=((screenWidth/2),9*(screenHeight/20)))
            
            text[2]=font[18].render("(Progress will be lost)(q)", True,fontcolour)
            text_rect[2]=text[2].get_rect(center=((screenWidth/2),10*(screenHeight/20)))

        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                windowRunning=False
                pauseMenuRunning=False

        keys= pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if currentmode=="game":
                gameRunning=True
                pauseMenuRunning=False
            if currentmode=="editor":
                editorRunning=True
                pauseMenuRunning=False

        if keys[pygame.K_s]:
            if currentmode=="game":
                pass
            if currentmode=="editor":
                m.saveCurrentMap(mapauthor)
                menuRunning=True
                pauseMenuRunning=False

        if keys[pygame.K_q]:

            menuRunning=True
            pauseMenuRunning=False

        gameWindow.blit(menubackground, (350, 25))
         #wird Menu schon angezeigt
        for i in range(numbertext):
            gameWindow.blit(text[i], text_rect[i])
        if pausemenudisplay==False:
            
            pygame.display.flip()
            pausemenudisplay=True





    while customGameRunning:

        pygame.time.delay(pygametimedelay)
        
        numbertext=8
        text=[]
        text_rect=[]
        for i in range(numbertext):
            text.append(font[60].render("Init", True,fontcolour))
            text_rect.append(text[i].get_rect(center=((screenWidth/2),screenHeight/2)))

        text[0]=font[50].render("Load Custom Game", True,fontcolour)
        text_rect[0]=text[0].get_rect(center=((screenWidth/2),1*(screenHeight/6)))
        
        text[1]=font[30].render("(1) "+m.singlemapdata[customgamepage+0], True,fontcolour)
        text_rect[1]=text[1].get_rect(center=((screenWidth/2),2*(screenHeight/7)))

        text[2]=font[30].render("(2) "+m.singlemapdata[customgamepage+1], True,fontcolour)
        text_rect[2]=text[2].get_rect(center=((screenWidth/2),3*(screenHeight/7)))

        text[3]=font[30].render("(3) "+m.singlemapdata[customgamepage+2], True,fontcolour)
        text_rect[3]=text[3].get_rect(center=((screenWidth/2),4*(screenHeight/7)))

        text[4]=font[30].render("(4) "+m.singlemapdata[customgamepage+3], True,fontcolour)
        text_rect[4]=text[4].get_rect(center=((screenWidth/2),5*(screenHeight/7)))

        text[5]=font[30].render("(5) "+m.singlemapdata[customgamepage+4], True,fontcolour)
        text_rect[5]=text[5].get_rect(center=((screenWidth/2),6*(screenHeight/7)))

        text[6]=font[30].render("Up (Up Key) Down (Down Key)", True,fontcolour)
        text_rect[6]=text[6].get_rect(center=((screenWidth/2),19*(screenHeight/20)))
        
        text[7]=font[30].render("Exit to Main Menu (Esc)", True,fontcolour)
        text_rect[7]=text[7].get_rect(center=((screenWidth/9),2*(screenHeight/70)))

        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                windowRunning=False
                customGameRunning=False
        
        keys= pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            menuRunning=True
            customGameRunning=False

        if keys[pygame.K_DOWN]:

            if customgamepage==mapnumber-5:
                pass
            elif customgamepage<mapnumber-5:
                customgamepage+=1
            
        if keys[pygame.K_UP]:    
            if customgamepage==0:
                pass
            elif customgamepage>0:
                customgamepage-=1
        
        if keys[pygame.K_1]:
            m.openMap((customgamepage+1)-1)
            runtime = t.perf_counter()
            collectablestarttime=runtime
            gamemode = "custom"
            movedirection = 1
            p1= p.Player(m.hub.spawnplayery,m.hub.spawnplayerx, runtime)
            g.npc=[]
            for i in range(4):
                g.npc.append(g.Ghost(m.hub.spawnnpcy[i], m.hub.spawnnpcx[i],runtime,i,i%2))

            gameRunning=True
            customGameRunning=False
        if keys[pygame.K_2]:
            m.openMap((customgamepage+2)-1)
            runtime = t.perf_counter()
            collectablestarttime = runtime
            gamemode = "custom"
            movedirection = 1
            p1 = p.Player(m.hub.spawnplayery, m.hub.spawnplayerx, runtime)
            g.npc = []
            for i in range(4):
                g.npc.append(g.Ghost(m.hub.spawnnpcy[i], m.hub.spawnnpcx[i], runtime, i, i % 2))
            gameRunning=True
            customGameRunning=False

        if keys[pygame.K_3]:
            m.openMap((customgamepage+3)-1)
            runtime = t.perf_counter()
            collectablestarttime = runtime
            gamemode = "custom"
            movedirection = 1
            p1 = p.Player(m.hub.spawnplayery, m.hub.spawnplayerx, runtime)
            g.npc = []
            for i in range(4):
                g.npc.append(g.Ghost(m.hub.spawnnpcy[i], m.hub.spawnnpcx[i], runtime, i, i % 2))
            gameRunning=True
            customGameRunning=False

        if keys[pygame.K_4]:
            m.openMap((customgamepage+4)-1)
            runtime = t.perf_counter()
            collectablestarttime = runtime
            gamemode = "custom"
            movedirection = 1
            p1 = p.Player(m.hub.spawnplayery, m.hub.spawnplayerx, runtime)
            g.npc = []
            for i in range(4):
                g.npc.append(g.Ghost(m.hub.spawnnpcy[i], m.hub.spawnnpcx[i], runtime, i, i % 2))
            gameRunning=True
            customGameRunning=False

        if keys[pygame.K_5]:
            m.openMap((customgamepage+5)-1)
            runtime = t.perf_counter()
            collectablestarttime = runtime
            gamemode = "custom"
            movedirection = 1
            p1 = p.Player(m.hub.spawnplayery, m.hub.spawnplayerx, runtime)
            g.npc = []
            for i in range(4):
                g.npc.append(g.Ghost(m.hub.spawnnpcy[i], m.hub.spawnnpcx[i], runtime, i, i % 2))
            gameRunning=True
            customGameRunning=False

            
        gameWindow.blit(gameBackground, (0, 0))
        for i in range(numbertext):
            gameWindow.blit(text[i], text_rect[i])
        pygame.display.flip()




            
    while editorRunning:
        pygame.time.delay(pygametimedelay)


        numbertext=3
        text=[]
        text_rect=[]
        for i in range(numbertext):
            text.append(font[60].render("Init", True,fontcolour))
            text_rect.append(text[i].get_rect(topleft=(0*(screenWidth/2),screenHeight/2)))
        text[0]=font[30].render("Pause Menu (Esc)", True,fontcolour)
        text_rect[0]=text[0].get_rect(topleft=(0*(screenWidth/50),1*(screenHeight/70)))

        text[1] = font[20].render("Select a block with the scrollwheel and place it with a left click. Save in the menu or (s).", True, fontcolour)
        text_rect[1] = text[0].get_rect(topleft=(2*(screenWidth / 8), 1 * (screenHeight / 70)))

        text[2] = font[20].render("",True, fontcolour)
        text_rect[2] = text[0].get_rect(topleft=(2*(screenWidth / 8),  4* (screenHeight / 70)))

        text[2] = font[20].render("New maps will show up in custom game as last entry after a restart of the game",True, fontcolour)
        text_rect[2] = text[0].get_rect(topleft=(2*(screenWidth / 8), 4 * (screenHeight / 70)))

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                windowRunning=False
                editorRunning=False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button==1:
                
                    mousepos=pygame.mouse.get_pos()
                    mousepos=[int((mousepos[0]-m.fieldstartx)/m.blocksizex),int((mousepos[1]-m.fieldstarty)/m.blocksizey)]
                    if mousepos[0] >=0 and mousepos[1]>=0:
                        m.changeBlock(selecteditem, mousepos[0], mousepos[1])

                elif event.button==3:
                
                    mousepos=pygame.mouse.get_pos()
                    mousepos=[int((mousepos[0]-m.fieldstartx)/m.blocksizex),int((mousepos[1]-m.fieldstarty)/m.blocksizey)]
                    if mousepos[0] >=0 and mousepos[1]>=0:
                        m.changeBlock(selecteditem, mousepos[0], mousepos[1])
                elif event.button==4:
                    if selecteditem <2:
                        selecteditem+=1
                    elif selecteditem >=2:
                        selecteditem=0
                        
                elif event.button==5:
                    if (selecteditem <=2)and (selecteditem >0):
                        selecteditem-=1
                    elif selecteditem <=0:
                        selecteditem=2
                
            keys= pygame.key.get_pressed()
            if keys[pygame.K_s]:
                m.saveCurrentMap("##")
                menuRunning=True
                editorRunning=False
                
            if keys[pygame.K_ESCAPE]:
                currentmode="editor"
                pausemenudisplay=False
                pauseMenuRunning=True
                editorRunning=False



        selecteditemsprite = m.selectSprite(selecteditem)





        pygame.draw.rect(gameWindow, (0, 0, 0), gamebar, 0)
        pygame.draw.rect(gameWindow, (11, 3, 251), gamebar, 2)
        gameWindow.blit(gameBackground, (0, 0))
        showhitboxes = False
        for i in range(numbertext):
            gameWindow.blit(text[i], text_rect[i])
        mousepos=pygame.mouse.get_pos()
        gameWindow.blit(selecteditemsprite, (mousepos[0]-int(m.blocksizey/2),(mousepos[1]-int(m.blocksizex/2))))

        for i in range(m.mapydirection):
            for j in range(m.mapxdirection):
                gameWindow.blit(m.mapdata[i][j].sprite, (m.mapdata[i][j].y, m.mapdata[i][j].x))
                if m.mapdata[i][j].blocktype == "Empty":
                    gameWindow.blit(m.mapdata[i][j].itemsprite, (m.mapdata[i][j].y, m.mapdata[i][j].x))

                if showhitboxes == True:
                    if m.mapdata[i][j].blocktype == "Empty":
                        pass
                        # pygame.draw.rect(gameWindow, (255, 0, 0), m.mapdata[i][j].itemhitbox, 2)
                    pygame.draw.rect(gameWindow, (20, 20, 20), m.mapdata[i][j].hitbox, 2)

        gameWindow.blit(m.hub.sprite, (m.hub.y, m.hub.x))
        pygame.display.flip()





    #menu.startMenu()
pygame.quit()
sys.exit()


