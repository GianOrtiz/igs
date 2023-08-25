from .object import Object, ObjectType

class Wireframe(Object):
    def __init__(self, points):
        super().__init__(ObjectType.WIREFRAME)
        self.__points = points

    def points(self):
        return self.__points
    
    def set_points(self, points):
        self.__points = points

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

    def center(self):
        center_x = sum(list(map(lambda pos: pos[0], self.__points)))/len(self.__points)
        center_y = sum(list(map(lambda pos: pos[1], self.__points)))/len(self.__points)
        return (center_x, center_y)
