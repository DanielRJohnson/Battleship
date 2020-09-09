import pygame as pg
import sys
import math
from grid import gridWrapper
import constants as c
class Battleship:
    def __init__(self):
        #initialize pygame
        pg.init()
        #set the name of the window
        pg.display.set_caption("Battleship")
        #get the number of ships per player, and protect from bad input
        while 1: 
            try: 
                self.numShipsPerPlayer = int(input("How many ships per player? (1-5): "))
                if self.numShipsPerPlayer > 5 or self.numShipsPerPlayer < 1:
                    raise Exception("OutOfRange") 
            except ValueError: 
                print("Your input was not an integer. Please input an integer between 1 and 5.")
            except Exception:
                print("Please input an integer between 1 and 5.")
            except:
                print("Something went wrong. Exiting...")
                quit()
            else:
                break
        #initialize the screen
        self.screen=pg.display.set_mode((c.WIN_X,c.WIN_Y))
        #initialize the clock to control framerate
        self.clock = pg.time.Clock()
        #load the images and scale them accordingly
        self.bg = pg.transform.scale(pg.image.load("background-day.jpg"), (c.WIN_X, c.WIN_Y))
        self.hit = pg.transform.scale(pg.image.load("redX.png"), (c.SQUARE_SIZE, c.SQUARE_SIZE))
        self.miss = pg.transform.scale(pg.image.load("blackX.png"), (c.SQUARE_SIZE, c.SQUARE_SIZE))
        #initialize font object for the axis labels
        self.font = pg.font.Font('freesansbold.ttf', 44)
        #Direction vector for rotating when placing ships 
        self.shipDirectionVector = [0,1]
        #variable to keep track of the length of next placed ship
        self.lenShip = 1
        #initialize the grid
        self.gridW = gridWrapper()

    def rotateDirVec(self):
        #rotate the direction vector clockwise
        if self.shipDirectionVector[0] == 0 and self.shipDirectionVector[1] == 1:
            self.shipDirectionVector[0] = -1
            self.shipDirectionVector[1] = 0
            print("left")
        elif self.shipDirectionVector[0] == -1 and self.shipDirectionVector[1] == 0:
            self.shipDirectionVector[0] = 0
            self.shipDirectionVector[1] = -1
            print("up")
        elif self.shipDirectionVector[0] == 0 and self.shipDirectionVector[1] == -1:
            self.shipDirectionVector[0] = 1
            self.shipDirectionVector[1] = 0
            print("right")
        elif self.shipDirectionVector[0] == 1 and self.shipDirectionVector[1] == 0:
            self.shipDirectionVector[0] = 0
            self.shipDirectionVector[1] = 1
            print("down")

    def draw(self, P1Placing, P2Placing):
        #draw the background
        self.screen.blit(self.bg, (0,0))
        #loop through all squares on the grid
        for i in range(len(self.gridW.grid)):
            for j in range(len(self.gridW.grid[0])):
                #draw vertical line on grid
                pg.draw.line(self.screen, c.BLACK, (j * c.SQUARE_SIZE, 0), (j * c.SQUARE_SIZE, c.WIN_Y), 1)
                #if the square is a ship, draw the ship
                if self.gridW.grid[i][j] == "Ship":
                    pg.draw.rect(self.screen, c.RED, (j * c.SQUARE_SIZE, i * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                #if the square is a hit, draw the hit
                elif self.gridW.grid[i][j] == "hit":
                    self.screen.blit(self.hit, (j * c.SQUARE_SIZE, i * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                #if the square is a miss, draw the miss
                elif self.gridW.grid[i][j] == "miss":
                    self.screen.blit(self.miss, (j * c.SQUARE_SIZE, i * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                #if the row is divisible by ten
                if i % 10 == 0:
                    #draw a large horizontal seperator
                    pg.draw.line(self.screen, c.BLACK, (i * c.SQUARE_SIZE, 0), (i * c.SQUARE_SIZE, c.WIN_Y), 5)
                    #if the col is divisible by ten
                    if j % 10 == 0: 
                        #draw a large vertical seperator AND don't draw the axis labels by "continue"
                        pg.draw.line(self.screen, c.BLACK, (0, j * c.SQUARE_SIZE), (c.WIN_X, j * c.SQUARE_SIZE), 5)
                        continue
                    #draw axis labels
                    self.screen.blit((self.font.render(c.Alpha[(j - 1) % 10], True, c.BLACK)), (int(j * c.SQUARE_SIZE), int(i * c.SQUARE_SIZE)))
                    self.screen.blit((self.font.render(str(j % 10), True, c.BLACK)), (int(i * c.SQUARE_SIZE + c.SQUARE_SIZE / 4), int(j * c.SQUARE_SIZE)))
            #draw horizontal line on the grid
            pg.draw.line(self.screen, c.BLACK, (0, i * c.SQUARE_SIZE), (c.WIN_X, i * c.SQUARE_SIZE), 1)
            if P1Placing or P2Placing:
                #display a mock ship and the direction it's being placed
                mousePos = pg.mouse.get_pos()
                pg.draw.line(self.screen, c.RED, (mousePos[0], mousePos[1]), (mousePos[0] + c.SQUARE_SIZE * self.lenShip * self.shipDirectionVector[0], mousePos[1] + (c.SQUARE_SIZE * self.lenShip * self.shipDirectionVector[1])), 10)
        #update the display
        pg.display.update()

    def checkValidShip(self, P1Placing, P2Placing, effectiveX, effectiveY):
        valid = True
        if P1Placing:
            #loop through all "ship squares"
            for i in range(self.lenShip):
                #if the Y coordinate is not in P1's quadrant, the ship is not valid
                if (effectiveY + self.shipDirectionVector[1] * i >= 20) or (effectiveY + self.shipDirectionVector[1] * i <= 10):
                    valid = False
                    break
                #if the X coordinate is not in P1's quadrant, the ship is not valid
                if  (effectiveX + self.shipDirectionVector[0] * i >= 10) or (effectiveX + self.shipDirectionVector[0] * i <= 0):
                    valid = False
                    break
                #if the square is already occupied by a ship, the ship is not valid
                if (self.gridW.grid[effectiveY + self.shipDirectionVector[1] * i][effectiveX + self.shipDirectionVector[0] * i] != "Open"):
                    valid = False
                    break
        elif P2Placing:
            #loop through all "ship squares"
            for i in range(self.lenShip):
                #if the Y coordinate is not in P2's quadrant, the ship is not valid
                if (effectiveY + self.shipDirectionVector[1] * i >= 20) or (effectiveY + self.shipDirectionVector[1] * i <= 10):
                    valid = False
                    break
                #if the X coordinate is not in P2's quadrant, the ship is not valid
                if  (effectiveX + self.shipDirectionVector[0] * i <= 10) or (effectiveX + self.shipDirectionVector[0] * i >= 20):
                    valid = False
                    break
                #if the square is already occupied by a ship, the ship is not valid
                if  (self.gridW.grid[effectiveY + self.shipDirectionVector[1] * i][effectiveX + self.shipDirectionVector[0] * i] != "Open"):
                    valid = False
                    break
        #if neither player is placing, there are no valid ship placements, THIS SHOULD NEVER HAPPEN
        else:
            print("Neither player is placing!")
            valid = False
        return valid

    def placeShip(self, effectiveX, effectiveY):
        #loop through all "ship squares" and place them on the grid
        for i in range(self.lenShip):
            self.gridW.grid[effectiveY + self.shipDirectionVector[1] * i][effectiveX + self.shipDirectionVector[0] * i] = "Ship"

    def run(self):
        P1Placing = True
        P2Placing = False
        placedShips = 0
        #game loop
        while 1:
            #loop through all events
            for event in pg.event.get():
                #if the window is closed, exit program
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    #if the user types "r" and someone is placing, rotate the direction vector
                    if event.key == pg.K_r and (P1Placing or P2Placing):
                        self.rotateDirVec()
                #when the user clicks, do one of three things
                if event.type == pg.MOUSEBUTTONDOWN:
                    #get the mouse position and convert it to an X/Y coordinate on the grid
                    mousePos = pg.mouse.get_pos()
                    effectiveX = math.floor(mousePos[0]/(c.WIN_Y/20))
                    effectiveY = math.floor(mousePos[1]/(c.WIN_Y/20))
                    #if player one is placing, place the ship if it is valid
                    if P1Placing:
                        if self.checkValidShip(P1Placing, P2Placing, effectiveX, effectiveY):
                            self.placeShip(effectiveX, effectiveY)
                            self.lenShip += 1
                            placedShips += 1
                            #if player one finishes placing, reset things for player two's turn
                            if placedShips == self.numShipsPerPlayer:
                                self.shipDirectionVector[0] = 0
                                self.shipDirectionVector[1] = 1
                                P1Placing = False
                                P2Placing = True
                                self.lenShip = 1
                        else:
                            print("P1: Invalid Ship!")
                    #if player two is placing, place the ship if it is valid
                    elif P2Placing:
                        if self.checkValidShip(P1Placing, P2Placing, effectiveX, effectiveY):
                            self.placeShip(effectiveX, effectiveY)
                            self.lenShip += 1
                            placedShips += 1
                        else:
                            print("P2: Invalid Ship!")
                        #if all ships have been placed, player two is done placing
                        if placedShips >= self.numShipsPerPlayer * 2:
                            P2Placing = False
                    #else:
                        #Shoot for ships
            #update the screen for this frame
            self.draw(P1Placing, P2Placing)
            #advance the while loop at increments of 60FPS
            self.clock.tick(60)