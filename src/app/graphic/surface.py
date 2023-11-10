from .object3d import Object3D, Segment
from .point3d import Point3D
from .object import ObjectType

import numpy as np

BEZIER_MATRIX = [
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 3, 0, 0],
    [1, 0, 0, 0]
]

delta = 0.25

class BezierSurface(Object3D):
    def __init__(self, lines, color='#000000'):
        g = [
            lines[0],
            lines[1],
            lines[2],
            lines[3],
        ]
        segments = self.calculate_segments(g)
        super().__init__(segments, ObjectType.WIREFRAME, color)

    def to_string(self):
        return 'Bezier Surface - ' + self.id
    
    def calculate_segments(self, g):
        # Calculates the following:
        # x(s, t) = S * M * Gx * Mt * Tt
        # y(s, t) = S * M * Gy * Mt * Tt
        # z(s, t) = S * M * Gz * Mt * Tt
        gx = [
            [g[0][0][0], g[0][1][0], g[0][2][0], g[0][3][0]],
            [g[1][0][0], g[1][1][0], g[1][2][0], g[1][3][0]],
            [g[2][0][0], g[2][1][0], g[2][2][0], g[2][3][0]],
            [g[3][0][0], g[3][1][0], g[3][2][0], g[3][3][0]]
        ]
        gy = [
            [g[0][0][1], g[0][1][1], g[0][2][1], g[0][3][1]],
            [g[1][0][1], g[1][1][1], g[1][2][1], g[1][3][1]],
            [g[2][0][1], g[2][1][1], g[2][2][1], g[2][3][1]],
            [g[3][0][1], g[3][1][1], g[3][2][1], g[3][3][1]]
        ]
        gz = [
            [g[0][0][2], g[0][1][2], g[0][2][2], g[0][3][2]],
            [g[1][0][2], g[1][1][2], g[1][2][2], g[1][3][2]],
            [g[2][0][2], g[2][1][2], g[2][2][2], g[2][3][2]],
            [g[3][0][2], g[3][1][2], g[3][2][2], g[3][3][2]]
        ]
        gs = [gx, gy, gz]

        segments = []
        s = 0
        while s < 1:
            matrix_s = [s**3, s**2, s, 1]
            t = 0
            previous_point = None
            while t < 1:
                matrix_t = [[t**3], [t**2], [t], [1]]
                
                axis = []
                for g in gs:
                    multiplication_matrices = [
                        matrix_s,
                        BEZIER_MATRIX,
                        g,
                        BEZIER_MATRIX,
                        matrix_t
                    ]
                    identity = [
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                    ]
                    res = identity
                    for matrix in multiplication_matrices:
                        res = np.matmul(res, matrix)
                    axis.append(res[0])                

                x, y, z = axis
                point = Point3D(x, y, z)
                if previous_point is None:
                    previous_point = point
                else:
                    segment = Segment(previous_point, point)
                    segments.append(segment)
                
                t += delta
            s += delta

        t = 0
        while t < 1:
            matrix_t = [[t**3], [t**2], [t], [1]]
            s = 0
            previous_point = None
            while s < 1:
                matrix_s = [s**3, s**2, s, 1]
                
                axis = []
                for g in gs:
                    multiplication_matrices = [
                        matrix_s,
                        BEZIER_MATRIX,
                        g,
                        BEZIER_MATRIX,
                        matrix_t
                    ]
                    identity = [
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                    ]
                    res = identity
                    for matrix in multiplication_matrices:
                        res = np.matmul(res, matrix)
                    axis.append(res[0])                

                x, y, z = axis
                point = Point3D(x, y, z)
                if previous_point is None:
                    previous_point = point
                else:
                    segment = Segment(previous_point, point)
                    segments.append(segment)
                
                s += delta
            t += delta
        
        return segments
