import os

from .object3d import Object3D
from .point3d import Point3D
from .line import Line
from .point import Point
from .wireframe import Wireframe

class DescriptorOBJ:
    @staticmethod
    def export_to_OBJ(obj: Object3D) -> str:
        parse_str = ''
        points_str = 'f '
        i = 1

        segments = obj.segments()
        for segment in segments:
            point_a, point_b = segment.a, segment.b
            parse_str += 'v {0} {1} {2}\n'.format(point_a.x, point_a.y, point_a.z)
            parse_str += 'v {0} {1} {2}\n'.format(point_b.x, point_b.y, point_b.z)
            points_str += str(i) + ' '
            i += 1
        
        points_str += '\n'
        comment = '# ' + obj.to_string() + '\n'
        return comment + parse_str + points_str

    @staticmethod
    def parse(file: str) -> list[Object3D]:
        objs = []
        points = []
        with open(file) as f:
            for line in f:
                if line[0] == 'v':
                    coordinates_partials = line.split(' ')[1:]
                    points.append(Point3D(float(coordinates_partials[0]),float(coordinates_partials[1]),float(coordinates_partials[2])))
                if line[0] == 'f':
                    number_of_points = int(line.split(' ')[-1])
                    obj_points = points[:number_of_points]
                    if number_of_points == 1:
                        objs.append(Object3D(Segment(obj_points[0], obj_points[0]), ObjectType.POINT))
                    elif number_of_points == 2:
                        objs.append(Object3D(Segment(obj_points[0], obj_points[1]), ObjectType.LINE))
                    else:
                        segments = []
                        previous_point = None
                        for point in obj_points:
                            if previous_point is None:
                                previous_point = point
                            else:
                                segments.append(Segment(previous_point, point))
                        objs.append(Object3D(segments, ObjectType.WIREFRAME))
                    obj_points = []
