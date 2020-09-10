class ShipNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit = False

class Ship:
    def __init__(self):
        self.shipSquares = []
        self.sunk = False
    def checkSunk(self):
        for square in self.shipSquares:
            if square.hit == False:
                return False
        self.sunk = True
        return True
    def addSquare(self, x, y):
        self.shipSquares.append(ShipNode(x,y))