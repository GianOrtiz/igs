from .graphic.object import ObjectType
from .display_file import DisplayFile
from .window import Window

class Viewport:
    def __init__(self, window, x_max, x_min, y_max, y_min):
        self.__x_max = x_max
        self.__x_min = x_min
        self.__y_max = y_max
        self.__y_min = y_min
        self.__window = window

    def x_max(self) -> float:
        return self.__x_max
    
    def y_max(self) -> float:
        return self.__y_max
    
    def display_file(self) -> DisplayFile:
        return self.__window.display_file()
    
    def window(self) -> Window:
        return self.__window

    def draw(self, draw_line, draw_path):
        # Draw the limit of the viewport.
        draw_line((10, 10, 10, self.__y_max - 20, '#FF0000'))
        draw_line((10, self.__y_max - 20, self.__x_max - 20, self.__y_max - 20, '#FF0000'))
        draw_line((self.__x_max - 20, self.__y_max - 20, self.__x_max - 20, 10, '#FF0000'))
        draw_line((self.__x_max - 20, 10, 10, 10, '#FF0000'))
        
        for obj in self.__window.normalized_display_file().objects():
            if obj.show():
                obj.draw(draw_line, self.transform_coordinate, draw_path)

    def transform_coordinates(self, coordinates: list[tuple[float, float]]) -> list[tuple[float, float]]:
        transformed_coordinates = []
        for coordinate in coordinates:
            transformed_coordinates.append(self.transform_coordinate(coordinate))
        return transformed_coordinates

    def transform_coordinate(self, coordinate: tuple[float, float]) -> tuple[float, float]:
        x = ((coordinate[0] - (-1))/(1 - (-1))) * ((self.__x_max - 10) - (self.__x_min + 10)) + 10
        if coordinate[1] > 0:
            y = (1 - ((coordinate[1] - (-1))/(1 - (-1)))) * ((self.__y_max + 10) - (self.__y_min + 10)) + 10
        else:
            y = (1 - ((coordinate[1] - (-1))/(1 - (-1)))) * ((self.__y_max + 10) - (self.__y_min + 10)) - 20
        return (x, y)
