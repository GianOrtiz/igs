from .object import Object, ObjectType
from .utils import transform
from PyQt5.QtGui import QPainterPath, QColor

class Wireframe(Object):
    def __init__(self, points, color='#000000', filled=False):
        super().__init__(ObjectType.WIREFRAME, color)
        if filled and len(points) > 0:
            if points[0] != points[-1]:
                points.append(points[0])
            self.__points = points
        else:
            self.__points = points

        self.__filled = filled

    def points(self):
        return self.__points
    
    def set_points(self, points):
        self.__points = points

    def to_string(self):
        return 'Wireframe - ' + self.id()

    def draw(self, draw_line, transform_coordinate, draw_path):
        if self.__filled:
            path = QPainterPath()
            prev_point = None
            for p in self.__points:
                if prev_point is None:
                    prev_point = transform_coordinate(p)
                    path.moveTo(prev_point[0], prev_point[1])
                point = transform_coordinate(p)
                path.lineTo(point[0], point[1])
                prev_point = point
            path.closeSubpath()
            fill_color = (path, QColor(self.color()))
            draw_path(path)
        else:
            prev_point = None
            for p in self.__points:
                if prev_point is None:
                    prev_point = transform_coordinate(p)
                point = transform_coordinate(p)
                draw_line((prev_point[0], prev_point[1], point[0], point[1], self.color()))
                prev_point = point

    def center(self):
        center_x = sum(list(map(lambda pos: pos[0], self.__points)))/len(self.__points)
        center_y = sum(list(map(lambda pos: pos[1], self.__points)))/len(self.__points)
        return (center_x, center_y)

    def object_from_transformation(self, transformations):
        points = self.points()
        transformed_points = []
        for point in points:
            transformed_point = transform(point, transformations)
            transformed_points.append(transformed_point)
        
        obj = Wireframe([], self.color(), self.__filled)
        obj.set_points(transformed_points)
        return obj
