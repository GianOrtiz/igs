import math
from .display_file import DisplayFile

ZOOM_FACTOR = 50
MOVE_FACTOR = 50

class Window:
    def __init__(self, x_max, x_min, y_max, y_min, display_file):
        self.__x_max = x_max
        self.__x_min = x_min
        self.__y_max = y_max
        self.__y_min = y_min
        window_center = self.__calculate_window_center()
        self.__window_center_x = window_center[0]
        self.__window_center_y = window_center[1]
        self.__display_file = display_file
        self.__normalized_display_file = DisplayFile()
        self.__generate_normalized_display_file()
    
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

    def add_object(self, obj):
        self.__display_file.add_object(obj)
        self.add_normalized_object(obj)

    def zoom_out(self):
        self.__x_max = self.__x_max + ZOOM_FACTOR
        self.__x_min = self.__x_min - ZOOM_FACTOR
        self.__y_max = self.__y_max + ZOOM_FACTOR
        self.__y_min = self.__y_min - ZOOM_FACTOR
    
    def zoom_in(self):
        self.__x_max = self.__x_max - ZOOM_FACTOR
        self.__x_min = self.__x_min + ZOOM_FACTOR
        self.__y_max = self.__y_max - ZOOM_FACTOR
        self.__y_min = self.__y_min + ZOOM_FACTOR

    def move_left(self):
        self.__x_max = self.__x_max - MOVE_FACTOR
        self.__x_min = self.__x_min + MOVE_FACTOR
    
    def move_right(self):
        self.__x_max = self.__x_max + MOVE_FACTOR
        self.__x_min = self.__x_min - MOVE_FACTOR
    
    def move_bottom(self):
        self.__y_max = self.__y_max - MOVE_FACTOR
        self.__y_min = self.__y_min + MOVE_FACTOR
    
    def move_top(self):
        self.__y_max = self.__y_max + MOVE_FACTOR
        self.__y_min = self.__y_min - MOVE_FACTOR

    def __generate_normalized_display_file(self):
        translate_to_center_matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [-1 * self.__window_center_x, -1 * self.__window_center_y, 1],
        ]
        radians = 0
        angle_sin = math.sin(radians)
        angle_cos = math.cos(radians)
        rotate_matrix = [
            [angle_cos, -1 * angle_sin, 0],
            [angle_sin, angle_cos, 0],
            [0, 0, 1],
        ]
        normalized_x = 1/self.__x_max
        normalized_y = 1/self.__y_max
        scale_to_normalized_matrix = [
            [normalized_x, 0, 0],
            [0, normalized_y, 0],
            [0, 0, 1]
        ]

        for obj in self.__display_file.objects():
            normalized_obj = obj.object_from_transformation([translate_to_center_matrix, rotate_matrix, scale_to_normalized_matrix])
            self.__normalized_display_file.add_object(normalized_obj)

    def add_normalized_object(self, obj):
        translate_to_center_matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [-1 * self.__window_center_x, -1 * self.__window_center_y, 1],
        ]
        radians = 0
        angle_sin = math.sin(radians)
        angle_cos = math.cos(radians)
        rotate_matrix = [
            [angle_cos, -1 * angle_sin, 0],
            [angle_sin, angle_cos, 0],
            [0, 0, 1],
        ]
        normalized_x = 1/self.__x_max
        normalized_y = 1/self.__y_max
        scale_to_normalized_matrix = [
            [normalized_x, 0, 0],
            [0, normalized_y, 0],
            [0, 0, 1]
        ]

        normalized_obj = obj.object_from_transformation([translate_to_center_matrix, rotate_matrix, scale_to_normalized_matrix])
        self.__normalized_display_file.add_object(normalized_obj)

    def __calculate_window_center(self):
        return ((self.__x_max - self.__x_min)/2, (self.__y_max - self.__y_min)/2)
