from object import Object, ObjectType

class Wireframe(Object):
    def __init__(self, points):
        super().__init__(ObjectType.WIREFRAME)
        self.__points = points

    def points(self):
        return self.__points
