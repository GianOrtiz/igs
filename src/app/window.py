ZOOM_FACTOR = 0.5
MOVE_FACTOR = 5

class Window:
    def __init__(self, x_max, x_min, y_max, y_min, display_file):
        self.__x_max = x_max
        self.__x_min = x_min
        self.__y_max = y_max
        self.__y_min = y_min
        self.__display_file = display_file
    
    def x_max(self):
        return self.__x_max
    
    def x_min(self):
        return self.__x_min

    def y_max(self):
        return self.__y_max
    
    def y_min(self):
        return self.__y_min
    
    def display_file(self):
        return self.__display_file

    def zoom_out(self):
        self.__x_max = self.__x_max * (1 + ZOOM_FACTOR)
        self.__x_min = self.__x_min * (1 + ZOOM_FACTOR)
        self.__y_max = self.__y_max * (1 + ZOOM_FACTOR)
        self.__y_min = self.__y_min * (1 + ZOOM_FACTOR)
    
    def zoom_in(self):
        self.__x_max = self.__x_max * (1 - ZOOM_FACTOR)
        self.__x_min = self.__x_min * (1 - ZOOM_FACTOR)
        self.__y_max = self.__y_max * (1 - ZOOM_FACTOR)
        self.__y_min = self.__y_min * (1 - ZOOM_FACTOR)

    def move_left(self):
        self.__x_max = self.__x_max + MOVE_FACTOR
        self.__x_min = self.__x_min - MOVE_FACTOR
    
    def move_right(self):
        self.__x_max = self.__x_max - MOVE_FACTOR
        self.__x_min = self.__x_min + MOVE_FACTOR
    
    def move_bottom(self):
        self.__y_max = self.__y_max + MOVE_FACTOR
        self.__y_min = self.__y_min - MOVE_FACTOR
    
    def move_top(self):
        self.__y_max = self.__y_max - MOVE_FACTOR
        self.__y_min = self.__y_min + MOVE_FACTOR
