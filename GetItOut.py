import pygame
from pygame.locals import *
import random
import math
import sys

XCELL = 50
YCELL = 50
XSPACING = 10
YSPACING = 10
TOPBAR = 70

#Helper functions
def GamePosToScreenPos(pos):
    return (pos[0]*XCELL + XSPACING, pos[1] * YCELL + YSPACING + TOPBAR)

def CheckTounching(pos1, pos2, size):
    if ((pos1[0] >= pos2[0] and pos1[0] <= pos2[0] + size[0]) and (pos1[1] >= pos2[1] and pos1[1] <= pos2[1] + size[1])):
        return True
    else:
        return False

class GetItOut:
    def __init__(self, setUp):
        pygame.init()
        pygame.display.set_caption("Get It Out")

        self.xSize = setUp[0]
        self.ySize = setUp[1]
        self.balls = setUp[2]
        self.moves = setUp[3]

        self.clock = pygame.time.Clock()

        #Load assets
        self.retry = pygame.image.load('Assets/retry.png')
        self.door = pygame.image.load('Assets/door.png')
        self.ball = pygame.image.load('Assets/ball.png')
        self.closed = pygame.image.load('Assets/closed.png')

        self.screen = pygame.display.set_mode(((XCELL * self.xSize) + 2 * XSPACING, ((YCELL * self.ySize) + 2 * YSPACING + TOPBAR)))

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((200,150,200))

        if pygame.font:
            self.font = pygame.font.Font(None, 40)

        self.lost = False
        self.won = False

        self.doorLocations = []
        self.entryPoints = []
        self.openPositions = []
        self.ballPositions = []
        self.solution = []

        self.ChooseDoorLocations()
        self.setUpComplete = False
        self.SetUpPuzzle()
        self.setUpComplete = True

    def ChooseDoorLocations(self):
        for i in range (0, self.balls):
            side = random.randint(0,3)
            #It's okay to have duplicates here, as this just reduces the number of exits
            xDif = (XCELL - self.door.get_size()[0]) / 2
            yDif = (YCELL - self.door.get_size()[1]) / 2
            if side == 0 or side == 2:
                randY = random.randint(0,self.ySize - 1)
                if side == 0:
                    self.doorLocations.append((XSPACING - self.door.get_size()[0]/2, randY * YCELL + TOPBAR + YSPACING + yDif))
                    self.entryPoints.append((0, randY))
                else:
                    self.doorLocations.append((XSPACING + self.xSize * XCELL - self.door.get_size()[0]/2, randY * YCELL + TOPBAR + YSPACING + yDif))
                    self.entryPoints.append((self.xSize - 1, randY))
            else:
                randX = random.randint(0,self.xSize - 1)
                if side == 1:
                    self.doorLocations.append((randX * XCELL  + XSPACING + xDif, YSPACING + TOPBAR - self.door.get_size()[1]/2))
                    self.entryPoints.append((randX, 0))
                else:
                    self.doorLocations.append((randX * XCELL  + XSPACING + xDif, YSPACING + TOPBAR + self.ySize * YCELL - self.door.get_size()[1]/2))
                    self.entryPoints.append((randX, self.ySize - 1))
    
    def SetUpPuzzle(self):
        fullFail = True
        while fullFail == True:
            fullFail = False
            self.openPositions.clear()
            self.ballPositions.clear()
            self.solution.clear()
            self.openPositions.append(self.entryPoints[0])
            self.ballPositions.append(self.entryPoints[0])
            triedLeft, triedRight, triedUp, triedDown = False, False, False, False
            ballsRemaining = self.balls - 1
            for i in range (0, self.moves):
                #If a valid move is impossible, restart
                if fullFail == True:
                    break

                valid = False

                #Decide if to start up a new ball
                startNewBall = random.randint(0, self.moves - i)
                if (startNewBall < ballsRemaining):
                    if self.entryPoints[self.balls - ballsRemaining] not in self.ballPositions:
                        if self.entryPoints[self.balls - ballsRemaining][0] == 0:
                            if self.CheckIfMoveValid(1,0):
                                self.MoveBalls(1,0)
                                self.ballPositions.append(self.entryPoints[self.balls - ballsRemaining])
                                self.openPositions.append(self.entryPoints[self.balls - ballsRemaining])
                                ballsRemaining -= 1
                                valid = True
                        elif self.entryPoints[self.balls - ballsRemaining][0] == self.xSize - 1:
                            if self.CheckIfMoveValid(-1,0):
                                self.MoveBalls(-1,0)
                                self.ballPositions.append(self.entryPoints[self.balls - ballsRemaining])
                                self.openPositions.append(self.entryPoints[self.balls - ballsRemaining])
                                ballsRemaining -= 1
                                valid = True
                        elif self.entryPoints[self.balls - ballsRemaining][1] == 0:
                            if self.CheckIfMoveValid(0,1):
                                self.MoveBalls(0,1)
                                self.ballPositions.append(self.entryPoints[self.balls - ballsRemaining])
                                self.openPositions.append(self.entryPoints[self.balls - ballsRemaining])
                                ballsRemaining -= 1
                                valid = True
                        elif self.entryPoints[self.balls - ballsRemaining][1] == self.ySize - 1:
                            if self.CheckIfMoveValid(0,-1):
                                self.MoveBalls(0,-1)
                                self.ballPositions.append(self.entryPoints[self.balls - ballsRemaining])
                                self.openPositions.append(self.entryPoints[self.balls - ballsRemaining])
                                ballsRemaining -= 1
                                valid = True

                while valid == False:
                    valid = True
                    direction = random.randint(0,3)
                    match direction:
                        case 0:
                            move = (1,0)
                            triedRight = True
                        case 1:
                            move = (-1,0)
                            triedLeft = True
                        case 2:
                            move = (0,1)
                            triedDown = True
                        case 3:
                            move = (0,-1)
                            triedUp = True
                    if (self.CheckIfMoveValid(move[0], move[1])):
                        self.solution.append(move)
                        self.MoveBalls(move[0], move[1])
                        triedUp, triedDown, triedLeft, triedRight = False, False, False, False
                    else:
                        valid = False
                        if (triedRight == True and triedDown == True and triedLeft == True and triedUp == True):
                            #Skip to the restart
                            valid = True
                            fullFail = True

    
    def CheckIfMoveValid(self, xChange, yChange):
        for b in self.ballPositions:
            if (b[0] + xChange > self.xSize - 1):
                return False
            elif (b[0] + xChange < 0):
                return False
            elif (b[1] + yChange > self.ySize - 1):
                return False
            elif (b[1] + yChange < 0):
                return False
            #elif ((b[0] + xChange, b[1] + yChange) in self.ballPositions):
            #    return False
        return True

    def CheckIfMoveValidWithExit(self, xChange, yChange):
        for b in self.ballPositions:
            if (b[0] + xChange > self.xSize - 1):
                if b not in self.entryPoints:
                    return False
            elif (b[0] + xChange < 0):
                if b not in self.entryPoints:
                    return False
            elif (b[1] + yChange > self.ySize - 1):
                if b not in self.entryPoints:
                    return False
            elif (b[1] + yChange < 0):
                if b not in self.entryPoints:
                    return False
            elif (b[0] + xChange, b[1] + yChange) not in self.openPositions:
                return False
        return True

    def MoveBalls(self, xChange, yChange):
        for b in range(0, len(self.ballPositions)):
            self.ballPositions[b] = (self.ballPositions[b][0] + xChange, self.ballPositions[b][1] + yChange)
            if ((self.ballPositions[b][0], self.ballPositions[b][1]) not in self.openPositions) and self.setUpComplete == False:
                self.openPositions.append((self.ballPositions[b][0], self.ballPositions[b][1]))
        

    def Run(self):
        self.finished = False

        while not self.finished:
            #Handle input
            self.HandleInput()

            #Draw screen
            self.Draw()

            self.clock.tick(60)
        
        pygame.quit()
        return True

    def HandleInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if self.lost == True or self.won == True:
                    pos = pygame.mouse.get_pos()
                    if CheckTounching(pos, (self.screen.get_size()[0] - self.retry.get_size()[0] - XSPACING, 3 * YSPACING), self.retry.get_size()):
                        self.finished = True
            elif event.type == KEYDOWN:
                if self.won or self.lost:
                    return
                if event.key == K_LEFT:
                    if self.CheckIfMoveValidWithExit(-1,0):
                        self.MoveBalls(-1,0)
                        for b in self.ballPositions:
                            if (b[0] < 0 or b[1] < 0 or b[0] > self.xSize - 1 or b[1] > self.ySize - 1):
                                self.ballPositions.remove(b)
                                if len(self.ballPositions) == 0:
                                    self.won = True
                    else:
                        self.MoveBalls(-1,0)
                        self.lost = True
                if event.key == K_RIGHT:
                    if self.CheckIfMoveValidWithExit(1,0):
                        self.MoveBalls(1,0)
                        for b in self.ballPositions:
                            if (b[0] < 0 or b[1] < 0 or b[0] > self.xSize - 1 or b[1] > self.ySize - 1):
                                self.ballPositions.remove(b)
                                if len(self.ballPositions) == 0:
                                    self.won = True
                    else:
                        self.MoveBalls(1,0)
                        self.lost = True
                if event.key == K_UP:
                    if self.CheckIfMoveValidWithExit(0,-1):
                        self.MoveBalls(0,-1)
                        for b in self.ballPositions:
                            if (b[0] < 0 or b[1] < 0 or b[0] > self.xSize - 1 or b[1] > self.ySize - 1):
                                self.ballPositions.remove(b)
                                if len(self.ballPositions) == 0:
                                    self.won = True
                    else:
                        self.MoveBalls(0,-1)
                        self.lost = True
                if event.key == K_DOWN:
                    if self.CheckIfMoveValidWithExit(0,1):
                        self.MoveBalls(0,1)
                        for b in self.ballPositions:
                            if (b[0] < 0 or b[1] < 0 or b[0] > self.xSize - 1 or b[1] > self.ySize - 1):
                                self.ballPositions.remove(b)
                                if len(self.ballPositions) == 0:
                                    self.won = True
                    else:
                        self.MoveBalls(0,1)
                        self.lost = True

    
    def Draw(self):
        #clear screen
        self.screen.blit(self.background, (0,0))

        #Draw vertical lines
        topPoint = XSPACING, YSPACING + TOPBAR
        bottomPoint = XSPACING, self.ySize * YCELL + YSPACING + TOPBAR
        for i in range(0, self.xSize + 1):
            pygame.draw.line(self.screen, (10,10,10), topPoint, bottomPoint)
            topPoint = topPoint[0] + XCELL, topPoint[1]
            bottomPoint = bottomPoint[0] + XCELL, bottomPoint[1]

        #Draw horizontal lines
        leftPoint = XSPACING, YSPACING + TOPBAR
        rightPoint = XCELL * self.xSize + XSPACING, YSPACING + TOPBAR
        for i in range(0, self.ySize + 1):
            pygame.draw.line(self.screen, (10,10,10), leftPoint, rightPoint)
            leftPoint = leftPoint[0], leftPoint[1] + YCELL
            rightPoint = rightPoint[0], rightPoint[1] + YCELL
        
        #Draw doors
        for d in self.doorLocations:
            self.screen.blit(self.door, d)
        
        #Draw balls
        for b in self.ballPositions:
            self.screen.blit(self.ball, GamePosToScreenPos(b))

        #Draw closed cells
        for i in range(0, self.xSize):
            for j in range(0, self.ySize):
                if (i,j) not in self.openPositions:
                    self.screen.blit(self.closed, GamePosToScreenPos((i,j)))

        if self.lost == True or self.won == True:
            if self.lost:
                endStr = "You lose!"
            else:
                endStr = "You win!"
            endText = self.font.render(endStr, True, (10,10,10))
            self.screen.blit(endText, (XSPACING, YSPACING))
            self.screen.blit(self.retry, (self.screen.get_size()[0] - self.retry.get_size()[0] - XSPACING, 3 * YSPACING))

        #Refresh the screen
        pygame.display.flip()