import math
from typing import Tuple
from .graphic.object import Object, ObjectType
from .display_file import DisplayFile
from .graphic.line import Line

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
        self.generate_normalized_display_file()
    
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
        self.clip()

    def zoom_out(self):
        self.__x_max = self.__x_max + ZOOM_FACTOR
        self.__x_min = self.__x_min - ZOOM_FACTOR
        self.__y_max = self.__y_max + ZOOM_FACTOR
        self.__y_min = self.__y_min - ZOOM_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.generate_normalized_display_file()
        self.clip()
    
    def zoom_in(self):
        self.__x_max = self.__x_max - ZOOM_FACTOR
        self.__x_min = self.__x_min + ZOOM_FACTOR
        self.__y_max = self.__y_max - ZOOM_FACTOR
        self.__y_min = self.__y_min + ZOOM_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.generate_normalized_display_file()
        self.clip()

    def move_left(self):
        y_move_factor = MOVE_FACTOR * math.sin(self.__rotation)
        x_move_factor = MOVE_FACTOR * math.cos(self.__rotation)
        self.__x_max -= x_move_factor
        self.__x_min -= x_move_factor
        self.__window_center_x -= x_move_factor
        self.__y_max -= y_move_factor
        self.__y_min -= y_move_factor
        self.__window_center_y -= y_move_factor
        self.__normalized_display_file = DisplayFile()
        self.generate_normalized_display_file()
        self.clip()
    
    def move_right(self):
        y_move_factor = MOVE_FACTOR * math.sin(self.__rotation)
        x_move_factor = MOVE_FACTOR * math.cos(self.__rotation)
        self.__x_max += x_move_factor
        self.__x_min += x_move_factor
        self.__window_center_x += x_move_factor
        self.__y_max += y_move_factor
        self.__y_min += y_move_factor
        self.__window_center_y += y_move_factor
        self.__normalized_display_file = DisplayFile()
        self.generate_normalized_display_file()
        self.clip()
    
    def move_bottom(self):
        x_move_factor = MOVE_FACTOR * math.sin(self.__rotation)
        y_move_factor = MOVE_FACTOR * math.cos(self.__rotation)
        self.__y_max = self.__y_max - y_move_factor
        self.__y_min = self.__y_min - y_move_factor
        self.__window_center_y = self.__window_center_y - y_move_factor
        self.__x_max = self.__x_max + x_move_factor
        self.__x_min = self.__x_min + x_move_factor
        self.__window_center_x = self.__window_center_x + x_move_factor
        self.__normalized_display_file = DisplayFile()
        self.generate_normalized_display_file()
        self.clip()
    
    def move_top(self):
        x_move_factor = MOVE_FACTOR * math.sin(self.__rotation)
        y_move_factor = MOVE_FACTOR * math.cos(self.__rotation)
        self.__y_max = self.__y_max + y_move_factor
        self.__y_min = self.__y_min + y_move_factor
        self.__window_center_y = self.__window_center_y + y_move_factor
        self.__x_max = self.__x_max - x_move_factor
        self.__x_min = self.__x_min - x_move_factor
        self.__window_center_x = self.__window_center_x - x_move_factor
        self.__normalized_display_file = DisplayFile()
        self.generate_normalized_display_file()
        self.clip()

    def rotate_left(self):
        self.__rotation = self.__rotation + ROTATION_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.generate_normalized_display_file()
        self.clip()

    def rotate_right(self):
        self.__rotation = self.__rotation - ROTATION_FACTOR
        self.__normalized_display_file = DisplayFile()
        self.generate_normalized_display_file()
        self.clip()

    def generate_normalized_display_file(self):
        self.__normalized_display_file = DisplayFile()
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
        normalized_x = 2/(self.__x_max - self.__x_min)
        normalized_y = 2/(self.__y_max - self.__y_min)
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
        radians = self.__rotation
        angle_sin = math.sin(radians)
        angle_cos = math.cos(radians)
        rotate_matrix = [
            [angle_cos, -1 * angle_sin, 0],
            [angle_sin, angle_cos, 0],
            [0, 0, 1],
        ]
        normalized_x = 2/(self.__x_max - self.__x_min)
        normalized_y = 2/(self.__y_max - self.__y_min)
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

    def clip(self):
        for obj in self.__normalized_display_file.objects():
            if obj.type() == ObjectType.LINE:
                self.liang_barsky(obj)
            elif obj.type() == ObjectType.POINT:
                points = obj.points()
                x, y = points[0]
                if x <= 1 and x >= -1 and y <= 1 and y >= -1:
                    obj.set_show(True)
                else:
                    obj.set_show(False)
            elif obj.type() == ObjectType.WIREFRAME:
                pass
        
    def cohen_sutherland(self, line: Line):
        points = line.points()

        def get_rc(point):
            rc = 0b0000
            x, y = point

            if x < -1:
                rc = rc | 0b0010
            else:
                rc = rc | 0b0000
            
            if x > 1:
                rc = rc | 0b1000
            else:
                rc = rc | 0b0000

            if y < -1:
                rc = rc | 0b0001
            else:
                rc = rc | 0b0000
            
            if y > 1:
                rc = rc | 0b0100
            else:
                rc = rc | 0b0000

            return rc

        start_point = points[0]
        end_point = points[1]

        start_rc = get_rc(start_point)
        end_rc = get_rc(end_point)

        while True:
            if start_rc == end_rc and start_rc == 0b0000:
                line.set_show(True)
                break
            if start_rc & end_rc != 0:
                line.set_show(False)
                break
            else:
                line.set_show(True)
                
                x1, y1 = start_point
                x2, y2 = end_point

                if start_rc > end_rc:
                    rc = start_rc
                else:
                    rc = end_rc

                if rc & 0b0100 != 0:
                    x = x1 + (x2 - x1) * (1 - y1) / (y2 - y1)
                    y = 1
                elif rc & 0b0001 != 0:
                    x = x1 + (x2 - x1) * (-1 - y1) / (y2 - y1)
                    y = -1
                elif rc & 0b1000 != 0:
                    y = y1 + (y2 - y1) * (1 - x1) / (x2 - x1)
                    x = 1
                elif rc & 0b0010 != 0:
                    y = y1 + (y2 - y1) * (-1 - x1) / (x2 - x1)
                    x = -1

                if rc == start_rc:
                    x1 = x
                    y1 = y
                else:
                    x2 = x
                    y2 = y

                start_point = (x1, y1)
                end_point = (x2, y2)
                start_rc = get_rc(start_point)
                end_rc = get_rc(end_point)
                line.set_points([(x1, y1), (x2, y2)])

    def liang_barsky(self, line: Line):
        points = line.points()
        x1, y1 = points[0]
        x2, y2 = points[1]

        p1 = -1 * (x2 - x1)
        p2 = -1 * p1
        p3 = -1 * (y2 - y1)
        p4 = -1 * p3


        q1 = x1 - (-1)
        q2 = 1 - x1
        q3 = y1 - (-1)
        q4 = 1 - y1

        negative_values = [0]
        positive_values = [1]

        if p1 != 0:
            r1 = q1/p1
            r2 = q2/p2
            if p1 < 0:
                negative_values.append(r1)
                positive_values.append(r2)
            else:
                negative_values.append(r2)
                positive_values.append(r1)

        if p3 != 0:
            r3 = q3/p3
            r4 = q4/p4
            if p3 < 0:
                negative_values.append(r3)
                positive_values.append(r4)
            else:
                negative_values.append(r4)
                positive_values.append(r3)
        
        u1 = max(negative_values)
        x1 = x1 + p2 * u1
        y1 = y1 + p4 * u1
        
        u2 = min(positive_values)
        x2 = x2 + p2 * u2
        y2 = y2 + p4 * u2
        
        line.set_points([(x1, y1), (x2, y2)])
