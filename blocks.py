import pygame
import maps as m
import player as p


currentlevel=1

class Empty:
    name=""
    blocktype="Empty"

    
    def __init__(self, xvaluewindow, yvaluewindow, itemtype):
        self.name=self
        self.x=xvaluewindow
        self.y=yvaluewindow
        self.width=40
        self.height=40
        self.hitable=False
        self.sprite=pygame.image.load("Graphics/Blocks/empty.png")
        self.hitboxdata=(self.y,self.x, self.width, self.height)
        self.hitbox=pygame.Rect(self.hitboxdata)
        self.item=itemtype
        if self.item == 0:
            self.itemsprite = pygame.image.load("Graphics/Blocks/empty.png")
            self.itemhitbox=pygame.Rect((self.y,self.x, self.width, self.height))
        elif self.item == 1:
            self.itemsprite = pygame.image.load("Graphics/Items/item_1_dot.png") #10x10 px
            self.itemhitbox=pygame.Rect((self.y+15,self.x+15, self.width/4, self.height/4))

        elif self.item == 2:
            self.itemsprite = pygame.image.load("Graphics/Items/item_2_special_dot.png") #20x20 px
            self.itemhitbox = pygame.Rect((self.y + self.width / 4, self.x + self.height / 4, self.width / 2, self.height / 2))

        elif self.item == 3:
            if currentlevel==2:
                self.itemsprite = pygame.image.load("Graphics/Items/item_3_strawberry.png")  # 30x30 px
            elif currentlevel == 3:
                self.itemsprite = pygame.image.load("Graphics/Items/item_3_banana.png")  # 30x30 px
            else:
                self.itemsprite = pygame.image.load("Graphics/Items/item_3_cherry.png")  # 30x30 px

            self.itemhitbox = pygame.Rect((self.y + self.width / 8, self.x + self.height / 8, (self.width * (3/4)), (self.height  * (3/4))))

        else:
            self.itemsprite = pygame.image.load("Graphics/Blocks/empty.png")
            self.itemhitbox = self.hitbox


    #work in progress
    def changeItem(self, newitemtype):

        if newitemtype == 0:
            self.item=0
            self.itemsprite = pygame.image.load("Graphics/Blocks/empty.png")
            self.itemhitbox=pygame.Rect((self.y,self.x, self.width, self.height))

        if newitemtype == 3:
            self.item = 3
            if currentlevel==2:
                self.itemsprite = pygame.image.load("Graphics/Items/item_3_strawberry.png")  # 30x30 px
            elif currentlevel == 3:
                self.itemsprite = pygame.image.load("Graphics/Items/item_3_banana.png")  # 30x30 px
            else:
                self.itemsprite = pygame.image.load("Graphics/Items/item_3_cherry.png")  # 30x30 px

            self.itemhitbox = pygame.Rect((self.y + self.width / 8, self.x + self.height / 8, (self.width * (3 / 4)), (self.height * (3 / 4))))




class Wall:
    name=""
    blocktype="Wall"
    def __init__(self, xvaluewindow, yvaluewindow):
        self.name=self
        self.x=xvaluewindow
        self.y=yvaluewindow
        self.hitable=True
        self.sprite=pygame.image.load("Graphics/Blocks/wall.png")
        self.width=40
        self.height=40
        self.hitboxdata=(self.y,self.x, self.width, self.height)
        self.hitbox=pygame.Rect(self.hitboxdata)
class Hub:
    name=""
    blocktype="Hub"
    def __init__(self, xvaluewindow, yvaluewindow, fieldposx, fieldposy):
        self.name=self
        self.x=xvaluewindow
        self.y=yvaluewindow
        self.width=40
        self.height=40
        self.hitable=True
        self.sprite=pygame.image.load("Graphics/Blocks/hub.png")
        self.spawnplayerx=self.x
        self.spawnplayery=self.y +(self.width*2)
        self.spawnnpcy=[self.y +(self.width*0),self.y +(self.width*1),self.y +(self.width*3),self.y +(self.width*4)]
        self.spawnnpcx=[self.x,self.x,self.x,self.x]
        self.fieldposx=fieldposx
        self.fieldposy=fieldposy
        self.hitboxdata=(self.y,self.x,self.height*5,self.width)
        self.hitbox=pygame.Rect(self.hitboxdata)
class Error:
    name=""
    blocktype="Error"

    def __init__(self, xvaluewindow, yvaluewindow):
        self.name=self
        self.x=xvaluewindow
        self.y=yvaluewindow
        self.width=40
        self.height=40
        self.hitable=False
        self.sprite=pygame.image.load("Graphics/Blocks/error.png")
        self.hitboxdata=(self.y,self.x, self.width, self.height)
        self.hitbox=pygame.Rect(self.hitboxdata)
