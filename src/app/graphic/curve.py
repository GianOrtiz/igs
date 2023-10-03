from .wireframe import Wireframe

BEZIER_MATRIX = [
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 3, 0, 0],
    [1, 0, 0, 0]
]

DEFAULT_ITERATIONS = 10

class Curve(Wireframe):
    def __init__(self, points: list[tuple[float, float]], color: str ='#000000'):
        super().__init__(points, color, filled=False)

        transformed_points: list[tuple[float, float]] = []
        for i in range(DEFAULT_ITERATIONS):
            next_point = self.calculate_next_value(points, i)
            transformed_points.append(next_point)
        
        self.set_points(transformed_points)

    def calculate_next_value(self, values: list[tuple[float, float]], t: int) -> float:
        def transformation(coordinates: list[float]):
            coord_1, coord_2, coord_3, coord_4 = coordinates
            return (
                coord_1*((-1*t**3) + (3*t**2) - (3*t) + 1) + \
                    coord_2*((3*t**3) - (6*t**2) - (3*t)) + \
                        coord_3*((-3*t**3) + (3*t**2)) + \
                            coord_4*(t**3))    

        xs = []
        ys = []
        for c in values:
            xs.append(c[0])
            ys.append(c[1])
        return (transformation(xs), transformation(ys))
