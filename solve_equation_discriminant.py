import cmath


def solve_equation_discriminant(a: float, b: float, c: float) -> tuple[complex, complex] | float:
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
       tuple[complex, complex] or float
           Returns a tuple containing two roots when the discriminant is non-zero. If the
           discriminant is zero, returns a single real root as a float.
       """
    # Вычисляем дискриминант
    D = b ** 2 - 4 * a * c
    if D != 0:
        # Используем cmath для вычисления комплексных корней
        x1 = (-b + cmath.sqrt(D)) / (2 * a)
        x2 = (-b - cmath.sqrt(D)) / (2 * a)
        return x1, x2
    else:
        x = -b / (2 * a)  # Один корень
        return x


def check_root(a: float, b: float, c: float, roots: tuple | float) -> bool:
    r"""Checks whether the found roots satisfy the quadratic equation.

    This function evaluates the quadratic equation for each root and checks
    if it is close to zero within a specified tolerance.

    Parameters
    ----------
    a : float
        The coefficient of \( x^2 \) in the quadratic equation.
    b : float
        The coefficient of \( x \) in the quadratic equation.
    c : float
        The constant term in the quadratic equation.
    roots : tuple or float
        A tuple containing the roots of the equation to be checked.
        A float if there is only one root.

    Returns
    -------
    bool
        Returns `True` if all roots satisfy the equation within the specified
        tolerance; otherwise, returns `False`.
    """
    tolerance = 1e-10  # Допустимая погрешность
    if isinstance(roots, float):  # Проверяем, является ли корень float
        roots = (roots,)  # Преобразуем в кортеж
    for x in roots:
        if x is None:
            continue
        if abs(a * x ** 2 + b * x + c) >= tolerance:
            return False
    return True


try:
    a = float(input("Введите коэффициент a: "))
    b = float(input("Введите коэффициент b: "))
    c = float(input("Введите коэффициент c: "))
except ValueError:
    print("Ошибка: необходимо вводить числовые значения.")
else:
    if a == 0:
        print("Коэффициент 'a' не может быть равен нулю, так как это перестает быть квадратным уравнением.")
    else:
        result = solve_equation_discriminant(a, b, c)
        print(f"Решение уравнения: {result}")
if check_root(a, b, c, result):
    print("Корни прошли проверку и являются корректными.")
else:
    print("Ошибка: найденные корни не удовлетворяют исходному уравнению.")
