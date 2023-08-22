from .object import Object, ObjectType

class Wireframe(Object):
    def __init__(self, points):
        super().__init__(ObjectType.WIREFRAME)
        self.__points = points

    def points(self):
        return self.__points

    def to_string(self):
        return 'Wireframe - ' + self.id()

    def draw(self, draw_line, transform_coordinate):
        prev_point = None
        for p in self.__points:
            if prev_point is None:
                prev_point = transform_coordinate(p)
            point = transform_coordinate(p)
            draw_line((prev_point[0], prev_point[1], point[0], point[1]))
            prev_point = point
