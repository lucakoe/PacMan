import pygame
import maps as m
import blocks
global npcblockwall
npcblockwall=blocks.Wall(m.hub.x,m.hub.y + (m.hub.width * 3))

npc=[]
class Ghost:
    name = ""
    x = 0
    y = 0
    width = 40
    height = 40
    vel = 2  # velocity
    direction = 4
    npcnumber=0
    respawntimer=5
    vulnerable=False
    outofhub = False
    starttime=0
    passiveoractive=0 #0 = random , 1=agressive and 2 = defensive

    movedirection=4
    movabledirections=[0,1,2,3]
    started=False #can't ghost go out of hub
    ghostdelay=0

    def __init__(self, xvaluewindow, yvaluewindow,starttime,npcnumber, passiveoractive):
        self.name = self.name
        self.x = xvaluewindow
        self.y = yvaluewindow
        self.hitboxdata = (self.x, self.y, self.width, self.height)
        self.hitbox = pygame.Rect(self.hitboxdata)
        self.ghosthitbox = self.hitbox
        self.passiveoractive = passiveoractive
        self.npcnumber=npcnumber
        self.starttime = starttime
        self.countdowntilstart=(npcnumber+1)*7
        if self.npcnumber == 0:
            self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_normal.png")
        elif self.npcnumber == 1:
            self.sprite = pygame.image.load("Graphics\Ghosts\ghost_1_normal.png")
        elif self.npcnumber == 2:
            self.sprite = pygame.image.load("Graphics\Ghosts\ghost_2_normal.png")
        elif self.npcnumber == 3:
            self.sprite = pygame.image.load("Graphics\Ghosts\ghost_3_normal.png")
        else:
            self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_normal.png")
        '''
        if npcnumber==0 or npcnumber==1:
            self.movedirection = 2
        elif npcnumber==2 or npcnumber==3:
            self.movedirection = 0
            '''


    def updateHitbox(self):
        self.hitboxdata = (self.x, self.y, self.width, self.height)
        self.hitbox = pygame.Rect(self.hitboxdata)

    def createGhostHitbox(self, direction):  # direction 0=left 1=up 2=right 3=down
        if direction == 0:
            self.ghosthitbox = pygame.Rect((self.x - 1, self.y, self.width, self.height))

        elif direction == 1:
            self.ghosthitbox = pygame.Rect((self.x, self.y - 1, self.width, self.height))

        elif direction == 2:
            self.ghosthitbox = pygame.Rect((self.x + 1, self.y, self.width, self.height))

        elif direction == 3:
            self.ghosthitbox = pygame.Rect((self.x, self.y + 1, self.width, self.height))

        if self.movedirection==1:
            self.movabledirections=[0,1,2]
        elif self.movedirection==2:
            self.movabledirections=[3,1,2]
        elif self.movedirection==3:
            self.movabledirections=[0,3,2]
        elif self.movedirection==0:
            self.movabledirections=[0,1,3]


    def checkCollition(self,objecttype):  # checks if one pixel infront is a block (if blocktype==0) or if collide with item (if blocktype==1) or if player is outside of hub (if blockype==2) or with Player (if blocktype==3)
        if objecttype == 0:
            self.updateHitbox()
            for i in range(m.mapydirection):
                for j in range(m.mapxdirection):
                    if m.mapdata[i][j].hitable == True:
                        if self.ghosthitbox.colliderect(m.mapdata[i][j].hitbox):
                            return True

            if self.outofhub == True:
                if (self.ghosthitbox.colliderect(m.hub.hitbox) and (m.hub.hitable) == True):
                    return True

            if (self.hitbox.colliderect(m.hub.hitbox)) != True:
                self.outofhub = True

            return False



    def die(self):
        self.direction=1
        self.x=m.hub.spawnnpcx[npcnumber]
        self.y = m.hub.spawnnpcy[npcnumber]
        self.started=False

    def changeVulnerableState(self):
        if self.passiveoractive==1:
            self.passiveoractive=2
            self.vulnerable=True
            if self.npcnumber == 0:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_vulnerable.png")
            elif self.npcnumber == 1:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_1_vulnerable.png")
            elif self.npcnumber == 2:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_2_vulnerable.png")
            elif self.npcnumber == 3:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_3_vulnerable.png")
            else:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_vulnerable.png")
        elif self.passiveoractive==2:
            self.passiveoractive=1
            self.vulnerable = False
            if self.npcnumber==0:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_normal.png")
            elif self.npcnumber==1:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_1_normal.png")
            elif self.npcnumber==2:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_2_normal.png")
            elif self.npcnumber==3:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_3_normal.png")
            else:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_normal.png")

        elif self.vulnerable== True:
            self.vulnerable=False

            if self.npcnumber==0:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_normal.png")
            elif self.npcnumber==1:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_1_normal.png")
            elif self.npcnumber==2:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_2_normal.png")
            elif self.npcnumber==3:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_3_normal.png")
            else:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_normal.png")

        elif self.vulnerable== False:
            self.vulnerable=True
            if self.npcnumber == 0:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_vulnerable.png")
            elif self.npcnumber == 1:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_1_vulnerable.png")
            elif self.npcnumber == 2:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_2_vulnerable.png")
            elif self.npcnumber == 3:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_3_vulnerable.png")
            else:
                self.sprite = pygame.image.load("Graphics\Ghosts\ghost_0_vulnerable.png")





        
    '''
    def moveDirection(self, direction): #direction left=0 up=1 right=2 down=3


        if direction==0:
            if p1.x < -p1.width+p1.vel:
                p1.x=screenWidth
            p1.x-=p1.vel

        if direction==1:
            if  p1.y < -p1.height+p1.vel:
                p1.y=screenHeight
            p1.y-=p1.vel
            
        if direction==2:
            if p1.x > screenWidth -p1.vel:
                p1.x=-p1.width
            p1.x+=p1.vel

        if direction==3:
            if  p1.y > screenHeight - p1.vel :
                p1.y= -p1.width
            p1.y+=p1.vel
    '''
