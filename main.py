import pygame as pg
import sys
import math
from grid import gridWrapper
pg.init()
pg.display.set_caption("Battleship")
clock=pg.time.Clock()
#Screen_Dsiplay_units
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

def draw():
    screen.blit(bg, (0,0))
    for i in range(20):
        for j in range(20):
            pg.draw.line(screen, BLACK, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, WIN_Y), 1)
        pg.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIN_X, i * SQUARE_SIZE), 1)
    for i in range(len(gridW.grid)):
        for j in range(len(gridW.grid[0])):
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
    pg.display.update()

def main():
    placing = True
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
                print(effectiveX + 1, effectiveY + 1)
                #Place ships
                if placing and placedShips < 5:
                    if effectiveY >= 10 and effectiveX < 10:
                        if gridW.grid[effectiveY][effectiveX] != "Ship":
                            validShip = True
                            for i in range(lenShip):
                                if ((effectiveY + dirVec[1] * i >= 20) or (effectiveY + dirVec[1] * i < 10) or (effectiveX + dirVec[0] * i >= 10) or (effectiveX + dirVec[0] * i < 0) or (gridW.grid[effectiveY + dirVec[1] * i][effectiveX + dirVec[0] * i] != "Open")):
                                    validShip = False
                            if validShip:
                                for i in range(lenShip):
                                    gridW.grid[effectiveY + dirVec[1] * i][effectiveX + dirVec[0] * i] = "Ship"
                                lenShip += 1
                                placedShips += 1
                            else:
                                print("Invalid Ship!")
                elif placing:
                    if effectiveY >= 10 and effectiveX >= 10:
                        if gridW.grid[effectiveY][effectiveX] != "Ship":
                            validShip = True
                            for i in range(lenShip - 5):
                                if ((effectiveY + dirVec[1] * i >= 20) or (effectiveY + dirVec[1] * i < 10) or (effectiveX + dirVec[0] * i < 10) or (effectiveX + dirVec[0] * i >= 20) or (gridW.grid[effectiveY + dirVec[1] * i][effectiveX + dirVec[0] * i] != "Open")):
                                    validShip = False
                            if validShip:
                                for i in range(lenShip - 5):
                                    gridW.grid[effectiveY + dirVec[1] * i][effectiveX + dirVec[0] * i] = "Ship"
                                lenShip += 1
                                placedShips += 1
                            else:
                                print("Invalid Ship!")
                    if placedShips == 10:
                        placing = False
                #else:
                    #Shoot for ships
        draw()
        clock.tick(120)

if __name__ == "__main__":
    main()