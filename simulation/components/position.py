class Position():

    def __init__(self, x: int, y: int):
        super().__init__()
        self.__x = x
        self.__y = y

    def move(self, x: int, y: int):
        self.__x += x
        self.__y += y

    def __get_x(self):
        return round(self.__x)

    def __set_x(self, val):
        self.__x = val

    x = property(__get_x, __set_x)

    def __get_y(self):
        return round(self.__y)

    def __set_y(self, val):
        self.__y = val

    y = property(__get_y, __set_y)
