import pygame as pg
import sys
import math
import string
from grid import gridWrapper
pg.init()
pg.display.set_caption("Battleship")
clock=pg.time.Clock()
#Screen_Dsiplay_units
print("How many ships per player?")
numShipsPerPlayer = int(input())
SQUARE_SIZE = 40
WIN_X, WIN_Y = SQUARE_SIZE * 20, SQUARE_SIZE * 20
screen=pg.display.set_mode((WIN_X,WIN_Y))
bg=pg.image.load("background-day.jpg").convert()
bg=pg.transform.scale(bg, (WIN_X, WIN_Y))
hit = pg.image.load("redX.png")
hit = pg.transform.scale(hit, (SQUARE_SIZE, SQUARE_SIZE))
miss = pg.image.load("blackX.png")
miss = pg.transform.scale(miss, (SQUARE_SIZE, SQUARE_SIZE))
##Colors for reference 
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
gridW = gridWrapper()
Alpha = list(string.ascii_uppercase) 


"""sysfont = pg.font.get_default_font()
font = pg.font.SysFont('Times New Roman', 100)
img = font.render(sysfont, True, RED)
screen.blit(img, (0,0))

textW1 = pg.font.SysFont('Arial', 100, False, False).render(sysfont, True, RED)
screen.blit(textW1, (0,0))"""
font = pg.font.Font('freesansbold.ttf', 44) 

def draw(P1Placing, P2Placing):
    screen.blit(bg, (0,0))
    for i in range(20):
        for j in range(20):
            pg.draw.line(screen, BLACK, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, WIN_Y), 1)
        pg.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIN_X, i * SQUARE_SIZE), 1)
    for i in range(len(gridW.grid)):
        for j in range(len(gridW.grid[0])):
            if P1Placing and i >= 10 and j < 10:
                if gridW.grid[i][j] == "Ship":
                    pg.draw.rect(screen, RED, (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif P2Placing and j >= 10 and i >= 10:
                if gridW.grid[i][j] == "Ship":
                    pg.draw.rect(screen, RED, (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif gridW.grid[i][j] == "hitShip":
                screen.blit(hit, (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                #pg.draw.rect(screen, [0,255,0], (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif gridW.grid[i][j] == "Miss":
                screen.blit(miss, (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                #pg.draw.rect(screen, BLACK, (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pg.draw.line(screen, BLACK, (10 * SQUARE_SIZE, 0), (10 * SQUARE_SIZE, WIN_Y), 5) #Vertical Seperator
    pg.draw.line(screen, BLACK, (0, 10 * SQUARE_SIZE), (WIN_X, 10 * SQUARE_SIZE), 5) #Horizontal Seperator
    for i in range(len(gridW.grid)):
        for j in range(1, len(gridW.grid)):
            if i == 0 or i == 10:
                if j < 10:
                    screen.blit((font.render(Alpha[j - 1], True, [0,0,255])), (int(j * SQUARE_SIZE), int(i * SQUARE_SIZE)))
                    screen.blit((font.render(str(j), True, [0,0,255])), (int(i * SQUARE_SIZE + SQUARE_SIZE / 4), int(j * SQUARE_SIZE)))
                elif j > 10:
                    screen.blit((font.render(Alpha[j - 11], True, [0,0,255])), (int(j * SQUARE_SIZE), int(i * SQUARE_SIZE)))
                    screen.blit((font.render(str(j - 10), True, [0,0,255])), (int(i * SQUARE_SIZE + SQUARE_SIZE / 4), int(j * SQUARE_SIZE)))
    pg.display.update()

def main():
    P1Placing = True
    P2Placing = False
    placedShips = 0
    lenShip = 1
    dirVec = [0,1]
    while 1:
        #game loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    if dirVec[0] == 0 and dirVec[1] == 1:
                        dirVec[0] = -1
                        dirVec[1] = 0
                        print("left")
                    elif dirVec[0] == -1 and dirVec[1] == 0:
                        dirVec[0] = 0
                        dirVec[1] = -1
                        print("down")
                    elif dirVec[0] == 0 and dirVec[1] == -1:
                        dirVec[0] = 1
                        dirVec[1] = 0
                        print("right")
                    elif dirVec[0] == 1 and dirVec[1] == 0:
                        dirVec[0] = 0
                        dirVec[1] = 1
                        print("up")
            if event.type == pg.MOUSEBUTTONDOWN:
                Pressed=pg.mouse.get_pos()
                effectiveX = math.floor(Pressed[0]/(WIN_Y/20))
                effectiveY = math.floor(Pressed[1]/(WIN_Y/20))
                #print(effectiveX + 1, effectiveY + 1)
                #Place ships
                if P1Placing and placedShips < numShipsPerPlayer:
                    if effectiveY >= 10 and effectiveX < 10:
                        if gridW.grid[effectiveY][effectiveX] != "Ship":
                            validShip = True
                            for i in range(lenShip):
                                if ((effectiveY + dirVec[1] * i >= 20) or (effectiveY + dirVec[1] * i <= 10) or (effectiveX + dirVec[0] * i >= 10) or (effectiveX + dirVec[0] * i <= 0) or (gridW.grid[effectiveY + dirVec[1] * i][effectiveX + dirVec[0] * i] != "Open")):
                                    validShip = False
                            if validShip:
                                for i in range(lenShip):
                                    gridW.grid[effectiveY + dirVec[1] * i][effectiveX + dirVec[0] * i] = "Ship"
                                lenShip += 1
                                placedShips += 1
                                if placedShips == numShipsPerPlayer:
                                    #pg.time.wait(1000)
                                    dirVec[0] = 0
                                    dirVec[1] = 1
                                    P1Placing = False
                                    P2Placing = True
                            else:
                                print("Invalid Ship!")
                elif P2Placing:
                    if effectiveY >= 10 and effectiveX >= 10:
                        if gridW.grid[effectiveY][effectiveX] != "Ship":
                            validShip = True
                            for i in range(lenShip - numShipsPerPlayer):
                                if ((effectiveY + dirVec[1] * i >= 20) or (effectiveY + dirVec[1] * i <= 10) or (effectiveX + dirVec[0] * i <= 10) or (effectiveX + dirVec[0] * i >= 20) or (gridW.grid[effectiveY + dirVec[1] * i][effectiveX + dirVec[0] * i] != "Open")):
                                    validShip = False
                            if validShip:
                                for i in range(lenShip - numShipsPerPlayer):
                                    gridW.grid[effectiveY + dirVec[1] * i][effectiveX + dirVec[0] * i] = "Ship"
                                lenShip += 1
                                placedShips += 1
                            else:
                                print("Invalid Ship!")
                    if placedShips >= numShipsPerPlayer * 2:
                        #pg.time.wait(1000)
                        P2Placing = False
                #else:
                    #Shoot for ships
        draw(P1Placing, P2Placing)
        clock.tick(120)

if __name__ == "__main__":
    main()