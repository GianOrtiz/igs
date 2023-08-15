from .object import Object, ObjectType

class Point(Object):
    def __init__(self, x, y):
        super().__init__(ObjectType.POINT)
        self.__x = x
        self.__y = y
    
    def points():
        return [(x, y)]

    def x(self):
        return self.__x
    
    def y(self):
        return self.__y
