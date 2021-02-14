class Position():

    def __init__(self, x: int, y: int):
        super().__init__()
        self.__x = x
        self.__y = y

    def move(self, x: int, y: int):
        self.__x += x
        self.__y += y

    def __getx(self):
        return round(self.__x)

    def __setx(self, val):
        self.__x = val

    x = property(__getx, __setx)

    def __gety(self):
        return round(self.__y)

    def __sety(self, val):
        self.__y = val

    y = property(__gety, __sety)
