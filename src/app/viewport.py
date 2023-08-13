class Viewport:
    def __init__(self, window, x_max, x_min, y_max, y_min):
        self.__x_max = x_max
        self.__x_min = x_min
        self.__y_max = y_max
        self.__y_min = y_min
        self.__window = window
    
    def transform_coordinates(self, coordinates):
        transformed_coordinates = []
        for coordinate in coordinates:
            transformed_coordinates.insert(self.transform_coordinate(coordinate))
        return transformed_coordinates

    def transform_coordinate(self, coordinate):
        x = ((coordinate[0] - self.__window.x_min())/(self.__window.x_max() - self.__window.x_min())) * (self.__x_max - self.__x_min)
        y = (1 - ((coordinate[1] - self.__window.y_min())/(self.__window.y_max() - self.__window.y_min()))) * (self.__y_max - self.__y_min)
        return (x, y)
