

import numpy as np


matrix_list = []

m1 = np.array([[1, 1, 1],
               [2, 2, 2],
               [3, 3, 3]])

m2 = np.array([[1, 2, 3],
               [4, 5, 6],
               [7, 8, 9]])
m3 = np.array([[1, 2, 3],
               [4, 5, 6],
               [7, 8, 9]])

matrix_list.append(m1)
matrix_list.append(m2)
matrix_list.append(m3)

weights = np.array([1, 1, 1])


avg_matrix = np.average(matrix_list, axis=0, weights=weights)

print(avg_matrix)
