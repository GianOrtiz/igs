from .object import Object, ObjectType

class Line(Object):
    def __init__(self, start_point, end_point):
        super().__init__(ObjectType.LINE)
        self.__start_point = start_point
        self.__end_point = end_point
    
    def points(self):
        return [
            self.__start_point,
            self.__end_point
        ]
    
    def start_point(self):
        return self.__start_point
    
    def end_point(self):
        return self.__end_point
