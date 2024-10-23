import cmath


def discriminant(a: float, b: float, c: float) -> tuple[complex, complex] | float:
    D = b ** 2 - 4 * a * c  # Вычисляем дискриминант

    if D < 0:
        # Используем cmath для вычисления комплексных корней
        x1 = (-b + cmath.sqrt(D)) / (2 * a)
        x2 = (-b - cmath.sqrt(D)) / (2 * a)
        return x1, x2
    elif D == 0:
        x = -b / (2 * a)  # Один корень
        return x
    else:
        x1 = (-b + cmath.sqrt(D)) / (2 * a)
        x2 = (-b - cmath.sqrt(D)) / (2 * a)
        return x1, x2  # Два корня


a = float(input("Введите коэффициент a: "))
b = float(input("Введите коэффициент b: "))
c = float(input("Введите коэффициент c: "))

if a == 0:
    print("Коэффициент 'a' не может быть равен нулю, так как это перестает быть квадратным уравнением.")
else:
    result = discriminant(a, b, c)
    print(f"Решение уравнения: {result}")
