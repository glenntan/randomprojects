#Battleship Game
import pygame
import sys
import time
from random import randint
pygame.init()

#Window Set-up 
screen = pygame.display.set_mode((800,550))
frame = pygame.time.Clock()
font = pygame.font.SysFont("monospace",12)

#Set up Soundtrack
pygame.mixer.music.load("battleshipSoundtrack.wav")
pygame.mixer.music.play(-1)

#To return coordinate of a mouseclick
def Mouseclick():
    finish = False
    while finish == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish == True 
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX,mouseY) = pygame.mouse.get_pos()
                finish = True
    return (mouseX,mouseY)

#To return grid from coordinate
def getGrid(coordX,coordY):
    x = coordX//50
    y = coordY//50

    row = y
    column = x + 1
    if column <= 8:
        surface = 1 #Surface
    else:
        surface = 2 #Subsea
    return [row, column, surface]

#To return text of grid for display to user
def getText(textList):

    #row
    if textList[0] != 0:
        row = chr(64+textList[0])
    else:
        row = " "

    #column
    if textList[1] == 0:
        column = " "
    elif 0 < textList[1] <= 8:
        column = textList[1] 
    else:
        column = textList[1] - 8

    #surface    
    if len(textList) == 3:
        if textList[2] == 1:
            surface = "Surface"
        else:
            surface = "Subsea"
        return [row,column,surface]
    else:
        return [row,column]

#To determine which button was pressed (3 is the most left button, followed by 2 and 1)
def getButton(coordX, coordY):
    if coordY > 445 and coordY < 540:
        if 500 < coordX < 585:
            response = 1
        elif 600 < coordX < 685:
            response = 2
        elif 700 < coordX < 785:
            response = 3
    return response

#To obtain 3 by 3 AOE for fires
def getAOE(midGrid):
    AOE = [[0,0],[0,0],[0,0],
           [0,0],[0,0],[0,0],
           [0,0],[0,0],[0,0]]

    count = 0
    for y in range(-1,2):
        for x in range(-1,2):
            if 1 <= midGrid[0] + y <= 8:
                if midGrid[1] <= 8:
                    if 1 <= midGrid[1] + x <= 8:
                        AOE[count] = [midGrid[0] + y, midGrid[1] + x]
                else:
                    if 9 <= midGrid[1] + x <= 16:
                        AOE[count] = [midGrid[0] + y, midGrid[1] + x]
            count += 1
        
    return AOE

#To randomize a random coordinate for enemy deployement and fires
def getRandomCoord():
        hitcoordx = randint(1,8)
        hitcoordy = randint(1,16)
        return [hitcoordx, hitcoordy]

#Load images and transform to desired scale

introScreenImage = pygame.image.load("introScreen.png")
introScreenImage = pygame.transform.scale(introScreenImage, (800,550))

userSurfaceImage = pygame.image.load("userSurface.png")
userSurfaceImage = pygame.transform.scale(userSurfaceImage, (800,400))
 
userBannerImage = pygame.image.load("userBanner.jpg")
userBannerImage = pygame.transform.scale(userBannerImage, (800,50))

enemySurfaceImage = pygame.image.load("enemySurface.png")
enemySurfaceImage = pygame.transform.scale(enemySurfaceImage, (801,400))

controlPanelImage = pygame.image.load("controlPanel.jpeg")
controlPanelImage = pygame.transform.scale(controlPanelImage, (800,100))

playGameButtonImage = pygame.image.load("playGame.png")
playGameButtonImage = pygame.transform.scale(playGameButtonImage, (120,40))

horizontalButtonImage = pygame.image.load("horizontal.png")
horizontalButtonImage = pygame.transform.scale(horizontalButtonImage, (85,85))

verticalButtonImage = pygame.image.load("vertical.png")
verticalButtonImage = pygame.transform.scale(verticalButtonImage, (85,85))

tryagainButtonImage = pygame.image.load("tryagain.jpeg")
tryagainButtonImage = pygame.transform.scale(tryagainButtonImage, (85,85))

