import math

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def __add__(self, other):
        result = [[0 for _ in range(len(self.matrix[0]))] for _ in range(len(self.matrix))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                result[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return Matrix(result)
    
    def __sub__(self, other):
        result = [[0 for _ in range(len(self.matrix[0]))] for _ in range(len(self.matrix))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                result[i][j] = self.matrix[i][j] - other.matrix[i][j]
        return Matrix(result)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Matrix([[elem * other for elem in row] for row in self.matrix])
        
        result = [[0 for _ in range(len(other.matrix[0]))] for _ in range(len(self.matrix))]
        
        
        for i in range(len(self.matrix)):
            for j in range(len(other.matrix[0])):
                to_write = 0
                for k in range(len(other.matrix)):
                    to_write += self.matrix[i][k] * other.matrix[k][j]
                result[i][j] = to_write
        
        return Matrix(result)

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

class Vector:
    def __init__(self, vector):
        self.vector = vector

    def matrix_to_vector(self, matrix : Matrix):
        if len(matrix.matrix) == 1:
            return Vector(matrix.matrix[0])
        else:
            raise ValueError("Matrix is not a vector.")
    
    def normalize(self):
        length = math.sqrt(sum([x ** 2 for x in self.vector]))
        if length == 0:
            return self.vector
        return [x / length for x in self.vector]
    
    def cross(self, other):
        if len(self.vector) != 3 or len(other.vector) != 3:
            raise ValueError("Cross product is only defined for 3-dimensional vectors.")
        a1, a2, a3 = self.vector
        b1, b2, b3 = other.vector
        return Vector([
            a2 * b3 - a3 * b2,
            a3 * b1 - a1 * b3,
            a1 * b2 - a2 * b1
        ])

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.vector, other.vector)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.vector, other.vector)])

    def __mul__(self, scalar):
        if isinstance(scalar, Vector):
            ans = 0
            for i in range(len(self.vector)):
                ans += self.vector[i] * scalar.vector[i]
            return ans
        
        return Vector([a * scalar for a in self.vector])

    def __str__(self):
        return str(self.vector)

def translate(pos):
    tx, ty, tz = pos
    return Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])

def rotate_x(a):
    return Matrix([
        [1, 0, 0, 0],
        [0, math.cos(a), math.sin(a), 0],
        [0, -math.sin(a), math.cos(a), 0],
        [0, 0, 0, 1]
    ])

def rotate_y(a):
    return Matrix([
        [math.cos(a), 0, -math.sin(a), 0],
        [0, 1, 0, 0],
        [math.sin(a), 0, math.cos(a), 0],
        [0, 0, 0, 1]
    ])

def rotate_z(a):
    return Matrix([
        [math.cos(a), math.sin(a), 0, 0],
        [-math.sin(a), math.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def scale(n):
    return Matrix([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n, 0],
        [0, 0, 0, 1]
    ])