from .point3d import Point3D
from .utils import transform_3d

class Segment:
    def __init__(self, a: Point3D, b: Point3D):
        self.a = a
        self.b = b

class Object3D:
    def __init__(self, segments: list[Segment]):
        self.segments = segments

    def center(self) -> tuple[float]:
        sum_x = 0
        sum_y = 0
        sum_z = 0
        for segment in self.segments:
            sum_x += segment.a.x + segment.b.x
            sum_y += segment.a.y + segment.b.y
            sum_z += segment.a.z + segment.b.z

        len_points = len(self.segments)*2
        center_x = sum_x/len_points
        center_y = sum_y/len_points
        center_z = sum_z/len_points
        return (center_x, center_y, center_z)

    def scale(self, scale: list[float]):
        for segment in self.segments:
            segment.a.scale(scale)
            segment.b.scale(scale)

    def translate(self, translation: list[float]):
        for segment in self.segments:
            segment.a.translate(translation)
            segment.b.translate(translation)
    
    def rotate_from_axis(self, theta: float, point: Point3D):
        for segment in self.segments:
            segment.a.rotate_from_axis(point)
            segment.b.rotate_from_axis(point)

    def rotate_x(self, theta: float):
        for segment in self.segments:
            segment.a.rotate_x(theta)
            segment.b.rotate_x(theta)
    
    def rotate_y(self, theta: float):
        for segment in self.segments:
            segment.a.rotate_y(theta)
            segment.b.rotate_y(theta)

    def rotate_z(self, theta: float):
        for segment in self.segments:
            segment.a.rotate_z(theta)
            segment.b.rotate_z(theta)

    def from_transformations(self, transformations: list[list[float]]):
        segments: list[Segment] = []
        for s in self.segments:
            segment = Segment(s.a, s.b)
            segments.append(segment)
            segment.a.transform(transformations)
            segment.b.transform(transformations)
        return Object3D(segments)