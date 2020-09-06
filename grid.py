class gridWrapper:
    def __init__(self):
        self.grid = []
        for row in range(20):
            self.grid.append([])
            for column in range (20):
                self.grid[row].append("Open")
    #def shoot(x,y)