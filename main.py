from enum import Enum


class UnitPA(Enum):
    PA = 1
    HPA = 2
    KPA = 3
    MPA = 4
    AT = 5
    ATM = 6
    BAR = 7
    PSI = 8


class Unit(Enum):
    bbl_d = 1
    mbbl_d = 2
    mmbbl_d = 3
    bbl_y = 4
    mbbl_y = 5
    mmbbl_y = 6
    m3_d = 7
    e3m3_d = 8
    e6m3_d = 9
    scf_d = 10
    mscf_d = 11
    mmscg_d = 12


class UnitConverter:
    conversion_factors: dict[Unit, float] = {
        Unit.bbl_d: 1,
        Unit.mbbl_d: 1000,
        Unit.mmbbl_d: 1000000,
        Unit.bbl_y: 0.0027379,
        Unit.mbbl_y: 2.7379,
        Unit.mmbbl_y: 2737.9,
        Unit.m3_d: 6.28981,
        Unit.e3m3_d: 6289.81,
        Unit.e6m3_d: 6289810,
        Unit.scf_d: 0.1781,
        Unit.mscf_d: 178.1,
        Unit.mmscg_d: 178100
    }

    @classmethod
    def convert(cls, from_unit: Unit, to_unit: Unit, value: float) -> float:
        value_in_bbl_per_day = value * cls.conversion_factors[from_unit]
        return value_in_bbl_per_day / cls.conversion_factors[to_unit]


class UnitPAConverter:
    conversion_factors: dict[UnitPA, float] = {
        UnitPA.PA: 1,
        UnitPA.HPA: 100,
        UnitPA.KPA: 1000,
        UnitPA.MPA: 1_000_000,
        UnitPA.AT: 98066.5,
        UnitPA.ATM: 101325,
        UnitPA.BAR: 100000,
        UnitPA.PSI: 6894.76
    }

    @classmethod
    def convert(cls, from_unit: UnitPA, to_unit: UnitPA, value: float) -> float:
        value_in_pa = value * cls.conversion_factors[from_unit]
        return value_in_pa / cls.conversion_factors[to_unit]


class GeneralUnitConverter:
    def __init__(self, from_unit, to_unit, value):
        self.from_unit = from_unit
        self.to_unit = to_unit
        self.value = value


def output_result(from_unit, to_unit, amount, result):
    print(f"{amount} {from_unit.name} = {result} {to_unit.name}")


def output_result(from_unit, to_unit, amount, result):
    print(f"{amount} {from_unit.name} = {result} {to_unit.name}")


def main():
    while True:
        print("Выберите категорию единиц измерения:")
        print("1. Давление (Pressure)")
        print("2. Объемный расход (Volume Flow Rate)")

        try:
            category_choice = int(input("Введите номер категории: "))
            if category_choice == 1:
                unit_class = UnitPA
                break
            elif category_choice == 2:
                unit_class = Unit
                break
            else:
                print("Выберите правильную категорию.")
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

    print(f"Вы выбрали категорию: {unit_class.__name__}")

    while True:
        print("Выберите единицу измерения:")
        for unit in unit_class:
            print(f"{unit.value}. {unit.name.replace('_', '/')}")

        try:
            from_unit_value = int(input("Введите номер исходной единицы: "))
            if from_unit_value < 1 or from_unit_value > len(unit_class):
                print("Выберите номер из предложенных единиц.")
                continue
            from_unit = unit_class(from_unit_value)

            to_unit_value = int(input("Введите номер целевой единицы: "))
            if to_unit_value < 1 or to_unit_value > len(unit_class):
                print("Выберите номер из предложенных единиц.")
                continue
            to_unit = unit_class(to_unit_value)

            amount = float(input("Введите количество: "))
            if amount < 0:
                print("Количество не может быть отрицательным.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

    # Конвертация значения
    if unit_class == UnitPA:
        result = UnitPAConverter.convert(from_unit, to_unit, amount)
    else:
        result = UnitConverter.convert(from_unit, to_unit, amount)

    output_result(from_unit, to_unit, amount, result)


main()
