from enum import Enum
from typing import Dict


class Unit(Enum):
    r"""Enum representing units of volume flow rate.

    This enumeration provides a list of units for volume flow rate measurements,
    such as barrels per day and cubic meters per day. Each unit is associated
    with an integer value for easy selection.

    Attributes
    ----------
    bbl/b : int
        Barrel per day.
    mbbl_d : int
        Thousand barrels per day.
    mmbbl_d : int
        Million barrels per day.
    bbl_y : int
        Barrel per year.
    mbbl_y : int
        Thousand barrels per year.
    mmbbl_y : int
        Million barrels per year.
    m3_d : int
        Cubic meter per day.
    e3m3_d : int
        Standard cubic foot per day.
    e6m3_d : int
        Million cubic meters per day.
    scf_d : int
        Standard cubic foot per day.
    mscf_d : int
        Thousand standard cubic feet per day.
    mmscf_d : int
        Million standard cubic feet per day.
    """

    bbl_d = 1  # баррель в день
    mbbl_d = 2  # тысяча баррелей в день
    mmbbl_d = 3  # миллион баррелей в день
    bbl_y = 4  # баррель в год
    mbbl_y = 5  # тысяча баррелей в год
    mmbbl_y = 6  # миллион баррелей в год
    m3_d = 7  # кубометр в день
    e3m3_d = 8  # стандартный кубический фут в день
    e6m3_d = 9  # миллион кубических метров в сутки
    scf_d = 10  # стандартный кубический фут в сутки
    mscf_d = 11  # тысяча стандартных кубических футов в сутки
    mmscg_d = 12  # миллион стандартных кубических футов в сутки


class UnitConverter:
    r"""A converter for various units of volume flow rate.

    This class provides a method for converting between different units of volume flow rate.
    The conversion is based on pre-defined conversion factors that map each unit to barrels
    per day (bbl/d), which acts as the base unit.

    Attributes
    ----------
    conversion_factors : dict
        A dictionary mapping each Unit to its conversion factor to barrels per day (bbl/d).

    Methods
    -------
    __init__(from_unit, to_unit, amount)
        Initializes the converter with a source unit, target unit, and quantity to convert.
    convert()
        Performs the conversion from the source unit to the target unit.

    """

    # Коэффициенты перевода к баррелю в день (bbl/d)
    conversion_factors: Dict[Unit, float] = {
        Unit.bbl_d: 1,
        Unit.mbbl_d: 999.9999999999999,
        Unit.mmbbl_d: 999999.9999999999,
        Unit.bbl_y: 0.0027379093109240003,
        Unit.mbbl_y: 2.737909310924,
        Unit.mmbbl_y: 2737.9093109240002,
        Unit.m3_d: 6.289810770432104,
        Unit.e3m3_d: 6289.810770432104,
        Unit.e6m3_d: 6289810.770432104,
        Unit.scf_d: 0.17810760667903522,
        Unit.mscf_d: 178.10760667903523,
        Unit.mmscg_d: 178107.60667903523
    }

    def __init__(self, from_unit: Unit, to_unit: Unit, amount: float) -> None:
        r"""Initialize the UnitConverter with source and target units and the quantity to convert.

        Parameters
        ----------
        from_unit : Unit
            The source unit to convert from.
        to_unit : Unit
            The target unit to convert to.
        amount : float
            The quantity in the source unit to convert.

        """
        self.from_unit = from_unit
        self.to_unit = to_unit
        self.amount = amount

    def convert_unit(self) -> float:
        r"""Convert the quantity from the source unit to the target unit.

        This method first converts the given quantity to barrels per day (bbl/d) and then
        converts that intermediate value to the target unit.

        Returns
        -------
        float
            The converted quantity in the target unit.

        """

        # Перевод количества в баррели в день
        amount_in_bbl_per_day = self.amount * self.conversion_factors[self.from_unit]

        # Перевод из баррелей в день в целевую единицу
        converted_amount = amount_in_bbl_per_day / self.conversion_factors[self.to_unit]
        return converted_amount


def main():
    while True:
        print("Выберите единицы измерения:")
        for unit in Unit:
            print(f"{unit.value}.{unit.name.replace('_',' ')}")

        try:
            from_unit = int(input("Введите номер исходной единицы: "))
            if from_unit < 1 or from_unit > len(Unit):
                print("Выберите номер из предложенных единиц.")
                continue
            from_unit = Unit(from_unit)

            to_unit = int(input("Введите номер целевой единицы: "))
            if to_unit < 1 or to_unit > len(Unit):
                print("Выберите номер из предложенных единиц.")
                continue
            to_unit = Unit(to_unit)

            amount = float(input("Введите количество: "))
            if amount < 0:
                print("Количество не может быть отрицательным.")
                continue
            converter = UnitConverter(from_unit, to_unit, amount)
            result = converter.convert_unit()
            print(f"{amount} {from_unit.name} = {result} {to_unit.name}")
            break
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

main()
