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
steps = 10

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

class BezierForwardDifferencesSurface(Object3D):
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

        cx = np.matmul(BEZIER_MATRIX, gx)
        cx = np.matmul(cx, BEZIER_MATRIX)

        cy = np.matmul(BEZIER_MATRIX, gy)
        cy = np.matmul(cy, BEZIER_MATRIX)

        cz = np.matmul(BEZIER_MATRIX, gz)
        cz = np.matmul(cz, BEZIER_MATRIX)

        delta = 1 / (steps - 1)

        e_delta = np.array([
            [0, 0, 0, 1],
            [delta**3, delta**2, delta, 0],
            [6*(delta**3), 2*(delta**2), 0, 0,],
            [6*(delta**3), 0, 0, 0]
        ])

        ddx = np.matmul(e_delta, cx)
        ddx = np.matmul(ddx, e_delta.transpose())

        ddy = np.matmul(e_delta, cy)
        ddy = np.matmul(ddy, e_delta.transpose())

        ddz = np.matmul(e_delta, cz)
        ddz = np.matmul(ddz, e_delta.transpose())

        segments = []
        for i in range(steps):
            points = calculate_forward_diffences(ddx[0][0], ddy[0][0], ddz[0][0], steps, ddx[0][1], ddx[0][2], ddx[0][3], ddy[0][1], ddy[0][2], ddy[0][3], ddz[0][1], ddz[0][2], ddz[0][3])
            last_point = None
            for point in points:
                if last_point is not None:
                    segments.append(Segment(last_point, point))
                last_point = point
            
            for i in range(len(ddx)):
                if i == len(ddx)-1:
                    break

                for j in range(len(ddx[i])):
                    ddx[i][j] += ddx[i+1][j]
                    ddy[i][j] += ddy[i+1][j]
                    ddz[i][j] += ddz[i+1][j]

        ddx = np.matmul(e_delta, cx)
        ddx = np.matmul(ddx, e_delta.transpose())
        ddx = ddx.transpose()

        ddy = np.matmul(e_delta, cy)
        ddy = np.matmul(ddy, e_delta.transpose())
        ddy = ddy.transpose()

        ddz = np.matmul(e_delta, cz)
        ddz = np.matmul(ddz, e_delta.transpose())
        ddz = ddz.transpose()

        for i in range(steps):
            points = calculate_forward_diffences(ddx[0][0], ddy[0][0], ddz[0][0], steps, ddx[0][1], ddx[0][2], ddx[0][3], ddy[0][1], ddy[0][2], ddy[0][3], ddz[0][1], ddz[0][2], ddz[0][3])
            last_point = None
            for point in points:
                if last_point is not None:
                    segments.append(Segment(last_point, point))
                last_point = point
            
            for i in range(len(ddx)):
                if i == len(ddx)-1:
                    break

                for j in range(len(ddx[i])):
                    ddx[i][j] += ddx[i+1][j]
                    ddy[i][j] += ddy[i+1][j]
                    ddz[i][j] += ddz[i+1][j]

        return segments
    
def calculate_forward_diffences(x, y, z, n, delta_x,delta_2_x,delta_3_x,delta_y,delta_2_y,delta_3_y, delta_z,delta_2_z, delta_3_z) -> list[tuple[float, float]]:
    points_to_draw = []

    i = 0
    old_x, old_y, old_z = None, None, None
    old_x = x
    old_y = y
    old_z = z
    points_to_draw.append(Point3D(old_x, old_y, old_z))
    while i < n:
        i += 1
        x = old_x + delta_x
        delta_x = delta_x + delta_2_x
        delta_2_x = delta_2_x + delta_3_x
        y = old_y + delta_y
        delta_y = delta_y + delta_2_y
        delta_2_y = delta_2_y + delta_3_y
        z = old_z + delta_z
        delta_z = delta_z + delta_2_z
        delta_2_z = delta_2_z + delta_3_z
        points_to_draw.append(Point3D(x, y, z))
        old_x = x
        old_y = y
        old_z = z

    return points_to_draw

