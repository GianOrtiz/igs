from .object import Object, ObjectType
from .utils import transform
from enum import Enum

class LineClippingAlgorithm:
    LIANG_BARSKY = 1
    COHEN_SUTHERLAND = 2

class Line(Object):
    def __init__(self, start_point, end_point, color='#000000', clipping_algorithm =LineClippingAlgorithm.LIANG_BARSKY):
        super().__init__(ObjectType.LINE, color)
        self.__start_point = start_point
        self.__end_point = end_point
        self.__clipping_algorithm = clipping_algorithm
    
    def clipping_algorithm(self) -> LineClippingAlgorithm:
        return self.__clipping_algorithm

    def points(self):
        return [
            self.__start_point,
            self.__end_point
        ]
    
    def set_points(self, points):
        self.__start_point = points[0]
        self.__end_point = points[1]
    
    def start_point(self):
        return self.__start_point
    
    def end_point(self):
        return self.__end_point

    def to_string(self):
        return 'Line - ' + self.id()

    def draw(self, draw_line, transform_coordinate, draw_path):
        start_point = transform_coordinate(self.__start_point)
        end_point = transform_coordinate(self.__end_point)
        draw_line((start_point[0], start_point[1], end_point[0], end_point[1], self.color()))

    def center(self):
        # Same things as a sum of all points divided by the number of points.
        return ((self.__start_point[0] + self.__end_point[0])/2, (self.__start_point[1] + self.__end_point[1])/2)

    def object_from_transformation(self, transformations):
        points = self.points()
        transformed_points = []
        for point in points:
            transformed_point = transform(point, transformations)
            transformed_points.append(transformed_point)
        
        obj = Line((0, 0), (0, 0), self.color())
        obj.set_points(transformed_points)
        return obj
