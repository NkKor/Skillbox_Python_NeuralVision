from sympy import symbols, Eq, solve, sqrt, sin, cos, Matrix, pi
import numpy as np

# Решение первой системы
x, y = symbols('x y', real=True, positive=True)
eq1 = Eq(sqrt(x) - 4*y - 2*sqrt(x) + 3*y, 1)
eq2 = Eq(7*sqrt(x) + 3*y - 5*x + 22*y, 13)
sol1 = solve([eq1, eq2], (x, y))
print("Solution for System 1:", sol1)

# Решение второй системы
x, y = symbols('x y', real=True)
eq1 = Eq(x**4 - y**4, 15)
eq2 = Eq(x**3 * y - x * y**3, 6)
sol2 = solve([eq1, eq2], (x, y))
print("Solution for System 2:", sol2)

# Решение третьей системы
x, y, z = symbols('x y z', real=True)
eq1 = Eq(x + y + z, 2)
eq2 = Eq(x**2 + y**2 + z**2, 6)
eq3 = Eq(x**3 + y**3 + z**3, 8)
sol3 = solve([eq1, eq2, eq3], (x, y, z))
print("Solution for System 3:", sol3)

# Решение четвертой системы
x, y, z = symbols('x y z', real=True, positive=True)
eq1 = Eq(x/y + y/z + z/x, 3)
eq2 = Eq(y/x + z/y + x/z, 3)
eq3 = Eq(x + y + z, 3)
sol4 = solve([eq1, eq2, eq3], (x, y, z))
print("Solution for System 4:", sol4)

# Проверка равенства двух матриц трансформации
alpha, Tx, Ty, Tz = symbols('alpha Tx Ty Tz')
T1 = Matrix([
    [cos(alpha), -sin(alpha), 0, Tx],
    [sin(alpha), cos(alpha), 0, Ty],
    [0, 0, 1, Tz],
    [0, 0, 0, 1]
])
T2 = Matrix([
    [cos(alpha), -sin(alpha), 0, Tx],
    [sin(alpha), cos(alpha), 0, Ty],
    [0, 0, 1, Tz],
    [0, 0, 0, 1]
])
print("Are T1 and T2 equal?", T1 == T2)

# Построение результирующей матрицы трансформации
# Смещение и вращения
Tx, Ty, Tz = 10, 10, 1
alpha_x, alpha_y, alpha_z = 30 * pi / 180, -45 * pi / 180, 0

# Матрицы вращения вокруг осей
Rx = Matrix([
    [1, 0, 0, 0],
    [0, cos(alpha_x), -sin(alpha_x), 0],
    [0, sin(alpha_x), cos(alpha_x), 0],
    [0, 0, 0, 1]
])
Ry = Matrix([
    [cos(alpha_y), 0, sin(alpha_y), 0],
    [0, 1, 0, 0],
    [-sin(alpha_y), 0, cos(alpha_y), 0],
    [0, 0, 0, 1]
])
Rz = Matrix([
    [cos(alpha_z), -sin(alpha_z), 0, 0],
    [sin(alpha_z), cos(alpha_z), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

# Матрица переноса
T = Matrix([
    [1, 0, 0, Tx],
    [0, 1, 0, Ty],
    [0, 0, 1, Tz],
    [0, 0, 0, 1]
])

# Результирующая матрица трансформации
Transformation_Matrix = T * Rz * Ry * Rx
print("Символьная матрица трансформации:")
print(Transformation_Matrix)

# Преобразование в NumPy-матрицу
Transformation_Matrix_np = np.array(Transformation_Matrix).astype(np.float64)
print("NumPy матрица трансформации:")
print(Transformation_Matrix_np)
