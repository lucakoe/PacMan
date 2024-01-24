import pygame
import blocks



fieldstartx=0 # obere linke Ecke des Spielfelds als Pixel
fieldstarty=60
mapxdirection=25  #Ein block auf karte 50x50 Pixel groß bei Fenstergröße von 1000x500 --> 20x10 Blöcke - oben eine Leiste für Menü, Score und Leben 20x9 -->180
mapydirection=11
blocksizex=40 # größe eines Blockes auf dem Spielfeld in Pixel
blocksizey=40
mapdatasize=mapxdirection*mapydirection#Größe der Speichereinheit einer Karte.
mapsingledatainfosize=10 #Informationsteil vor den einzelnen Maps
mapdatainfosize = 130#Infoteil der Mapdatei; frei für Informationen wie gesamtzahl der Maps etc.
mapnumberinfosize=6 #Länge Infoteil der die Gesammtzahl der gespeicherten nummern enthält
collectableposx=0
collectableposy=0
collectablefieldposx=0
collectablefieldposy=0
collectableplaced=False
collectablespawned=False


mapdata=[]
hub = blocks.Hub(fieldstarty + (5 * blocksizey), fieldstartx + (10 * blocksizex), 5, 10)
singlemapdata=[]


def openMap(mapnumber):
    '''
    Die Kartendaten werden als ein langer String gespeichert, der dann in die einzelnen
    Kartendaten zerteilt wird. Die Blöcke werden abgespeichert als leer=0 block=1 hub=2.
    '''
    mapdatastart=(mapnumber*(mapdatasize+mapsingledatainfosize))+mapdatainfosize+mapnumberinfosize+mapsingledatainfosize #Startpunkt an dem die Daten der gewählten Karte anfangen
    global hub
    hub = blocks.Hub(fieldstarty + (5 * blocksizey), fieldstartx + (10 * blocksizex), 5, 10)
    with open ('Maps/maps.txt', 'r') as m:
        
        mapalldata = m.read() #Alle Kartendaten werden aus der Datei ausgelesen und in die Variable gespeichert
        mapdataraw=mapalldata[mapdatastart:(mapdatastart+mapdatasize)] #gewünschte Kartendatei wird aus allen Karten ausgeschnitten
    
    for i in range(mapydirection): #die rohen Mapdaten aus der datei werden in eine zweidimensionale Liste gepackt (zur bequemeren bearbeitung)
        mapdata.append([])
        for j in range (mapxdirection):
            mapdata[i].append([])
            mapdata[i][j]=mapdataraw[(i*mapxdirection)+j]
    wall=[]
    for i in range(mapydirection): #die daten werden ausgelesen und es werden Instanzen der dazu passenden Block-Klassen erstellt
        
        for j in range (mapxdirection):
            if mapdata[i][j]=="0":
                mapdata[i][j]=blocks.Empty(fieldstarty+(i*blocksizey),fieldstartx+(j*blocksizex),1)
            elif mapdata[i][j]=="1":
                mapdata[i][j]=blocks.Wall(fieldstarty+(i*blocksizey),fieldstartx+(j*blocksizex))
            elif mapdata[i][j]=="2":
                mapdata[i][j]= blocks.Empty(fieldstarty+(i*blocksizey),fieldstartx+(j*blocksizex),0)
                global hub
                hub=blocks.Hub(fieldstarty+(i*blocksizey),fieldstartx+(j*blocksizex) ,i,j) # Notiz: Aufpassen dass nur ein Hub plaziert wird (Ansonsten wir der Hub verwendet, der am weitesten rechts unten liegt)
                '''for i in range(4):
                    mapdata[hub.fieldposy+i][hub.fieldposx+i]= blocks.Empty(fieldstarty+((hub.fieldposy+i)*blocksizey),fieldstartx+((hub.fieldposx+i)*blocksizex))'''
            elif mapdata[i][j]=="3":
                mapdata[i][j]=blocks.Empty(fieldstarty+(i*blocksizey),fieldstartx+(j*blocksizex),2)

            elif mapdata[i][j]=="4":
                mapdata[i][j]=blocks.Empty(fieldstarty+(i*blocksizey),fieldstartx+(j*blocksizex),0)
                global collectableposx
                collectableposx = j
                global collectableposy
                collectableposy = i
                global collectablespawned
                collectablespawned = False
            elif mapdata[i][j]=="5":
                mapdata[i][j]=blocks.Empty(fieldstarty+(i*blocksizey),fieldstartx+(j*blocksizex),0)

            else:
                mapdata[i][j]=blocks.Error(fieldstarty+(i*blocksizey),fieldstartx+(j*blocksizex))

    for i in range(5):
        mapdata[hub.fieldposx][hub.fieldposy+i]= blocks.Empty(((hub.fieldposx)*blocksizey),((hub.fieldposy+i)*blocksizex),0)



