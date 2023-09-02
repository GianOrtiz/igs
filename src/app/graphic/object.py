from abc import ABC, abstractmethod
from enum import Enum
from .utils import transform

import uuid
import math

class ObjectType(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3

class Object(ABC):
    def __init__(self, type, color):
        self.__type = type
        self.__id = uuid.uuid4().hex
        self.__color = color

    def type(self):
        return self.__type
    
    def id(self):
        return self.__id

    def color(self):
        return self.__color

    @abstractmethod
    def to_string(self):
        pass

    @abstractmethod
    def draw(self, draw_line, transform_coordinate):
        pass

    @abstractmethod
    def center(self):
        pass

    @abstractmethod
    def points(self):
        pass

    @abstractmethod
    def set_points(self, points):
        pass

    def translate(self, position):
        translate_matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [position[0], position[1], 1]
        ]

        points = self.points()
        transformed_points = []
        for point in points:
            transformed_point = transform(point, [translate_matrix])
            transformed_points.append(transformed_point)
        
        self.set_points(transformed_points)

    def rotate_center(self, angle_in_radians):
        points = self.points()
        transformed_points = []
        object_center = self.center()
        sin_angle = math.sin(angle_in_radians)
        cos_angle = math.cos(angle_in_radians)
        rotate_matrix = [
            [cos_angle, -1 * sin_angle, 0],
            [sin_angle, cos_angle, 0],
            [0, 0, 1]
        ]

        for point in points:
            dx = object_center[0]
            dy = object_center[1]
            translate_to_center_matrix = [
                [1, 0, 0],
                [0, 1, 0],
                [-1 * dx, -1 * dy, 1],
            ]
            translate_to_point_matrix = [
                [1, 0, 0],
                [0, 1, 0],
                [dx, dy, 1],
            ]
            transformed_point = transform(point, [
                translate_to_center_matrix,
                rotate_matrix,
                translate_to_point_matrix,
            ])
            transformed_points.append(transformed_point)
        
        self.set_points(transformed_points)

    def rotate_world_center(self, angle_in_radians):
        sin_angle = math.sin(angle_in_radians)
        cos_angle = math.cos(angle_in_radians)
        # Create the rotation matrix.
        rotate_matrix = [
            [cos_angle, -1 * sin_angle, 0],
            [sin_angle, cos_angle, 0],
            [0, 0, 1]
        ]
        
        points = self.points()
        transformed_points = []
        for point in points:
            # As the default rotation is from the center of the world we do not need to translate the object.
            transformed_point = transform(point, [rotate_matrix])
            transformed_points.append(transformed_point)
        
        self.set_points(transformed_points)
    
    @abstractmethod
    def object_from_transformation(self, transformations):
        pass
    
    def rotate_point(self, point, angle_in_radians):
        points = self.points()
        transformed_points = []
        sin_angle = math.sin(angle_in_radians)
        cos_angle = math.cos(angle_in_radians)
        # Create the rotation matrix.
        rotate_matrix = [
            [cos_angle, -1 * sin_angle, 0],
            [sin_angle, cos_angle, 0],
            [0, 0, 1]
        ]

        for obj_point in points:
            # Create translation matrices from the given point.
            dx = point[0]
            dy = point[1]
            translate_to_center_matrix = [
                [1, 0, 0],
                [0, 1, 0],
                [-1 * dx, -1 * dy, 1],
            ]
            translate_to_point_matrix = [
                [1, 0, 0],
                [0, 1, 0],
                [dx, dy, 1],
            ]
            transformed_point = transform(point, [
                translate_to_center_matrix,
                rotate_matrix,
                translate_to_point_matrix,
            ])
            transformed_points.append(transformed_point)
        
        self.set_points(transformed_points)
    
    def scale(self, scales):
        object_center = self.center()

        translate_to_world_center_matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [-1 * object_center[0], -1 * object_center[1], 1]
        ]
        translate_to_object_center_matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [object_center[0], object_center[1], 1]
        ]
        scale_matrix = [
            [scales[0], 0, 0],
            [0, scales[1], 0],
            [0, 0, 1]
        ]

        points = self.points()
        transformed_points = []
        for point in points:
            transformed_point = transform(
                point,
                [
                    translate_to_world_center_matrix,
                    scale_matrix,
                    translate_to_object_center_matrix])
            transformed_points.append(transformed_point)
        
        self.set_points(transformed_points)
