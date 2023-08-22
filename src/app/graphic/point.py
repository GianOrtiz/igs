from .object import Object, ObjectType

class Point(Object):
    def __init__(self, x, y):
        super().__init__(ObjectType.POINT)
        self.__x = x
        self.__y = y
    
    def points(self):
        return [(x, y)]

    def x(self):
        return self.__x
    
    def y(self):
        return self.__y

    def to_string(self):
        return 'Point - ' + self.id()

    def draw(self, draw_line, transform_coordinate):
        # Draws more than one point so we can see the point in the screen. This is done for
        # educational purposes only.
        p1 = transform_coordinate((self.__x, self.__y))
        p2 = transform_coordinate((self.__x+1, self.__y))
        p3 = transform_coordinate((self.__x+1, self.__y+1))
        p4 = transform_coordinate((self.__x+2, self.__y+1))
        p5 = transform_coordinate((self.__x+2, self.__y))
        draw_line((p1[0], p1[1], p2[0], p2[1]))
        draw_line((p2[0], p2[1], p3[0], p3[1]))
        draw_line((p3[0], p3[1], p4[0], p4[1]))
        draw_line((p4[0], p4[1], p5[0], p5[1]))
        draw_line((p5[0], p5[1], p1[0], p1[1]))