yesButtonImage = pygame.image.load("yes.jpeg")
yesButtonImage = pygame.transform.scale(yesButtonImage, (85,85))

nextButtonImage = pygame.image.load("next.png")
nextButtonImage = pygame.transform.scale(nextButtonImage, (85,85))

quitButtonImage = pygame.image.load("quitgame.png")
quitButtonImage = pygame.transform.scale(quitButtonImage, (85,85))

playagainButtonImage = pygame.image.load("playagain.png")
playagainButtonImage = pygame.transform.scale(playagainButtonImage, (85,85))

userSubmarineHImage = pygame.image.load("userSubmarineH.png")
userSubmarineHImage = pygame.transform.scale(userSubmarineHImage, (130,50))

userSubmarineVImage = pygame.image.load("userSubmarineV.png")
userSubmarineVImage = pygame.transform.scale(userSubmarineVImage, (50,130))

userDestroyerHImage = pygame.image.load("userDestroyerH.png")
userDestroyerHImage = pygame.transform.scale(userDestroyerHImage, (150,50))

userDestroyerVImage = pygame.image.load("userDestroyerV.png")
userDestroyerVImage = pygame.transform.scale(userDestroyerVImage, (50,150))

explosionImage = pygame.image.load("explosion.png")
explosionImage = pygame.transform.scale(explosionImage, (50,50))

missImage = pygame.image.load("miss.png")
missImage = pygame.transform.scale(missImage, (55,55))

#####################################################################################################################

#Introduction Screen

screen.blit(introScreenImage,(0,0))
screen.blit(playGameButtonImage,(340,480))
pygame.display.flip()
buttonX, buttonY = 0,0

while buttonY < 480 or buttonY > 530 or buttonX < 340 or buttonX >460:
    buttonX, buttonY = Mouseclick()


#####################################################################################################################

#Game Begins

