import pygame
import maps as m
import time as t
import ghost as g

class Player:
       
    name=""
    x=0
    y=0
    level=1
    lifes=3
    cherrys=[False,False,False]
    cherrysnumber=0
    score=0
    width=40
    height=40
    vel=2 #velocity
    boost=False
    boosttimer=0
    starttime=0
    direction=1
    outofhub = False
    controllable=False
    walkcount=0
    walktimer=0
    sprite=[[pygame.image.load("Graphics/Player/Pacman_1.png"),pygame.image.load("Graphics/Player/Pacman_2l.png"),pygame.image.load("Graphics/Player/Pacman_3l.png"),pygame.image.load("Graphics/Player/Pacman_2l.png"),pygame.image.load("Graphics/Player/Pacman_1.png")],
             [pygame.image.load("Graphics/Player/Pacman_1.png"),pygame.image.load("Graphics/Player/Pacman_2o.png"),pygame.image.load("Graphics/Player/Pacman_3o.png"),pygame.image.load("Graphics/Player/Pacman_2o.png"),pygame.image.load("Graphics/Player/Pacman_1.png")],
             [pygame.image.load("Graphics/Player/Pacman_1.png"),pygame.image.load("Graphics/Player/Pacman_2r.png"),pygame.image.load("Graphics/Player/Pacman_3r.png"),pygame.image.load("Graphics/Player/Pacman_2r.png"),pygame.image.load("Graphics/Player/Pacman_1.png")],
             [pygame.image.load("Graphics/Player/Pacman_1.png"),pygame.image.load("Graphics/Player/Pacman_2u.png"), pygame.image.load("Graphics/Player/Pacman_3u.png"),pygame.image.load("Graphics/Player/Pacman_2u.png"),pygame.image.load("Graphics/Player/Pacman_1.png")],
             [pygame.image.load("Graphics/Player/Pacman_1.png")]
            ]

    #sprite=pygame.image.load("Graphics/Player/Pacman_1.png")
    def __init__(self, xvaluewindow, yvaluewindow, starttime):
        self.name=self
        self.x=xvaluewindow
        self.y=yvaluewindow
        self.hitboxdata=(self.x,self.y, self.width, self.height)
        self.hitbox=pygame.Rect(self.hitboxdata)
        self.ghosthitbox=self.hitbox
        self.starttime=starttime
        self.controllablestarttime = starttime

    def updateHitbox(self):
        self.hitboxdata=(self.x,self.y, self.width, self.height)
        self.hitbox=pygame.Rect(self.hitboxdata)

    def createGhostHitbox(self, direction): # direction 0=left 1=up 2=right 3=down
        if direction==0:
            self.ghosthitbox = pygame.Rect((self.x-1,self.y, self.width, self.height))
        if direction==1:
            self.ghosthitbox = pygame.Rect((self.x,self.y-1, self.width, self.height))
        if direction==2:
            self.ghosthitbox = pygame.Rect((self.x+1,self.y, self.width, self.height))
        if direction==3:
            self.ghosthitbox = pygame.Rect((self.x,self.y+1, self.width, self.height))

    def checkForWin(self):
        for i in range(m.mapydirection):
            for j in range (m.mapxdirection):
                if m.mapdata[i][j].blocktype=="Empty":

                    if m.mapdata[i][j].item == 1:
                        return False
                    elif m.mapdata[i][j].item != 0 or 2 or 3:
                        pass

        return True


    def checkCollition(self, objecttype): #checks if one pixel infront is a block (if blocktype==0) or if collide with item (if blocktype==1) or if player is outside of hub (if blockype==2)
        if objecttype==0:
            self.updateHitbox()
            for i in range(m.mapydirection):
                for j in range (m.mapxdirection):
                    if m.mapdata[i][j].hitable==True:
                        if self.ghosthitbox.colliderect(m.mapdata[i][j].hitbox):

                            return True

            if self.outofhub==True:
                if (self.ghosthitbox.colliderect(m.hub.hitbox) and (m.hub.hitable)==True):

                    return True

            if (self.hitbox.colliderect(m.hub.hitbox))!= True:
                self.outofhub=True

            return False

        if objecttype ==1:
            self.updateHitbox()
            for i in range(m.mapydirection):
                for j in range(m.mapxdirection):
                    if m.mapdata[i][j].blocktype == "Empty":
                        if self.hitbox.colliderect(m.mapdata[i][j].itemhitbox):

                            if m.mapdata[i][j].item == 0:
                                return 0
                            elif m.mapdata[i][j].item == 1:
                                m.mapdata[i][j].changeItem(0)
                                return 1
                            elif m.mapdata[i][j].item == 2:
                                m.mapdata[i][j].changeItem(0)
                                return 2
                            elif m.mapdata[i][j].item == 3:
                                m.mapdata[i][j].changeItem(0)
                                return 3

            return 0

        if objecttype ==2:
            self.updateHitbox()
            for i in range(4):
                if self.hitbox.colliderect(g.npc[i].hitbox):
                    return i


            return 4

    def getDamage(self):
        self.lifes-=1

    def getScore(self):
        out=""
        for i in range(9-len(str(self.score))):

            out+="0"
        out+=str(self.score)
        return out



    def pickupItem(self, item):
        if item==0:
            pass
        elif item==1:
            self.score+=10
        elif item==2:
            self.score+=100
            self.boost=True
            self.boosttimer=t.perf_counter()
            self.vel=2
            for i in range(4):
                if g.npc[i].vulnerable==False:
                    g.npc[i].changeVulnerableState()
        elif item==3:
            self.score+=1000
            self.cherrys[self.level-1]=True
            self.cherrysnumber+=1



    '''    
    def moveDirection(self, direction): #direction left=0 up=1 right=2 down=3


        if direction==0:
            if self.x < -self.width+self.vel:
                self.x=screenWidth
            self.x-=self.vel

        if direction==1:
            if  self.y < -self.height+self.vel:
                self.y=screenHeight
            self.y-=self.vel
            
        if direction==2:
            if self.x > screenWidth -self.vel:
                self.x=-self.width
            self.x+=self.vel

        if direction==3:
            if  self.y > screenHeight - self.vel :
                self.y= -self.width
            self.y+=self.vel
    '''
