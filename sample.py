from sympy import symbols, Matrix, sin, cos, exp, eye, factorial
import numpy as np

# Матрица A
A = Matrix([
    [5, 7, 4],
    [1, 2, 1],
    [3, 1, 4]
])

# Функции для разложения в ряды
def matrix_expansion(A, func, terms=10):
    result = eye(A.shape[0])  # Единичная матрица
    power = eye(A.shape[0])  # Для хранения A^n
    for n in range(1, terms):
        power = power * A  # A^n
        result += func(n) * power / factorial(n)
    return result

# Вычисление sin(A), cos(A), exp(A)
sin_A = matrix_expansion(A, lambda n: (-1)**(n // 2) if n % 2 == 1 else 0, terms=15)
cos_A = matrix_expansion(A, lambda n: (-1)**(n // 2) if n % 2 == 0 else 0, terms=15)
exp_A = matrix_expansion(A, lambda n: 1, terms=15)

# Вывод символических матриц
print("sin(A):")
print(sin_A)
print("cos(A):")
print(cos_A)
print("exp(A):")
print(exp_A)

# Преобразование в NumPy-матрицы
sin_A_np = np.array(sin_A).astype(np.float64)
cos_A_np = np.array(cos_A).astype(np.float64)
exp_A_np = np.array(exp_A).astype(np.float64)

print("NumPy sin(A):")
print(sin_A_np)
print("NumPy cos(A):")
print(cos_A_np)
print("NumPy exp(A):")
print(exp_A_np)
