class Coordinate():
    def __init__(self, x, y):
        self.setCoordinates(x, y)

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y

    def getSurroundingCoordinates(self):
        return [
            Coordinate(self.x-1, self.y),
            Coordinate(self.x+1, self.y),
            Coordinate(self.x, self.y-1),
            Coordinate(self.x, self.y+1)
        ]
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def get2DMatrixEquivalent(self):
        return (self.y, self.x)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x + other.x, self.y + other.y)
        raise TypeError("unsupported operand.")
    
    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return (self.x == other.x) and (self.y == other.y)
        raise TypeError("unsupported operand.")