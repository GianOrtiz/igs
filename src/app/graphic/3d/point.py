import math

class Point3D:
    def __init__(self, x: float, y: float, z: float, color='#000000'):
        self.x = x
        self.y = y
        self.z = z

    def translate(self, translation: tuple[float]):
        tx, ty, tz = translation
        translate_matrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [tx, ty, tz, 1]
        ]
        self.x, self.y, self.z = transform_3d([self.x, self.y, self.z], translate_matrix)

    def scale(self, scale: tuple[float]):
        sx, sy, sz = scale
        translate_to_center_matrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-1 * self.x, -1 * self.y, -1 * self.z, 1],
        ]
        translate_from_center_matrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [self.x, self.y, self.z, 1],
        ]
        scale_matrix = [
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ]
        self.x, self.y, self.z = transform_3d([self.x, self.y, self.z], [translate_to_center_matrix, scale_matrix, translate_from_center_matrix])

    def rotate_x(self, theta: float):
        rotation_x = [
            [1, 0, 0, 0],
            [0, math.cos(theta), math.sin(theta), 0],
            [0, -1 * math.sin(theta), math.cos(theta), 0],
            [0, 0, 0, 1]
        ]
        self.x, self.y, self.z = transform_3d([self.x, self.y, self.z], [rotation_x])

    def rotate_y(self, theta: float):
        rotation_y = [
            [math.cos(theta), 0, -1 * math.sin(theta), 0],
            [0, 1, 0, 0],
            [math.sin(theta), 0, math.cos(theta), 0],
            [0, 0, 0, 1]
        ]
        self.x, self.y, self.z = transform_3d([self.x, self.y, self.z], [rotation_y])

    def rotate_z(self, theta: float):
        rotation_z = [
            [math.cos(theta), math.sin(theta), 0, 0],
            [-1 * math.sin(theta), math.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        self.x, self.y, self.z = transform_3d([self.x, self.y, self.z], [rotation_z])

    def rotate_from_axis(self, theta: float, point: Point3D):
        # Translate the point to the center of world.
        translate_to_center_matrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-1 * point.x, -1 * point.y, -1 * point.z, 1]
        ]

        # Rotate the points by thetaX to align to the xy axis.
        theta_x = math.atan2(self.y, self.z)
        rotation_x = [
            [1, 0, 0, 0],
            [0, math.cos(theta_x), math.sin(theta_x), 0],
            [0, -1 * math.sin(theta_x), math.cos(theta_x), 0],
            [0, 0, 0, 1]
        ]

        new_x, new_y, new_z = transform_3d([self.x, self.y, self.z], [translate_to_center_matrix, rotation_x])

        # Rotate the points by thetaZ to align to the y axis.
        theta_z = math.atan2(self.x, new_y)
        rotation_z = [
            [math.cos(theta_z), math.sin(theta_z), 0, 0],
            [-1 * math.sin(theta_z), math.cos(theta_z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        # Rotate the points over Y axis by the given theta.
        rotation_y = [
            [math.cos(theta), 0, -1 * math.sin(theta), 0],
            [0, 1, 0, 0],
            [math.sin(theta), 0, math.cos(theta), 0],
            [0, 0, 0, 1]
        ]

        # Rotate the points by -thetaZ to undo the rotation to thetaZ
        inverse_rotation_z = [
            [math.cos(-1 * theta_z), math.sin(-1 * theta_z), 0, 0],
            [-1 * math.sin(-1 * theta_z), math.cos(-1 * theta_z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        # Rotate the points by -thetaX to undo the rotation to thetaX
        inverse_rotation_x = [
            [1, 0, 0, 0],
            [0, math.cos(-1 * theta_x), math.sin(-1 * theta_x), 0],
            [0, -1 * math.sin(-1 * theta_x), math.cos(-1 * theta_x), 0],
            [0, 0, 0, 1]
        ]

        # Translate back to the point where it was translated initially.
        translate_to_center_matrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [point.x, point.y, point.z, 1]
        ]

        self.x, self.y, self.z = transform_3d([new_x, new_y, new_z], [
            rotation_z,
            rotation_y,
            inverse_rotation_z,
            inverse_rotation_x,
            translate_to_center_matrix
        ])