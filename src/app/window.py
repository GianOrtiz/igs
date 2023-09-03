import math
from typing import Tuple
from .graphic.object import Object
from .display_file import DisplayFile

ZOOM_FACTOR = 50
MOVE_FACTOR = 50
ROTATION_FACTOR = 0.1

class Window:
    def __init__(self, x_max, x_min, y_max, y_min, display_file):
        self.__x_max: float = x_max
        self.__x_min: float = x_min
        self.__y_max: float = y_max
        self.__y_min: float = y_min
        self.__rotation: int = 0
        window_center = self.__calculate_window_center()
        self.__window_center_x: float = window_center[0]
        self.__window_center_y: float = window_center[1]
        self.__display_file: DisplayFile = display_file
        self.__normalized_display_file: DisplayFile = DisplayFile()
        self.__generate_normalized_display_file()
    
    def x_max(self) -> float:
        return self.__x_max
    
    def x_min(self) -> float:
        return self.__x_min

    def y_max(self) -> float:
        return self.__y_max
    
    def y_min(self) -> float:
        return self.__y_min
    
    def normalized_display_file(self) -> DisplayFile:
        return self.__normalized_display_file

    def display_file(self) -> DisplayFile:
        return self.__display_file

    def add_object(self, obj: Object):
        self.__display_file.add_object(obj)
        self.add_normalized_object(obj)

    def zoom_out(self):
        self.__x_max = self.__x_max + ZOOM_FACTOR
        self.__x_min = self.__x_min - ZOOM_FACTOR
        self.__y_max = self.__y_max + ZOOM_FACTOR
        self.__y_min = self.__y_min - ZOOM_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.__generate_normalized_display_file()
    
    def zoom_in(self):
        self.__x_max = self.__x_max - ZOOM_FACTOR
        self.__x_min = self.__x_min + ZOOM_FACTOR
        self.__y_max = self.__y_max - ZOOM_FACTOR
        self.__y_min = self.__y_min + ZOOM_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.__generate_normalized_display_file()

    def move_left(self):
        self.__x_max = self.__x_max - MOVE_FACTOR
        self.__x_min = self.__x_min + MOVE_FACTOR
        self.__window_center_x = self.__window_center_x - MOVE_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.__generate_normalized_display_file()
    
    def move_right(self):
        self.__x_max = self.__x_max + MOVE_FACTOR
        self.__x_min = self.__x_min - MOVE_FACTOR
        self.__window_center_x = self.__window_center_x + MOVE_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.__generate_normalized_display_file()
    
    def move_bottom(self):
        self.__y_max = self.__y_max - MOVE_FACTOR
        self.__y_min = self.__y_min + MOVE_FACTOR
        self.__window_center_y = self.__window_center_y - MOVE_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.__generate_normalized_display_file()
    
    def move_top(self):
        self.__y_max = self.__y_max + MOVE_FACTOR
        self.__y_min = self.__y_min - MOVE_FACTOR
        self.__window_center_y = self.__window_center_y + MOVE_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.__generate_normalized_display_file()

    def rotate_left(self):
        self.__rotation = self.__rotation + ROTATION_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.__generate_normalized_display_file()

    def rotate_right(self):
        self.__rotation = self.__rotation - ROTATION_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.__generate_normalized_display_file()

    def __generate_normalized_display_file(self):
        translate_to_center_matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [-1 * self.__window_center_x, -1 * self.__window_center_y, 1],
        ]
        radians = self.__rotation
        angle_sin = math.sin(radians)
        angle_cos = math.cos(radians)
        rotate_matrix = [
            [angle_cos, -1 * angle_sin, 0],
            [angle_sin, angle_cos, 0],
            [0, 0, 1],
        ]
        normalized_x = 2/self.__x_max
        normalized_y = 2/self.__y_max
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
        normalized_x = 2/self.__x_max
        normalized_y = 2/self.__y_max
        scale_to_normalized_matrix = [
            [normalized_x, 0, 0],
            [0, normalized_y, 0],
            [0, 0, 1]
        ]

        normalized_obj = obj.object_from_transformation(
            [
                translate_to_center_matrix,
                rotate_matrix,
                scale_to_normalized_matrix,
            ]
        )
        self.__normalized_display_file.add_object(normalized_obj)

    def __calculate_window_center(self) -> Tuple[float]:
        return ((self.__x_max - self.__x_min)/2, (self.__y_max - self.__y_min)/2)