restartGame = True
while restartGame == True:
    restartGame = False
    #Initialize Game
    #Define 16x8 list for User and Enemy (includes both Surface and Subsea)
    userGrid = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    enemyGrid = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    #Display background
    screen.blit(userSurfaceImage,(0,50))
    screen.blit(userBannerImage,(0,0))
    screen.blit(controlPanelImage,(0,450))
    pygame.display.flip()

    #####################################################################################################################

    #Obtain coordinates of Submarine
    tryagain = True

    #Display instructions to select coordinates
    text1 = font.render("Click on the Screen to Select Coordinates for Deployment of Submarine",True,(0,0,0))
    screen.blit(controlPanelImage,(0,450))
    screen.blit(text1,(20,465))
    pygame.display.flip()

    while tryagain == True:

        tryagain = False
        userSubmarineCoordX, userSubmarineCoordY = 0,0
        userSubmarineOrientation = 0
        buttonX, buttonY = 0,0
        buttonResponse = 0
        
        #Obtain coordinates of selection 
        while userSubmarineCoordX % 50 == 0 or userSubmarineCoordY % 50 == 0 or userSubmarineCoordY < 50 or userSubmarineCoordY > 450:
            userSubmarineCoordX, userSubmarineCoordY = Mouseclick()
            screen.blit(controlPanelImage,(0,450))
            text2 = font.render("Please re-select the Coordinates for Deployment of Submarine",True,(200,0,0))
            screen.blit(controlPanelImage,(0,450))
            screen.blit(text2,(20,465))
            pygame.display.flip()

        #Convert coordinates to grids 
        userSubmarineGrid = getGrid(userSubmarineCoordX,userSubmarineCoordY)
        userSubmarineText = getText(userSubmarineGrid)

        #Display selected coordinates, buttons for orientation and for reselecting coordinates
        coordtext = "Your Submarine is to be deployed at " + str(userSubmarineText[0]) + str(userSubmarineText[1]) + " on the " + str(userSubmarineText[2])
        text3 = font.render(coordtext,True,(0,0,0))
        text4 = font.render("Please select Orientation of Submarine",True,(0,0,0))
        screen.blit(controlPanelImage,(0,450))
        screen.blit(text3,(20,465))
        screen.blit(text4,(20,480))
        screen.blit(horizontalButtonImage,(500,455))
        screen.blit(verticalButtonImage,(600,455))
        screen.blit(tryagainButtonImage,(700,455))
        pygame.display.flip()
        
        #Obtain button response
        while buttonY < 455 or buttonY > 540 or buttonX < 500 or 585 < buttonX < 600 or 685 < buttonX < 700 or buttonX >785:
            buttonX, buttonY = Mouseclick()
        buttonResponse = getButton(buttonX, buttonY)

        #User selected Select Again
        if buttonResponse == 3:
            tryagain = True
            screen.blit(controlPanelImage,(0,450))
            screen.blit(text1,(20,465))
            pygame.display.flip()

        #Display Horizontal Submarine
        elif buttonResponse == 1:
            userSubmarineOrientation = "Horizontal"
            if userSubmarineGrid[1] == 7 or userSubmarineGrid[1] == 8 or userSubmarineGrid[1] == 15 or userSubmarineGrid[1] == 16:
                tryagain = True
                text5 = font.render("Unable to deploy a Horizontal submarine at that coordinate.",True,(200,0,0))
                screen.blit(controlPanelImage,(0,450))
                screen.blit(text5,(20,465))
                screen.blit(text2,(20,480))
                pygame.display.flip()
            else:
                screen.blit(userSubmarineHImage,((userSubmarineGrid[1]-1)*50,userSubmarineGrid[0]*50 ))
                pygame.display.flip()
                
        #Display Vertical Submarine
        else:
            userSubmarineOrientation = "Vertical"
            if userSubmarineGrid[0] == 7 or userSubmarineGrid[0] == 8:
                tryagain = True
                text6 = font.render("Unable to deploy a Vertical submarine at that coordinate.",True,(200,0,0))
                screen.blit(controlPanelImage,(0,450))
                screen.blit(text6,(20,465))
                screen.blit(text2,(20,480))
                pygame.display.flip()
            else:
                screen.blit(userSubmarineVImage,((userSubmarineGrid[1]-1)*50,userSubmarineGrid[0]*50 ))
                pygame.display.flip()

    #Update position of submarine on grid
    if userSubmarineOrientation == "Horizontal":
        userGrid[userSubmarineGrid[0]-1][userSubmarineGrid[1]-1] = 'S'
        userGrid[userSubmarineGrid[0]-1][userSubmarineGrid[1]-0] = 'S'
        userGrid[userSubmarineGrid[0]-1][userSubmarineGrid[1]+1] = 'S'
    else:
        userGrid[userSubmarineGrid[0]-1][userSubmarineGrid[1]-1] = 'S'
        userGrid[userSubmarineGrid[0]-0][userSubmarineGrid[1]-1] = 'S'
        userGrid[userSubmarineGrid[0]+1][userSubmarineGrid[1]-1] = 'S'    


    #####################################################################################################################
        
    #Obtain for coordinates of Destroyer
    tryagain = True

    #Display instructions to select coordinates
    text7 = font.render("Submarine has been deployed.",True,(0,0,0))
    text8 = font.render("Click on the Screen to Select Coordinates for Deployment of Destroyer.",True,(0,0,0))
    text9 = font.render("Note: Destroyer can only be deployed on Surface level.",True,(0,0,0))
    screen.blit(controlPanelImage,(0,450))
    screen.blit(text7,(20,465))
    screen.blit(text8,(20,480))
    screen.blit(text9,(20,495))
    pygame.display.flip()

    while tryagain == True:

        tryagain = False
        userDestroyerCoordX, userDestroyerCoordY = 0,0
        userDestroyerOrientation = 0
        buttonX, buttonY = 0,0
        buttonResponse = 0
        
        #Obtain coordinates of selection
        while userDestroyerCoordX % 50 == 0 or userDestroyerCoordY % 50 == 0 or userDestroyerCoordY < 50 or userDestroyerCoordY > 450 or userDestroyerCoordX > 400:
            userDestroyerCoordX, userDestroyerCoordY = Mouseclick()
            text10 = font.render("Please re-select the Coordinates for Deployment of Destroyer",True,(200,0,0))
            text11 = font.render("Note: Destroyer can only be deployed on SURFACE level.",True,(200,0,0))
            screen.blit(controlPanelImage,(0,450))
            screen.blit(text10,(20,465))
            screen.blit(text11,(20,480))
            pygame.display.flip()

        #Convert coordinates to Grids 
        userDestroyerGrid = getGrid(userDestroyerCoordX,userDestroyerCoordY)
        userDestroyerText = getText(userDestroyerGrid)

        #Display selected coordinates, buttons for orientation and for reselecting coordinates
        coordtext = "Your Destroyer is to be deployed at " + str(userDestroyerText[0]) + str(userDestroyerText[1]) + " on the " + str(userDestroyerText[2])
        text12 = font.render(coordtext,True,(0,0,0))
        text13 = font.render("Please select Orientation of Destroyer",True,(0,0,0))
        screen.blit(controlPanelImage,(0,450))
        screen.blit(text12,(20,465))
        screen.blit(text13,(20,480))
        screen.blit(horizontalButtonImage,(500,455))
        screen.blit(verticalButtonImage,(600,455))
        screen.blit(tryagainButtonImage,(700,455))
        pygame.display.flip()
        
        #Obtain button response
        while buttonY < 455 or buttonY > 540 or buttonX < 500 or 585 < buttonX < 600 or 685 < buttonX < 700 or buttonX >785:
            buttonX, buttonY = Mouseclick()
        buttonResponse = getButton(buttonX, buttonY)

        #User selected Select Again
        if buttonResponse == 3:
            tryagain = True
            screen.blit(controlPanelImage,(0,450))
            screen.blit(text1,(20,465))
            pygame.display.flip()

        #Display Horizontal Destroyer
        elif buttonResponse == 1:
            userDestroyerOrientation = "Horizontal"
            if userDestroyerGrid[1] == 7 or userDestroyerGrid[1] == 8:
                tryagain = True
                text14 = font.render("Unable to deploy a Horizontal Destroyer at that coordinate.",True,(200,0,0))
                screen.blit(controlPanelImage,(0,450))
                screen.blit(text14,(20,465))
                screen.blit(text10,(20,480))
                pygame.display.flip()
            elif userGrid[userDestroyerGrid[0]-1][userDestroyerGrid[1]-1] == 'S' or userGrid[userDestroyerGrid[0]-1][userDestroyerGrid[1]-0] == 'S' or userGrid[userDestroyerGrid[0]-1][userDestroyerGrid[1]+1] == 'S':
                tryagain = True
                text15 = font.render("Unable to deploy at the same coordinate as Submarine.",True,(200,0,0))
                screen.blit(controlPanelImage,(0,450))
                screen.blit(text15,(20,465))
                screen.blit(text10,(20,480))
                pygame.display.flip()
            else:
                screen.blit(userDestroyerHImage,((userDestroyerGrid[1]-1)*50,userDestroyerGrid[0]*50 ))
                pygame.display.flip()
                
        #Display Vertical Destroyer
        else:
            userDestroyerOrientation = "Vertical"
            if userDestroyerGrid[0] == 7 or userDestroyerGrid[0] == 8:
                tryagain = True
                text16 = font.render("Unable to deploy a Vertical Destroyer at that coordinate.",True,(200,0,0))
                screen.blit(controlPanelImage,(0,450))
                screen.blit(text16,(20,465))
                screen.blit(text10,(20,480))
                pygame.display.flip()
            elif userGrid[userDestroyerGrid[0]-1][userDestroyerGrid[1]-1] == 'S' or userGrid[userDestroyerGrid[0]-0][userDestroyerGrid[1]-1] == 'S' or userGrid[userDestroyerGrid[0]+1][userDestroyerGrid[1]-1] == 'S':
                tryagain = True
                text17 = font.render("Unable to deploy at the same coordinate as Submarine.",True,(200,0,0))
                screen.blit(controlPanelImage,(0,450))
                screen.blit(text17,(20,465))
                screen.blit(text10,(20,480))
                pygame.display.flip()
            else:
                screen.blit(userDestroyerVImage,((userDestroyerGrid[1]-1)*50,userDestroyerGrid[0]*50 ))
                pygame.display.flip()

    #Update position of Destroyer on grid
    if userDestroyerOrientation == "Horizontal":
        userGrid[userDestroyerGrid[0]-1][userDestroyerGrid[1]-1] = 'D'
        userGrid[userDestroyerGrid[0]-1][userDestroyerGrid[1]-0] = 'D'
        userGrid[userDestroyerGrid[0]-1][userDestroyerGrid[1]+1] = 'D'
    else:
        userGrid[userDestroyerGrid[0]-1][userDestroyerGrid[1]-1] = 'D'
        userGrid[userDestroyerGrid[0]-0][userDestroyerGrid[1]-1] = 'D'
        userGrid[userDestroyerGrid[0]+1][userDestroyerGrid[1]-1] = 'D'    

    #####################################################################################################################
    #Randomize enemy position
    enemySubmarineOrientation = 0
    enemyDestroyerOrientation = 0
    enemySubmarineGrid = 0
    enemyDestroyerGrid = 0

    #Enemy Submarine
    enemySubmarineOrientation = randint(0,1) # 0 is horizontal; 1 is vertical
    occupied = True
    
    while occupied:
        enemySubmarineGrid = getRandomCoord()
        if enemySubmarineOrientation == 1 and enemySubmarineGrid[0] in range(1,7):
            occupied = False

        if enemySubmarineOrientation == 0 and (enemySubmarineGrid[1] in range(1,7) or enemySubmarineGrid[1] in range(9,15)):
            occupied = False
            
    if enemySubmarineOrientation == 0:
        enemyGrid[enemySubmarineGrid[0]-1][enemySubmarineGrid[1]-1] = 'S'
        enemyGrid[enemySubmarineGrid[0]-1][enemySubmarineGrid[1]-0] = 'S'
        enemyGrid[enemySubmarineGrid[0]-1][enemySubmarineGrid[1]+1] = 'S'
    else:
        enemyGrid[enemySubmarineGrid[0]-1][enemySubmarineGrid[1]-1] = 'S'
        enemyGrid[enemySubmarineGrid[0]-0][enemySubmarineGrid[1]-1] = 'S'
        enemyGrid[enemySubmarineGrid[0]+1][enemySubmarineGrid[1]-1] = 'S'     

    #Enemy Destroyer 
    enemyDestroyerOrientation = randint(0,1) # 0 is horizontal; 1 is vertical
    occupied = True

    while occupied:
        enemyDestroyerGrid = getRandomCoord()
        if enemyDestroyerOrientation == 1 and enemyDestroyerGrid[0] in range(1,7) and enemyDestroyerGrid[1] in range(1,9) and enemyGrid[enemyDestroyerGrid[0]-1][enemyDestroyerGrid[1]-1] != 'S' and enemyGrid[enemyDestroyerGrid[0]-0][enemyDestroyerGrid[1]-1] != 'S' and enemyGrid[enemyDestroyerGrid[0]+1][enemyDestroyerGrid[1]-1] != 'S':
            occupied = False

        if enemyDestroyerOrientation == 0 and enemyDestroyerGrid[1] in range(1,7) and enemyDestroyerGrid[0] in range(1,9) and enemyGrid[enemyDestroyerGrid[0]-1][enemyDestroyerGrid[1]-1] != 'S' and enemyGrid[enemyDestroyerGrid[0]-1][enemyDestroyerGrid[1]-0] != 'S' and enemyGrid[enemyDestroyerGrid[0]-1][enemyDestroyerGrid[1]+1] != 'S':
            occupied = False

    if enemyDestroyerOrientation == 0:
        enemyGrid[enemyDestroyerGrid[0]-1][enemyDestroyerGrid[1]-1] = 'D'
        enemyGrid[enemyDestroyerGrid[0]-1][enemyDestroyerGrid[1]-0] = 'D'
        enemyGrid[enemyDestroyerGrid[0]-1][enemyDestroyerGrid[1]+1] = 'D'
    else:
        enemyGrid[enemyDestroyerGrid[0]-1][enemyDestroyerGrid[1]-1] = 'D'
        enemyGrid[enemyDestroyerGrid[0]-0][enemyDestroyerGrid[1]-1] = 'D'
        enemyGrid[enemyDestroyerGrid[0]+1][enemyDestroyerGrid[1]-1] = 'D' 
    
    #####################################################################################################################

    #Just a holding screen     
    text18 = font.render("You battleships have been deployed! Are you ready for battle!?",True,(0,0,0))
    screen.blit(controlPanelImage,(0,450))
    screen.blit(text18,(20,465))
    screen.blit(yesButtonImage,(700,455))
    pygame.display.flip()
    buttonX, buttonY = 0,0

    while buttonY < 455 or buttonY > 540 or buttonX < 700 or buttonX >785:
        buttonX, buttonY = Mouseclick()

    #####################################################################################################################
    gameEnd = False

    while gameEnd == False:
        
        #USER FIRES
        screen.blit(enemySurfaceImage,(0,50))
        screen.blit(controlPanelImage,(0,450))
        pygame.display.flip()
        tryagain = True
        
        while tryagain == True:
            tryagain = False
            userFireCoordX, userFireCoordY = 0,0
            buttonX, buttonY = 0,0
            buttonResponse = 0

            #Display previous fires
            for elementX in range(0,8):
                for elementY in range(0,16):
                    if enemyGrid[elementX][elementY] == 'X':
                        screen.blit(missImage,((elementY)*50,(elementX+1)*50 ))
                        pygame.display.flip()
                        
                    elif enemyGrid[elementX][elementY] == '$':
                        screen.blit(explosionImage,((elementY)*50,(elementX+1)*50 ))
                        pygame.display.flip()
            
            #User fires
            text19 = font.render("Select Coordinates of Fire.",True,(0,0,0))
            text20 = font.render("Note: Area of Effect is 3 squares by 3 squares.",True,(0,0,0))
            screen.blit(controlPanelImage,(0,450))
            screen.blit(text19,(20,465))
            screen.blit(text20,(20,480))
            pygame.display.flip()

            #Obtain coordinates of selection
            while userFireCoordX % 50 == 0 or userFireCoordY % 50 == 0 or userFireCoordY < 50 or userFireCoordY > 450:
                userFireCoordX, userFireCoordY = Mouseclick()
                text21 = font.render("Please re-select the Coordinates of Fire",True,(200,0,0))
                screen.blit(controlPanelImage,(0,450))
                screen.blit(text21,(20,465))
                pygame.display.flip()

            #Convert coordinates to Grids 
            userFireGrid = getGrid(userFireCoordX,userFireCoordY)

            #Convert Fires to 3x3 Area
            userFireGridAOE = getAOE(userFireGrid)
            userFireText = []
            for elements in userFireGridAOE:
                userFireText.append(getText(elements))


            #Display selected coordinates, buttons for reselecting coordinates
            if userFireCoordX < 400:
                text22 = font.render("Fires will land on SURFACE at: ",True,(0,0,0))
            else:
                text22 = font.render("Fires will land on SUBSEA at: ",True,(0,0,0))


            text23 = font.render(str(userFireText[0][0]) + str(userFireText[0][1]) + " " + str(userFireText[1][0]) + str(userFireText[1][1]) + " " + str(userFireText[2][0]) + str(userFireText[2][1]),True,(0,0,0)) 
            text24 = font.render(str(userFireText[3][0]) + str(userFireText[3][1]) + " " + str(userFireText[4][0]) + str(userFireText[4][1]) + " " + str(userFireText[5][0]) + str(userFireText[5][1]),True,(0,0,0)) 
            text25 = font.render(str(userFireText[6][0]) + str(userFireText[6][1]) + " " + str(userFireText[7][0]) + str(userFireText[7][1]) + " " + str(userFireText[8][0]) + str(userFireText[8][1]),True,(0,0,0)) 

            screen.blit(controlPanelImage,(0,450))
            screen.blit(text22,(20,465))
            screen.blit(text23,(235,465))
            screen.blit(text24,(235,480))
            screen.blit(text25,(235,495))
            screen.blit(yesButtonImage,(600,455))
            screen.blit(tryagainButtonImage,(700,455))
            pygame.display.flip()

            #Obtain button response
            while buttonY < 455 or buttonY > 540 or buttonX < 600 or 685 < buttonX < 700 or buttonX >785:
                buttonX, buttonY = Mouseclick()
            buttonResponse = getButton(buttonX, buttonY)

            #User selected Select Again
            if buttonResponse == 3:
                tryagain = True
                continue

            
            #Update screen and grid with new shots     
            for element in userFireGridAOE:
                if element[1] != 0 and element[0] != 0:
                    if enemyGrid[element[0]-1][element[1]-1] == 0:
                        screen.blit(missImage,((element[1]-1)*50,element[0]*50 ))
                        pygame.display.flip()

                        enemyGrid[element[0]-1][element[1]-1] = 'X'
                        
                    elif enemyGrid[element[0]-1][element[1]-1] == 'S' or enemyGrid[element[0]-1][element[1]-1] == 'D':
                        screen.blit(explosionImage,((element[1]-1)*50,element[0]*50 ))
                        pygame.display.flip()

                        enemyGrid[element[0]-1][element[1]-1] = '$'
  
            #Display status of Game
            enemyStatus = 0
            for element in enemyGrid:
                enemyStatus += element.count('$')

            if enemyStatus == 0:
                text26 = font.render("All your shots missed! Try harder!",True,(0,0,0))
            elif 1 <= enemyStatus <= 4:
                text26 = font.render("You have hit " + str(enemyStatus) + " out of the 6 grids! KEEP IT UP!",True,(0,0,0))
            elif enemyStatus == 5:
                text26 = font.render("Just one more shot to go!!!",True,(0,0,0))
            else:
                text26 = font.render("Congratulations! You have won! All enemy ships have been destroyed!",True,(200,0,0))
                gameEnd = True

            screen.blit(controlPanelImage,(0,450))
            screen.blit(text26,(20,465))
            screen.blit(nextButtonImage,(700,455))
            pygame.display.flip()
            buttonX, buttonY = 0,0
            
            while buttonY < 455 or buttonY > 540 or buttonX < 700 or buttonX >785:
                buttonX, buttonY = Mouseclick()

    #####################################################################################################################
        
        #ENEMY FIRES
        tryagain = True
        
        while tryagain == True and gameEnd == False:
            screen.blit(userSurfaceImage,(0,50))
            screen.blit(controlPanelImage,(0,450))
            pygame.display.flip()
            tryagain = False
            enemyFireCoordX, enemyFireCoordY = 0,0
            buttonX, buttonY = 0,0
            buttonResponse = 0

            #Display ships
            if userSubmarineOrientation == "Horizontal":
                screen.blit(userSubmarineHImage,((userSubmarineGrid[1]-1)*50,userSubmarineGrid[0]*50 ))
            else:
                screen.blit(userSubmarineVImage,((userSubmarineGrid[1]-1)*50,userSubmarineGrid[0]*50 ))
                

            if userDestroyerOrientation == "Horizontal":
                screen.blit(userDestroyerHImage,((userDestroyerGrid[1]-1)*50,userDestroyerGrid[0]*50 ))
            else:
                screen.blit(userDestroyerVImage,((userDestroyerGrid[1]-1)*50,userDestroyerGrid[0]*50 ))

            #Display previous fires
            for elementX in range(0,8):
                for elementY in range(0,16):
                    if userGrid[elementX][elementY] == 'X':
                        screen.blit(missImage,((elementY)*50,(elementX+1)*50 ))
                        pygame.display.flip()
                        
                    elif userGrid[elementX][elementY] == '$':
                        screen.blit(explosionImage,((elementY)*50,(elementX+1)*50 ))
                        pygame.display.flip()

            #Obtain grid to of enemyfire
            enemyFireGrid = getRandomCoord()

            #Convert Fires to 3x3 Area
            enemyFireGridAOE = getAOE(enemyFireGrid)
            enemyFireText = []
            for elements in enemyFireGridAOE:
                enemyFireText.append(getText(elements))

            #Display selected coordinates, buttons for reselecting coordinates
            text27 = font.render("Brace yourself from enemy fires!",True,(0,0,0))
            screen.blit(controlPanelImage,(0,450))
            screen.blit(text27,(20,465))
            screen.blit(nextButtonImage,(700,455))
            pygame.display.flip()

            #Obtain button response
            while buttonY < 455 or buttonY > 540 or buttonX < 700 or buttonX >785:
                buttonX, buttonY = Mouseclick()
            buttonResponse = getButton(buttonX, buttonY)

            #Update screen and grid with new shots     
            for element in enemyFireGridAOE:
                if element[1] != 0 and element[0] != 0:
                    if userGrid[element[0]-1][element[1]-1] == 0:
                        screen.blit(missImage,((element[1]-1)*50,element[0]*50 ))
                        pygame.display.flip()

                        userGrid[element[0]-1][element[1]-1] = 'X'
                        
                    elif userGrid[element[0]-1][element[1]-1] == 'S' or userGrid[element[0]-1][element[1]-1] == 'D':
                        screen.blit(explosionImage,((element[1]-1)*50,element[0]*50 ))
                        pygame.display.flip()
                        userGrid[element[0]-1][element[1]-1] = '$'

            #Display status of Game
            userStatus = 0
            for element in userGrid:
                userStatus += element.count('$')

            if userStatus == 0:
                text28 = font.render("Phew! No ships have been damaged.",True,(0,0,0))
            elif 1 <= userStatus <= 4:
                text28 = font.render("You have been hit in " + str(userStatus) + " out of the 6 grids! Oh no!",True,(0,0,0))
            elif userStatus == 5:
                text28 = font.render("Danger Danger! One last grid left!",True,(0,0,0))
            else:
                text28 = font.render("Game Over - You Lost",True,(200,0,0))
                gameEnd = True

            screen.blit(controlPanelImage,(0,450))
            screen.blit(text28,(20,465))
            screen.blit(nextButtonImage,(700,455))
            pygame.display.flip()
            buttonX, buttonY = 0,0
            
            while buttonY < 455 or buttonY > 540 or buttonX < 700 or buttonX >785:
                buttonX, buttonY = Mouseclick()

    #Play again?
    text29 = font.render("Would you like to play again?",True,(0,0,0))
    screen.blit(text29,(20,480))
    screen.blit(playagainButtonImage,(600,455))
    screen.blit(quitButtonImage,(700,455))
    pygame.display.flip()
    buttonX, buttonY = 0,0
    buttonResponse = 0

    while buttonY < 455 or buttonY > 540 or buttonX < 600 or 685 < buttonX < 700 or buttonX >785:
        buttonX, buttonY = Mouseclick()
    buttonResponse = getButton(buttonX, buttonY)

    #User selected Play Again
    if buttonResponse == 2:
        restartGame = True
    else:
        quit()

#End 


        
        
            
        

   
            

            

        

            


