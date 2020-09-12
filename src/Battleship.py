import pygame as pg
import sys
import math
from src.grid import gridWrapper
from src.ship import Ship, ShipNode
import src.constants as c
class Battleship:
    def __init__(self):

        """
        @pre none
        @post Battleship class is created and is ready to be run
        @param none
        @author Daniel and Saher
        """

        #display welcome message
        print("\n=====================================\nWelcome to Battleship made by Team 14\n=====================================\n")
        #initialize pygame
        pg.init()
        #set up the mixer to play sounds in two channels, so sink sound and hit sound can happen at the same time
        pg.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
        self.channel1 = pg.mixer.Channel(0)
        self.channel2 = pg.mixer.Channel(1)
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
        #
        self.boardHighlight = pg.Surface((int(c.WIN_X / 2), int(c.WIN_Y / 2)))
        self.boardHighlight.set_alpha(99)
        self.boardHighlight.fill(c.RED)
        #initialize the clock to control framerate
        self.clock = pg.time.Clock()
        #load the images and scale them accordingly
        self.bg = pg.transform.scale(pg.image.load("media/background-day.jpg"), (c.WIN_X, c.WIN_Y))
        self.hit = pg.transform.scale(pg.image.load("media/redX.png"), (c.SQUARE_SIZE, c.SQUARE_SIZE))
        self.miss = pg.transform.scale(pg.image.load("media/blackX.png"), (c.SQUARE_SIZE, c.SQUARE_SIZE))
        #sound for a ship sinking
        self.sunk_sound = pg.mixer.Sound("media/sunk.wav")
        #sound for a ship being hit
        self.hit_sound = pg.mixer.Sound("media/hit.wav")
        #initialize font object for the axis labels
        self.font = pg.font.Font('freesansbold.ttf', 44)
        #Direction vector for rotating when placing ships 
        self.shipDirectionVector = [0,1]
        #variable to keep track of the length of next placed ship
        self.lenShip = 1
        #initialize the grid
        self.gridW = gridWrapper()

    def rotateDirVec(self):

        """
        @pre none
        @post rotates the direction vector for placing ships clockwise
        @author Daniel
        """

        #rotate the direction vector clockwise
        if self.shipDirectionVector[0] == 0 and self.shipDirectionVector[1] == 1:
            self.shipDirectionVector[0] = -1
            self.shipDirectionVector[1] = 0
            #print("left")
        elif self.shipDirectionVector[0] == -1 and self.shipDirectionVector[1] == 0:
            self.shipDirectionVector[0] = 0
            self.shipDirectionVector[1] = -1
            #print("up")
        elif self.shipDirectionVector[0] == 0 and self.shipDirectionVector[1] == -1:
            self.shipDirectionVector[0] = 1
            self.shipDirectionVector[1] = 0
            #print("right")
        elif self.shipDirectionVector[0] == 1 and self.shipDirectionVector[1] == 0:
            self.shipDirectionVector[0] = 0
            self.shipDirectionVector[1] = 1
            #print("down")

    def draw(self, P1Placing, P2Placing, P1Shooting, P2Shooting):

        """
        @pre game is running
        @post The screen is updated for the next frame
        @param P1/P2Placing indicate if either player is placing. P1/P2Shooting indicates if either player is placing.
        @author Daniel and Saher
        """

        #draw the background
        self.screen.blit(self.bg, (0,0))
        #loop through all squares on the grid
        for i in range(len(self.gridW.grid)):
            for j in range(len(self.gridW.grid[0])):
                #draw vertical line on grid
                pg.draw.line(self.screen, c.BLACK, (j * c.SQUARE_SIZE, 0), (j * c.SQUARE_SIZE, c.WIN_Y), 1)
                #if the square is a ship, draw the ship only when that player is placing
                if self.gridW.grid[i][j] == "Ship":
                    if P1Placing and i > 10 and j < 10:
                        pg.draw.rect(self.screen, c.RED, (j * c.SQUARE_SIZE, i * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                    elif P2Placing and i > 10 and j > 10:
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
        if P1Placing:
            self.screen.blit(self.boardHighlight, (0, 10*c.SQUARE_SIZE, 10*c.SQUARE_SIZE, 10*c.SQUARE_SIZE))
        elif P2Placing:
            self.screen.blit(self.boardHighlight, (10*c.SQUARE_SIZE, 10*c.SQUARE_SIZE, 10*c.SQUARE_SIZE, 10*c.SQUARE_SIZE))
        elif P1Shooting:
            self.screen.blit(self.boardHighlight, (0, 0, 10*c.SQUARE_SIZE, 10*c.SQUARE_SIZE))
        elif P2Shooting:
            self.screen.blit(self.boardHighlight, (10*c.SQUARE_SIZE, 0, 10*c.SQUARE_SIZE, 10*c.SQUARE_SIZE))
        #update the display
        pg.display.update()

    def checkValidShip(self, P1Placing, P2Placing, effectiveX, effectiveY):

        """
        @pre game is running, one player is placing
        @post returns true if that ship placement results in no overslow/index errors/another ship is in the way, else false
        @param P1/P2Placing indicates which player is placing, effectiveX/Y is the converted mouse input mapped to the grid
        @author Daniel and Saher
        """

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

    def placeShip(self, effectiveX, effectiveY, P1Placing, P2Placing, ship):

        """
        @pre game is running and one of the players is placing
        @post ship is placed on grid
        @param effectiveX/Y are the converted mouse inputs. P1/P2Placing indicates which player's turn it is. Ship is the ship to be placed
        @author Daniel
        """

        #loop through all "ship squares" and place them on the grid
        for i in range(self.lenShip):
            squareX = effectiveX + self.shipDirectionVector[0] * i
            squareY = effectiveY + self.shipDirectionVector[1] * i
            self.gridW.grid[squareY][squareX] = "Ship"
            if P1Placing:
                ship.addSquare(squareX + 10, squareY - 10)
            elif P2Placing:
                ship.addSquare(squareX - 10, squareY - 10)
            else:
                print("Neither player is placing!")

    def run(self):

        """
        @pre none
        @post The game starts. The function finishes when the game finishes.
        @author Saher and Daniel
        """

        P1Placing = True
        P2Placing = False
        P1Shooting = False
        P2Shooting = False
        placedShips = 0
        p1Ships = []
        p2Ships = []
        print("\n===========================================\nPlayer 1 is now placing, look away player 2\nYou can press 'R' to rotate!\n===========================================\n")
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
                            tempShip = Ship()
                            self.placeShip(effectiveX, effectiveY, P1Placing, P2Placing, tempShip)
                            p1Ships.append(tempShip)
                            self.lenShip += 1
                            placedShips += 1
                            #if player one finishes placing, reset things for player two's turn
                            if placedShips == self.numShipsPerPlayer:
                                print("\n===========================================\nPlayer 2 is now placing, look away player 1\nYou can press 'R' to rotate!\n===========================================\n")
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
                            tempShip = Ship()
                            self.placeShip(effectiveX, effectiveY, P1Placing, P2Placing, tempShip)
                            p2Ships.append(tempShip)
                            self.lenShip += 1
                            placedShips += 1
                        else:
                            print("P2: Invalid Ship!")
                        #if all ships have been placed, player two is done placing
                        if placedShips >= self.numShipsPerPlayer * 2:
                            P2Placing = False
                            P1Shooting = True
                            print("\n=========================================================\nBoth players have placed their ships. Take turns shooting\n=========================================================\n")
                    elif P1Shooting:
                        #if the bounds are valid, shoot the square, then if a ship has said square, mark it as hit. 
                        #then, if the ship is sunk for the first time, print a message and play a sound
                        if effectiveY > 0 and effectiveY < 10 and effectiveX > 0 and effectiveX < 10 and self.gridW.grid[effectiveY][effectiveX] == "Open":
                            self.gridW.__shoot__(effectiveY, effectiveX)
                            P1Shooting = False
                            P2Shooting = True
                            for ship in p2Ships:
                                for square in ship.shipSquares:
                                    if square.x == effectiveX and square.y == effectiveY:
                                        self.channel1.play(self.hit_sound)
                                        square.hit = True
                                if ship.sunk == False and ship.checkSunk():
                                    self.channel2.play(self.sunk_sound)
                                    print("\n=====================\nPlayer 1 sunk a ship!\n=====================\n")
                        else:
                            print("P1: Invalid space!")
                    elif P2Shooting:
                        #if the bounds are valid, shoot the square, then if a ship has said square, mark it as hit. 
                        #then, if the ship is sunk for the first time, print a message and play a sound
                        if effectiveY > 0 and effectiveY < 10 and effectiveX > 10 and effectiveX <= 20 and self.gridW.grid[effectiveY][effectiveX] == "Open":
                            self.gridW.__shoot__(effectiveY, effectiveX)
                            P2Shooting = False
                            P1Shooting = True
                            for ship in p1Ships:
                                for square in ship.shipSquares:
                                    if square.x == effectiveX and square.y == effectiveY:
                                        self.channel1.play(self.hit_sound)
                                        square.hit = True
                                if ship.sunk == False and ship.checkSunk():
                                    self.channel2.play(self.sunk_sound)
                                    print("\n=====================\nPlayer 2 sunk a ship!\n=====================\n")
                        else:
                            print("P2: Invalid space!")
            #If the game ends, break the loop and finish the program
            if self.gridW.__winner__(self.numShipsPerPlayer) == True:
                break
            #update the screen for this frame
            self.draw(P1Placing, P2Placing, P1Shooting, P2Shooting)
            #advance the while loop at increments of 60FPS
            self.clock.tick(60)