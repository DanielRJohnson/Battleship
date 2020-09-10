import constants as c
class gridWrapper:
    def __init__(self):
        self.grid = []
        for row in range(c.NUM_ROWS):
            self.grid.append([])
            for column in range (c.NUM_ROWS):
                self.grid[row].append("Open")
    def __shoot__(self,y,x):
        if x >= 1 and x <= 9:
            if self.grid[y-10][x+10] == "Ship":
                self.grid[y][x] = "hit"
                #print("hit ship")            
            else:
                self.grid[y][x] = "miss"
                #print("You Missed")

        
        elif x >= 10 and y <= 20:
            if self.grid[y-10][x-10] == "Ship":
                self.grid[y][x] = "hit"
                #print("hit ship")
            else:
                self.grid[y][x] = "miss"
                #print("You Missed")

    #def checkWinner(self)