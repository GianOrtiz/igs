import os

from .object import Object
from .line import Line
from .point import Point
from .wireframe import Wireframe

class DescriptorOBJ:
    @staticmethod
    def export_to_OBJ(obj: Object) -> str:
        parse_str = ''
        points_str = 'f '
        i = 1

        points = obj.points()
        for point in points:
            parse_str += 'v {0} {1} 0.0\n'.format(point[0], point[1])
            points_str += str(i) + ' '
            i += 1
        
        points_str += '\n'
        comment = '# ' + obj.to_string() + '\n'
        return comment + parse_str + points_str

    @staticmethod
    def parse(file: str) -> list[Object]:
        objs = []
        points = []
        with open(file) as f:
            for line in f:
                if line[0] == 'v':
                    coordinates_partials = line.split(' ')[1:]
                    points.append((float(coordinates_partials[0]), float(coordinates_partials[1])))
                if line[0] == 'f':
                    number_of_points = int(line.split(' ')[-1])
                    obj_points = points[:number_of_points]
                    if number_of_points == 1:
                        objs.append(Point(obj_points[0][0], obj_points[0][1]))
                    elif number_of_points == 2:
                        objs.append(Line(obj_points[0], obj_points[1]))
                    else:
                        objs.append(Wireframe(obj_points))
                    obj_points = []