def changeBlock(newblocktype, xfield, yfield):

    if newblocktype == 0:
        mapdata[yfield][xfield]=blocks.Empty(fieldstarty+(yfield*blocksizey),fieldstartx+(xfield*blocksizex),1)

    elif newblocktype == 1:
        mapdata[yfield][xfield]=blocks.Wall(fieldstarty+(yfield*blocksizey),fieldstartx+(xfield*blocksizex))

    elif newblocktype ==2:
        mapdata[yfield][xfield]=blocks.Empty(fieldstarty+(yfield*blocksizey),fieldstartx+(xfield*blocksizex),2)

    elif newblocktype ==3:
        global collectablefieldposy
        global collectablefieldposx
        global collectableplaced
        if collectableplaced==True:
            mapdata[yfield][xfield] = blocks.Empty(fieldstarty + (collectablefieldposy * blocksizey),fieldstartx + (collectablefieldposx * blocksizex), 1)
            mapdata[yfield][xfield]=blocks.Empty(fieldstarty+(yfield*blocksizey),fieldstartx+(xfield*blocksizex),3)
            collectablefieldposy=yfield
            collectablefieldposx = xfield
        else:
            mapdata[yfield][xfield] = blocks.Empty(fieldstartx + (xfield * blocksizey),fieldstarty + (xfield * blocksizex), 3)
            collectablefieldposy = yfield
            collectablefieldposx = xfield
            collectableplaced = True


    elif newblocktype == 4:
        if yfield< mapydirection-5:
            hub=blocks.Hub(fieldstartx+(xfield*blocksizex),fieldstarty+(yfield*blocksizey),xfield,yfield)
            for i in range(5):
               mapdata[hub.fieldposx][hub.fieldposy+i] = blocks.Empty(fieldstarty + (hub.fieldposx * blocksizey),fieldstartx + ((hub.fieldposy+i) * blocksizex),0)

def selectSprite(selecteditemorblock):
    if selecteditemorblock == 0:
        sprite=pygame.image.load("Graphics/Items/item_1_dot.png")

    elif selecteditemorblock == 1:
        sprite=pygame.image.load("Graphics/Blocks/wall.png")

    elif selecteditemorblock == 2:
        sprite=pygame.image.load("Graphics/Items/item_2_special_dot.png")
    elif selecteditemorblock == 3:
        sprite=pygame.image.load("Graphics/Items/item_3_cherry.png")
    elif selecteditemorblock == 4:
        sprite=pygame.image.load("Graphics/Blocks/hub.png")
    else:
        sprite=pygame.image.load("Graphics/Blocks/error.png")
    return sprite




def getAllMapDataSingleInfo():
    with open ('Maps/maps.txt', 'r') as m:
        mapalldata = m.read()
        mapnumber = int(mapalldata[mapdatainfosize+2:mapdatainfosize+mapnumberinfosize-1])+1
        for i in range (mapnumber):
        #WorkinProgress
            singlemapdata.append(mapalldata[(i*(mapdatasize+mapsingledatainfosize))+(mapdatainfosize+mapnumberinfosize+1):(i*(mapdatasize+mapsingledatainfosize))+mapdatainfosize+mapnumberinfosize+2+mapnumberinfosize+1])
        for i in range (999-mapnumber):
        #WorkinProgress
            singlemapdata.append("")    
    return mapnumber
        
def saveCurrentMap(authorsinitials): #work in progress; gesamtzahl ändert sich nicht; neuerstellte maps bekommen immer den gleichen mapzahl
    mapnumber=0
    with open ('Maps/maps.txt', 'r') as m:
        mapalldata = m.read()
        mapnumber = int(mapalldata[mapdatainfosize+2:mapdatainfosize+mapnumberinfosize-1])
    mapnumber+=1
    if mapnumber<10:
        numberout="00"+str(mapnumber)
    elif mapnumber<100:
        numberout="0"+str(mapnumber)
    elif mapnumber<1000:
        numberout=str(mapnumber)
    out=""
    for i in range(mapydirection):
        for j in range (mapxdirection):
            if mapdata[i][j].blocktype== "Empty":
                if mapdata[i][j].item==2:
                    out += "3"
                elif mapdata[i][j].item==3:
                    out += "4"
                else:
                    out+="0"
            elif mapdata[i][j].blocktype== "Wall":
                out+="1"
            elif mapdata[i][j].blocktype== "Hub":
                out+=""
            else:out+="0"
                
    if len(authorsinitials)==2:
        out="\n#"+numberout+" "+authorsinitials+" #"+out
    else:
        out="\n#"+numberout+" "+"##"+" #"+out

    with open ('Maps/maps.txt', 'a') as m1:
        m1.write(out)
    
    with open ('Maps/maps.txt', 'r') as m2:
        mapalldata = m2.read()
        
    with open ('Maps/maps.txt', 'w') as m3:
        a=mapalldata[0:mapdatainfosize+2]
        b=numberout
        c=mapalldata[mapdatainfosize+mapnumberinfosize-1:len(mapalldata)]
        mapalldata=a+b+c
        m3.write(mapalldata)

