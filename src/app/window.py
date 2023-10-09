import math
from typing import Tuple
from .graphic.object import Object, ObjectType
from .display_file import DisplayFile
from .graphic.line import Line, LineClippingAlgorithm
from .graphic.curve import BSplineForwardDifferencesCurve
from .graphic.wireframe import Wireframe

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
                if obj.clipping_algorithm() == LineClippingAlgorithm.LIANG_BARSKY:
                    self.liang_barsky(obj)
                else:
                    self.cohen_sutherland(obj)
            elif obj.type() == ObjectType.POINT:
                points = obj.points()
                x, y = points[0]
                if x <= 1 and x >= -1 and y <= 1 and y >= -1:
                    obj.set_show(True)
                else:
                    obj.set_show(False)
            elif obj.type() == ObjectType.WIREFRAME:
                self.weiler_atherton(obj)
            elif obj.type() == ObjectType.CURVE:
                self.clip_curve(obj)
        
    def clip_curve(self, curve):
        clipped_points = []
        curve_points = curve.points()
        for point in curve_points:
            x, y = point
            if x <= 1 and x >= -1 and y <= 1 and y >= -1:
                clipped_points.append(point)
        curve.set_points(clipped_points)

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

        p1 = -(x2 - x1)
        p2 = -p1
        p3 = -(y2 - y1)
        p4 = -p3

        q1 = x1 - (-1)
        q2 = 1 - x1
        q3 = y1 - (-1)
        q4 = 1 - y1

        t1 = 0
        t2 = 1

        for p, q in [(p1, q1), (p2, q2), (p3, q3), (p4, q4)]:
            if p == 0 and q < 0:
                # Line is parallel to window borders and outside.
                return

            if p != 0:
                t = q / p
                if p < 0:
                    t1 = max(t1, t)
                else:
                    t2 = min(t2, t)

        if t1 > t2:
            # Line is completely outside of the window
            return

        clipped_x1 = x1 + p2 * t1
        clipped_y1 = y1 + p4 * t1
        clipped_x2 = x1 + p2 * t2
        clipped_y2 = y1 + p4 * t2

        line.set_points([(clipped_x1, clipped_y1), (clipped_x2, clipped_y2)])

    def weiler_atherton(self, wireframe: Wireframe):
        points = wireframe.points()
        lines: list[Line] = []
        prev_point = None
        points_with_intersections = []
        window_lines: list[Line] = [
            Line((-1,-1), (1,-1)),
            Line((1,-1), (1,1)),
            Line((1,1), (-1,1)),
            Line((-1,1), (-1,-1))
        ]
        for point in points:
            if prev_point is not None:
                line = Line(prev_point, point)
                for window_line in window_lines:
                    intersection_point = line_intersection(line, window_line)
                    if intersection_point is not None:
                        if is_between(prev_point, point, intersection_point) and \
                            is_between(window_line.start_point(), window_line.end_point(), intersection_point):
                            points_with_intersections.append(intersection_point)
                            break
                points_with_intersections.append(point)
            else:
                points_with_intersections.append(point)
            prev_point = point

        prev_point = points_with_intersections[0]
        point = points_with_intersections[1]
        i = 1
        wireframe_clipped_points = []
        searching_for_reentering_point = False
        searched_all_points = False
        window_bounded_points = [
            (-1, 1),
            (1, 1),
            (1, -1),
            (-1, -1)
        ]
        while True:
            if searched_all_points:
                break

            prev_point = points_with_intersections[i-1]
            point = points_with_intersections[i]
            
            prev_x, prev_y = prev_point
            x, y = point

            if point == points_with_intersections[0]:
                if x >= -1 and x <=1 and y >= -1 and y <= 1:
                    wireframe_clipped_points.append(point)
                break

            if prev_x < -1 or prev_x > 1 or prev_y < -1 or prev_y > 1:
                # Previous point is from outside window bounds.
                if x >= -1 and x <=1 and y >= -1 and y <= 1:
                    # Add this point to the clipped points.
                    wireframe_clipped_points.append(point)
            elif x < -1 or x > 1 or y < -1 or y > 1:
                curr_x, curr_y = prev_x, prev_y

                # Advance points until it reenters window and join the window borders.
                while x < -1 or x > 1 or y < -1 or y > 1:
                    i += 1
                    prev_point = points_with_intersections[i-1]
                    if i == len(points_with_intersections):
                        i = i % len(points_with_intersections)
                        searched_all_points = True
                    point = points_with_intersections[i]
                    x, y = point
                
                if curr_x == 1 and x == 1:
                    if curr_y > y:
                        if curr_y != -1:
                            wireframe_clipped_points.append((1, -1))
                        wireframe_clipped_points.append((-1, -1))
                        wireframe_clipped_points.append((-1, 1))
                        wireframe_clipped_points.append((1, 1))
                elif curr_x == -1 and x == -1:
                    if curr_y < y:
                        if curr_y != 1:
                            wireframe_clipped_points.append((-1, 1))
                        wireframe_clipped_points.append((1, 1))
                        wireframe_clipped_points.append((1, -1))
                        wireframe_clipped_points.append((-1, -1))
                elif curr_y == 1 and y == 1:
                    if curr_x > x:
                        if curr_x != 1:
                            wireframe_clipped_points.append((1, 1))
                        wireframe_clipped_points.append((1, -1))
                        wireframe_clipped_points.append((-1, -1))
                        wireframe_clipped_points.append((-1, 1))
                elif curr_y == -1 and y == -1:
                    if curr_x < x:
                        if curr_x != -1:
                            wireframe_clipped_points.append((-1, -1))
                        wireframe_clipped_points.append((-1, 1))
                        wireframe_clipped_points.append((1, 1))
                        wireframe_clipped_points.append((1, -1))
                else:
                    j = -1
                    while j != len(window_bounded_points)-1:
                        j += 1
                        next_point = window_bounded_points[j]
                        if (curr_x == 1 and x == 1) or (curr_x == -1 and x == -1) or (curr_y == 1 and y == 1) or (curr_y == -1 and y == -1):
                            break
                        wireframe_clipped_points.append(next_point)
                        curr_x, curr_y = next_point
                if point not in wireframe_clipped_points:
                    wireframe_clipped_points.append(point)
            else:
                wireframe_clipped_points.append(point)
                        
            i += 1

        wireframe.set_points(wireframe_clipped_points)

def line_intersection(line1: Line, line2: Line):
    xdiff = (line1.start_point()[0] - line1.end_point()[0], line2.start_point()[0] - line2.end_point()[0])
    ydiff = (line1.start_point()[1] - line1.end_point()[1], line2.start_point()[1] - line2.end_point()[1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*[line1.start_point(), line1.end_point()]), det(*[line2.start_point(), line2.end_point()]))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return (x, y)

def is_between(a, b, c):
    crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])

    if abs(crossproduct) > 1e-6:
        return False

    dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
    if dotproduct < 0:
        return False

    squaredlengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
    if dotproduct > squaredlengthba:
        return False

    return True