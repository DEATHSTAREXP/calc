from django.shortcuts import render
from django.http import JsonResponse
import json
import math

#
# C# to Python Matrix Logic
#
def create_matrix(rows, cols, data):
    """Creates a matrix from a flat list of data."""
    matrix = [[0.0] * cols for _ in range(rows)]
    k = 0
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = float(data[k])
            k += 1
    return matrix

def get_minor(matrix, row, col):
    """Returns the minor matrix after removing a specified row and column."""
    n = len(matrix)
    minor = [[0.0] * (n - 1) for _ in range(n - 1)]
    minor_row = 0
    for i in range(n):
        if i == row:
            continue
        minor_col = 0
        for j in range(n):
            if j == col:
                continue
            minor[minor_row][minor_col] = matrix[i][j]
            minor_col += 1
        minor_row += 1
    return minor

def determinant(matrix):
    """Calculates the determinant of a square matrix."""
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])

    det = 0.0
    for j in range(n):
        minor = get_minor(matrix, 0, j)
        cofactor = ((-1) ** (0 + j)) * determinant(minor)
        det += matrix[0][j] * cofactor
    return det

def transpose(matrix):
    """Transposes a matrix."""
    rows = len(matrix)
    cols = len(matrix[0])
    transposed_matrix = [[0.0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            transposed_matrix[j][i] = matrix[i][j]
    return transposed_matrix

def cofactor_matrix(matrix):
    """Calculates the matrix of cofactors."""
    n = len(matrix)
    cofactor_mat = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = get_minor(matrix, i, j)
            cofactor_mat[i][j] = ((-1) ** (i + j)) * determinant(minor)
    return cofactor_mat

def inverse(matrix):
    """Calculates the inverse of a square matrix."""
    n = len(matrix)
    if n != len(matrix[0]):
        return None, "Матрица должна быть квадратной для вычисления обратной."

    det = determinant(matrix)
    if det == 0:
        return None, "Определитель матрицы равен нулю, обратной матрицы не существует."

    adjugate_matrix = transpose(cofactor_matrix(matrix))
    
    inversed_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            inversed_matrix[i][j] = adjugate_matrix[i][j] / det
            
    return inversed_matrix, None

#
# The main Django View function
#
def matrix_calculator(request):
    """Handles matrix operations based on POST requests."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            operation = data.get('operation')
            
            # Extract matrix data and dimensions
            matrix_a_data = data.get('matrixA')
            matrix_a_rows = data.get('rowsA')
            matrix_a_cols = data.get('colsA')
            matrix_a = create_matrix(matrix_a_rows, matrix_a_cols, matrix_a_data)

            result = None
            error = None

            if operation == 'add':
                matrix_b_data = data.get('matrixB')
                matrix_b_rows = data.get('rowsB')
                matrix_b_cols = data.get('colsB')
                if matrix_a_rows != matrix_b_rows or matrix_a_cols != matrix_b_cols:
                    error = "Матрицы должны иметь одинаковые размеры для сложения."
                else:
                    matrix_b = create_matrix(matrix_b_rows, matrix_b_cols, matrix_b_data)
                    result = [[matrix_a[i][j] + matrix_b[i][j] for j in range(matrix_a_cols)] for i in range(matrix_a_rows)]

            elif operation == 'subtract':
                matrix_b_data = data.get('matrixB')
                matrix_b_rows = data.get('rowsB')
                matrix_b_cols = data.get('colsB')
                if matrix_a_rows != matrix_b_rows or matrix_a_cols != matrix_b_cols:
                    error = "Матрицы должны иметь одинаковые размеры для вычитания."
                else:
                    matrix_b = create_matrix(matrix_b_rows, matrix_b_cols, matrix_b_data)
                    result = [[matrix_a[i][j] - matrix_b[i][j] for j in range(matrix_a_cols)] for i in range(matrix_a_rows)]

            elif operation == 'multiply':
                matrix_b_data = data.get('matrixB')
                matrix_b_rows = data.get('rowsB')
                matrix_b_cols = data.get('colsB')
                if matrix_a_cols != matrix_b_rows:
                    error = "Количество столбцов первой матрицы должно совпадать с количеством строк второй."
                else:
                    matrix_b = create_matrix(matrix_b_rows, matrix_b_cols, matrix_b_data)
                    result = [[sum(matrix_a[i][k] * matrix_b[k][j] for k in range(matrix_a_cols)) for j in range(matrix_b_cols)] for i in range(matrix_a_rows)]
            
            elif operation == 'inverse':
                result, error = inverse(matrix_a)

            elif operation == 'scalar_multiply':
                scalar = data.get('scalarN')
                result = [[matrix_a[i][j] * float(scalar) for j in range(matrix_a_cols)] for i in range(matrix_a_rows)]

            elif operation == 'transpose':
                result = transpose(matrix_a)

            response_data = {
                'result': result,
                'error': error
            }

            return JsonResponse(response_data)
        
        except (ValueError, TypeError) as e:
            return JsonResponse({'error': f'Неверный ввод: {e}'}, status=400)
    

    return render(request, 'main/index.html')


