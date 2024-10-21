import math

import scipy
from math import sqrt
# put your python code here
def discriminant(a, b, c):
    # Вычисляем дискриминант
    D = b ** 2 - 4 * a * c
    # Проверяем, что дискриминант неотрицательный
    if D < 0:
        print(f"Корней нет, дискриминант меньше нуля: {D}")
    elif D == 0:
        # Один корень
        x = -b / (2 * a)
        print(f"Один корень: x = {x}")
    else:
        # Два корня
        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)
        print(f"Два корня: x1 = {x1}, x2 = {x2}")

a = int(input('Введите коэффициент а: '))
b = int(input('Введите коэффициент b: '))
c = int(input('Введите коэффициент c: '))
result = discriminant(a, b, c)
print(result)
