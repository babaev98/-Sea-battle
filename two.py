class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinates = [x, y]

    def __eq__(self, other):
        if not isinstance(other, (list, Dot)):
            raise TypeError('Не верные координаты')
        sc = other if isinstance(other, list) else other.coordinates
        return self.coordinates == sc

    def __str__(self):
        return f"Dot({self.x},{self.y})"


class Board:
    def __init__(self):
        self.field = [[Dot(x, y), 'O'] for x in range(6) for y in range(6)]
        self.list_ship = [3, 2, 2, 1, 1, 1, 1]
        self.hid = bool
        self.living_ships = 0

    def getField(self):
        for i in range(6):
            result = self.field[i * 6: (i * 6) + 6]
            for x in result:
                print(x[1])



asd = Board()
print(asd.getField())