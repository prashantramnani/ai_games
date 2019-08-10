import sys
import pygame
import numpy as np
import random


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
screenSize = width, height = 500, 500


    
######################################################################3
def drawSnake(snake, screen):
    for l in snake:
        screen.fill(blue, rect = [l[0],l[1],10,10])
    

def drawApple(a,screen):
    screen.fill(red, rect=[a[0],a[1],10,10])

def drawWall(screen):
    screen.fill(black, rect=[0,0,10,500])
    screen.fill(black, rect=[0,0,500,10])
    screen.fill(black, rect=[490,0,10,500])
    screen.fill(black, rect=[0,490,500,10])
#############################################################################3
def collisionWithApple(snake ,applePos):
    for x in snake:
        # print(x.type,applePos.type)
        if list(x) == applePos:
            return 1
    return 0 


def collisionWithWall(snake,directionVec = None):
    if directionVec is None:
        directionVec = snake[0] - snake[1]
    a = snake[0] + directionVec
    if a[0] > 490 or a[0] < 0 or a[1] > 490 or a[1] < 0:
        return 1
    return 0    

def collisionWithSelf(snake):
    for x in range(1,len(snake)-1):
        if list(snake[0]) == list(snake[x]):
            return 1
    return 0     

def isBlocked(snakePos, directionVec):
    nextHeadPos = snakePos[0] + directionVec

    if collisionWithSelf(snakePos) == 1 or collisionWithWall(snakePos,directionVec) == 1:
        return 1
    else:
        return 0    

def blockedDirections(snakePos):
    currentDirectionVec  = snakePos[0] - snakePos[1]

    leftDirectionVec = np.array([currentDirectionVec[1], -currentDirectionVec[0]])
    rightDirctionVec = np.array([-currentDirectionVec[1], currentDirectionVec[0]])

    isFrontBlocked = isBlocked(snakePos,currentDirectionVec)
    isRightBlockd = isBlocked(snakePos, rightDirctionVec)
    isLeftBlocked = isBlocked(snakePos, leftDirectionVec)

    return isFrontBlocked, isRightBlockd, isLeftBlocked

def directionVectors(snakePos, applePos):
    snakeDirectionVector = snakePos[0] - snakePos[1]
    snakeAppleDirectionVec = np.array(applePos) - np.array(snakePos[0])
    
    normSnakeDirectionVector = np.linalg.norm(snakeDirectionVector)
    normSnakeAppleVec = np.linalg.norm(snakeAppleDirectionVec)

    snakeDirectionVecNormalized  = snakeDirectionVector/normSnakeDirectionVector
    appleDirectionVecNormalized = snakeAppleDirectionVec/normSnakeAppleVec

    return snakeDirectionVecNormalized, appleDirectionVecNormalized


#######################################################################################
def startPositions():
    snake = np.array([[250,250],[240,250],[230,250]])
    applePos = generateApplePos()
    return snake,applePos

def generateApplePos():
    return [random.randint(1,48)*10, random.randint(1,48)*10]
#########################################################################################
def gameLoop(display, clock):
    screen = display
    pygame.display.set_caption('SLITHER')
    screen.fill(white)
   
    snake,applePos = startPositions()
    gameExit = False
    move = [10, 0]
    drawApple(applePos,screen)
    pygame.display.update()
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if move != [10,0]:
                        move = [-10, 0]
                if event.key == pygame.K_RIGHT:
                    if move != [-10 ,0]:
                        move = [10, 0]
                if event.key == pygame.K_DOWN:
                    if move != [0, -10]:
                        move = [0, 10]
                if event.key == pygame.K_UP:
                    if move != [0, 10]:
                        move = [0, -10]  
        screen.fill(white)
        drawApple(applePos, screen)                               
        drawSnake(snake,screen)
        drawWall(screen)

        if collisionWithApple(snake,applePos):
            lenIncreaseVec = snake[len(snake)-1] - snake[len(snake)-2]
            a = np.linalg.norm(lenIncreaseVec)
            lenIncreaseVec = np.reshape(lenIncreaseVec/a,(1,2))
            snake = np.concatenate((snake,snake[len(snake)-1] + lenIncreaseVec*10))
            # print(lenIncreaseVec,snake)
            applePos = generateApplePos()
            drawApple(applePos, screen)

        if collisionWithWall(snake):
            gameExit = True

        if collisionWithSelf(snake):
            gameExit = True

        for i in range(len(snake)-1,-1,-1):
            if i == 0:
                snake[i] = snake[i] + move
            else:    
                snake[i] = snake[i-1]
        snake[snake>490] = 0
        snake[snake<0] = 500
        
        pygame.display.update()
        clock.tick(30)
        # gameExit = True


def playGame(snakePos, applePos, score, predictedDirection,screen, clock):
    screen.fill(white)
    drawSnake(snakePos, screen)
    drawApple(applePos, screen)
    drawWall(screen)
    pygame.display.update()


    currentDirectionVec = np.array(snakePos[0]) - np.array(snakePos[1])
    leftDirectionVec = np.array([currentDirectionVec[1], -currentDirectionVec[0]])
    rightDirctionVec = np.array([-currentDirectionVec[1], currentDirectionVec[0]])
    collisionWithWallOrSelf = 0

    if collisionWithWall(snakePos):
        collisionWithWallOrSelf = 1

    if collisionWithSelf(snakePos):
        collisionWithWallOrSelf = 1

    if(predictedDirection == 0):
        for i in range(len(snakePos)-1,-1,-1):
            if i == 0:
                snakePos[i] = snakePos[i] + leftDirectionVec
            else:    
                snakePos[i] = snakePos[i-1]        

    elif(predictedDirection == 1):
        for i in range(len(snakePos)-1,-1,-1):
            if i == 0:
                snakePos[i] = snakePos[i] + currentDirectionVec
            else:    
                snakePos[i] = snakePos[i-1]  

    else:
        for i in range(len(snakePos)-1,-1,-1):
            if i == 0:
                snakePos[i] = snakePos[i] + rightDirctionVec
            else:    
                snakePos[i] = snakePos[i-1]

    if collisionWithApple(snakePos,applePos):
        score += 1
        lenIncreaseVec = snakePos[len(snakePos)-1] - snakePos[len(snakePos)-2]
        a = np.linalg.norm(lenIncreaseVec)
        lenIncreaseVec = np.reshape(lenIncreaseVec/a,(1,2))
        snakePos = np.concatenate((snakePos,snakePos[len(snakePos)-1] + lenIncreaseVec*10))
        applePos = generateApplePos()

    pygame.display.update()
    clock.tick(1000)
    # print("hi")
    return applePos, snakePos, score

#####################################################################################################333

pygame.init()
display = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
if __name__ == "__main__":
    gameLoop(display, clock)
