from .object import Object, ObjectType
from .utils import transform

BEZIER_MATRIX = [
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 3, 0, 0],
    [1, 0, 0, 0]
]

class Curve(Object):
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
        
        obj = Curve([], self.color())
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
