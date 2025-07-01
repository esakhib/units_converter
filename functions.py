from math import exp

def exponential_decline_rate(Qi: float, Di: float, t:float):
    return Qi*exp(-Di*t)

Qi = float(input("Введите начальный дебит в bbl/d:"))
Di = float(input("Введите начальную скорость падения дебита в 1/d:"))
t = float(input("Введите время, прошедшее с момента начала учета снижения в сутках:"))

res = exponential_decline_rate(Qi,Di,t)

print(f"{res} барелей в сутки")


def harmonic_decline_rate(Qi: float, Di: float, t:float):



Qi = float(input("Введите начальный дебит в bbl/d:"))
Di = float(input("Введите начальную скорость падения дебита в 1/d:"))
t = float(input("Введите время, прошедшее с момента начала учета снижения в сутках:"))
res = exponential_decline_rate(Qi, Di, t)
print(f"{res} барелей в сутки")