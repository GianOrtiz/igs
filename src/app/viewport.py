from .graphic.object import ObjectType

class Viewport:
    def __init__(self, window, x_max, x_min, y_max, y_min):
        self.__x_max = x_max
        self.__x_min = x_min
        self.__y_max = y_max
        self.__y_min = y_min
        self.__window = window

    def x_max(self):
        return self.__x_max
    
    def y_max(self):
        return self.__y_max
    
    def display_file(self):
        return self.__window.display_file()
    
    def window(self):
        return self.__window

    def lines_to_draw(self):
        for obj in self.__window.display_file().objects():
            if obj.type() == ObjectType.POINT:
                points = obj.points()
                transformed_coordinates = self.transform_coordinates(points)
                return [transformed_coordinates[0][0], transformed_coordinates[0][1], transformed_coordinates[0][0], transformed_coordinates[0][1]]
            elif obj.type() == ObjectType.LINE:
                points = obj.points()
                transformed_coordinates = self.transform_coordinates(points)
                return [transformed_coordinates[0][0], transformed_coordinates[0][1], transformed_coordinates[1][0], transformed_coordinates[1][1]]
            elif obj.type() == ObjectType.WIREFRAME:
                lines = []
                points = obj.points()
                transformed_coordinates = self.transform_coordinates(points)
                prev_point = None
                for point in transformed_coordinates:
                    if prev_point is None:
                        prev_point = point
                    lines.append([prev_point[0], prev_point[1], point[0], point[1]])
                    prev_point = point
                return lines
        return []

    def transform_coordinates(self, coordinates):
        transformed_coordinates = []
        for coordinate in coordinates:
            transformed_coordinates.append(self.transform_coordinate(coordinate))
        return transformed_coordinates

    def transform_coordinate(self, coordinate):
        x = ((coordinate[0] - self.__window.x_min())/(self.__window.x_max() - self.__window.x_min())) * (self.__x_max - self.__x_min)
        y = (1 - ((coordinate[1] - self.__window.y_min())/(self.__window.y_max() - self.__window.y_min()))) * (self.__y_max - self.__y_min)
        return (x, y)
