import numpy as np
from numpy.polynomial import Polynomial


def solve_by_discriminant(a: float, b: float, c: float) -> tuple[np.complex128, np.complex128] | float:
    r"""Solve a quadratic equation and return its roots.

       This function calculates the roots of a quadratic equation given the coefficients
       of the equation. It handles real and complex roots using the discriminant.

       Parameters
       ----------
       a : float
           The coefficient of the x^2 term. Must be non-zero for a valid quadratic equation.
       b : float
           The coefficient of the x term.
       c : float
           The constant term in the equation.

       Returns
       -------
       tuple[np.complex128, np.complex128] or float
           Returns a tuple containing two roots when the discriminant is non-zero. If the
           discriminant is zero, returns a single real root as a float.

    """

    # Создаем полином и вычисляем корни
    p = Polynomial([c, b, a])
    decision = p.roots()

    # Проверяем, если два корня одинаковы, возвращаем только один корень
    if len(decision) == 2 and np.isclose(decision[0], decision[1]):
        return decision[0]  # Возвращаем только один корень

    return decision  # Возвращаем все корни


a, b, c = None, None, None

# Ввод коэффициентов
while True:
    try:
        a = float(input("Введите коэффициент а: "))
        if a == 0:
            print("Коэффициент 'a' не может быть равен нулю, так как уравнение перестает быть квадратным.")
            continue

        b = float(input("Введите коэффициент b: "))
        c = float(input("Введите коэффициент c: "))
        break  # Выход из цикла, если ввод корректен

    except ValueError:
        print("Ошибка: необходимо вводить числовые значения.")

result = solve_by_discriminant(a, b, c)
print(f"Решение уравнения: {result}")

# Проверка корней
tolerance = 1e-10  # Погрешность


# Преобразуем результат в список для удобства обработки
roots = [result] if isinstance(result, float) else result

for x in roots:
    if np.abs(a * x ** 2 + b * x + c) >= tolerance:
        print(f"Ошибка: корень {x} не удовлетворяет уравнению.")
    else:
        print(f'Корень {x} прошел проверку и является корректным с точностью до {tolerance}.')
