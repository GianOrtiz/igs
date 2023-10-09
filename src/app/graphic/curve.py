import numpy as np
from .object import Object, ObjectType
from .utils import transform

BEZIER_MATRIX = [
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 3, 0, 0],
    [1, 0, 0, 0]
]

BSPLINE_MATRIX = [
    [-1/6, 3/6, -3/6, 1/6],
    [3/6, -6/6, 3/6, 0],
    [-3/6, 0, 3/6, 0],
    [1/6, 4/6, 1/6, 0]
]

delta = 0.001

class BezierCurve(Object):
    def __init__(self, points: list[tuple[float, float]], color: str ='#000000'):
        super().__init__(ObjectType.CURVE, color)

        transformed_points: list[tuple[float, float]] = []
        if len(points) == 4:
            t = 0
            step = 0.1
            while t <= 1:
                next_point = self.calculate_next_value(points, t)
                transformed_points.append(next_point)
                t += step
            
            self.set_points(transformed_points)
        else:
            self.__points = []

    def to_string(self):
        return 'Curve - ' + self.id()
    
    def draw(self, draw_line, transform_coordinate, draw_path):
        prev_point = None
        for p in self.__points:
            if prev_point is None:
                prev_point = transform_coordinate(p)
            point = transform_coordinate(p)
            draw_line((prev_point[0], prev_point[1], point[0], point[1], self.color()))
            prev_point = point

    def center(self):
        pass

    def points(self):
        return self.__points
    
    def set_points(self, points: list[tuple[float, float]]):
        self.__points = points

    def object_from_transformation(self, transformations):
        points = self.points()
        transformed_points = []
        for point in points:
            transformed_point = transform(point, transformations)
            transformed_points.append(transformed_point)
        
        obj = BezierCurve([], self.color())
        obj.set_points(transformed_points)
        return obj

    def calculate_next_value(self, values: list[tuple[float, float]], t: int) -> float:
        def bezier(coordinates: list[float]):
            coord_1, coord_2, coord_3, coord_4 = coordinates
            val = (
                coord_1*(-1*(t**3) + (3*t**2) - (3*t) + 1) + \
                    coord_2*((3*t**3) - (6*t**2) + (3*t)) + \
                        coord_3*(-3*(t**3) + (3*t**2)) + \
                            coord_4*(t**3))
            return val

        xs = []
        ys = []
        for c in values:
            xs.append(c[0])
            ys.append(c[1])
        xt = bezier(xs)
        yt = bezier(ys)
        return (xt, yt)

class BSplineForwardDifferencesCurve(Object):
    def __init__(self, points: list[tuple[float, float]], color: str ='#000000'):
        super().__init__(ObjectType.CURVE, color)

        transformed_points: list[tuple[float, float]] = []

        self.__points = self.__calculate_points(points)

    def to_string(self):
        return 'Curve - ' + self.id()
    
    def draw(self, draw_line, transform_coordinate, draw_path):
        prev_point = None
        for p in self.__points:
            if prev_point is None:
                prev_point = transform_coordinate(p)
            point = transform_coordinate(p)
            draw_line((prev_point[0], prev_point[1], point[0], point[1], self.color()))
            prev_point = point

    def center(self):
        pass

    def points(self):
        return self.__points
    
    def set_points(self, points: list[tuple[float, float]]):
        self.__points = points

    def object_from_transformation(self, transformations):
        points = self.points()
        transformed_points = []
        for point in points:
            transformed_point = transform(point, transformations)
            transformed_points.append(transformed_point)
        
        obj = BSplineForwardDifferencesCurve([], self.color())
        obj.set_points(transformed_points)
        return obj

    def __calculate_points(self, points: list[tuple[float, float]]):
        points_to_draw = []

        for i in range(len(points) - 3):
            point_1, point_2, point_3, point_4 = points[i:i+4]
            gbs_x = [point_1[0], point_2[0], point_3[0], point_4[0]]
            gbs_y = [point_1[1], point_2[1], point_3[1], point_4[1]]
            a_x, b_x, c_x, d_x = np.matmul(BSPLINE_MATRIX, gbs_x)
            f_x = d_x
            delta_f_x = (a_x * (delta**3)) + (b_x * (delta**2)) + (c_x * delta)
            delta_f_2_x = (6 * a_x * (delta**3)) + (2 * b_x * (delta**2))
            delta_f_3_x = (6 * a_x * (delta**3))
            a_y, b_y, c_y, d_y = np.matmul(BSPLINE_MATRIX, gbs_y)
            f_y = d_y
            delta_f_y = (a_y * (delta**3)) + (b_y * (delta**2)) + (c_y * delta)
            delta_f_2_y = (6 * a_y * (delta**3)) + (2 * b_y * (delta**2))
            delta_f_3_y = (6 * a_y * (delta**3))

            points_to_draw += calculate_forward_diffences(f_x, f_y, 10, delta_f_x, delta_f_2_x, delta_f_3_x, delta_f_y, delta_f_2_y, delta_f_3_y)
    
        return points_to_draw

def calculate_forward_diffences(x, y, n, delta_x,delta_2_x,delta_3_x,delta_y,delta_2_y,delta_3_y) -> list[tuple[float, float]]:
    points_to_draw = []

    i = 0
    old_x, old_y = None, None
    old_x = x
    old_y = y
    points_to_draw.append((old_x, old_y))
    while i < n:
        i += 1
        x = x + delta_x
        delta_x = delta_x + delta_2_x
        delta_2_x = delta_2_x + delta_3_x
        y = y + delta_y
        delta_y = delta_y + delta_2_y
        delta_2_y = delta_2_y + delta_3_y
        points_to_draw.append((x, y))
        old_x = x
        old_y = y

    return points_to_draw
