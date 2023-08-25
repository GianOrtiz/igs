import numpy as np

def transform(point, transform_matrices):
    transform_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for matrix in transform_matrices:
        transform_matrix = np.matmul(transform_matrix, matrix)
    
    transformed_point = np.matmul([point[0], point[1], 0], transform_matrix)
    return (transformed_point[0], transformed_point[1])
    