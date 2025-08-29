class Coordinate():
    def __init__(self, x, y):
        self.setCoordinates(x, y)

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y

    def getCoordinatesInProximity(self):
        return [
            Coordinate(self.x, self.y),
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
    
    def distance(self, other):
        self.typeCheck(other)
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def typeCheck(self, other):
        if not isinstance(other, Coordinate):
            raise TypeError("unsupported operand.")
        
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        self.typeCheck(other)
        return Coordinate(self.x + other.x, self.y + other.y)
    
    # def __iadd__(self, other):
    #     self.typeCheck(other)
    #     self.x += other.x
    #     self.y += other.y
    #     return self
        
    def __sub__(self, other):
        self.typeCheck(other)
        return Coordinate(self.x - other.x, self.y - other.y)
        
    def __eq__(self, other):
        self.typeCheck(other)
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y))
