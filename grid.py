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

    def __winner__ (self,x):
        p1_count = 0
        p2_count = 0
        win_count = x
        for i in range(1,10):
            for j in range(1,10):
                if self.grid[j][i]=="hit":
                    p1_count += 1
        for p in range(11,20):
            for q in range(0,10):
                if self.grid[q][p]=="hit":
                    p2_count += 1
        
        if p1_count==5 or p1_count==4 or p1_count==2:
            p1_count=0

        if p1_count==3:
            p1_count=2
        if p1_count==6:
            p1_count=3
        if p1_count==10:
            p1_count=4
        if p1_count==15:
            p1_count=5  
            
        if p2_count==5 or p2_count==4 or p2_count==2:
            p2_count=0
        if p2_count==3:
            p2_count=2
        if p2_count==6:
            p2_count=3
        if p2_count==10:
            p2_count=4
        if p2_count==15:
            p2_count=5

        if p1_count == win_count:
            print("\n=====================\nPlayer 1 wins!\n=====================\n")
            return True
        
        if p2_count == win_count:
            print("\n=====================\nPlayer 2 wins!\n=====================\n")
            return True