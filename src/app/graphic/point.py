from .object import Object, ObjectType
from .utils import transform

class Point(Object):
    def __init__(self, x, y, color='#000000'):
        super().__init__(ObjectType.POINT, color)
        self.__x = x
        self.__y = y
        self.__show = True
    
    def points(self):
        return [(self.__x, self.__y)]
    
    def set_points(self, points):
        self.__x = points[0][0]
        self.__y = points[0][1]

    def x(self):
        return self.__x
    
    def y(self):
        return self.__y

    def to_string(self):
        return 'Point - ' + self.id()

    def draw(self, draw_line, transform_coordinate, draw_path):
        # Draws more than one point so we can see the point in the screen. This is done for
        # educational purposes only.
        p1 = transform_coordinate((self.__x, self.__y))
        draw_line((p1[0], p1[1], p1[0], p1[1], self.color()))

    def center(self):
        return (self.__x, self.__y)

    def object_from_transformation(self, transformations):
        points = self.points()
        transformed_points = []
        for point in points:
            transformed_point = transform(point, transformations)
            transformed_points.append(transformed_point)
        
        obj = Point(0, 0, self.color())
        obj.set_points(transformed_points)
        return obj
