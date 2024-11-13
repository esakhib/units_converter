from enum import Enum
from typing import Iterable
import numpy as np


class Unit(Enum):
    r"""Enum representing units for pressure and volume flow rate measurements.

    This enumeration provides a list of units for both pressure and volume flow rate
    measurements, covering a range of commonly used units such as pascals, barrels per day,
    and standard cubic feet per day. Each unit is associated with an integer value for easy selection.

    Attributes
    ----------
    PA : int
        Pascal, the SI unit of pressure.
    HPA : int
        Hectopascal, equivalent to 100 pascals.
    KPA : int
        Kilopascal, equivalent to 1000 pascals.
    MPA : int
        Megapascal, equivalent to 1,000,000 pascals.
    AT : int
        Technical atmosphere.
    ATM : int
        Atmosphere, the unit of pressure based on the average atmospheric pressure at sea level.
    BAR : int
        Bar, a unit of pressure, defined as 100,000 pascals.
    PSI : int
        Pounds per square inch, commonly used in the United States for pressure measurements.

    BBL_D : int
        Barrel per day.
    MBBL_D : int
        Thousand barrels per day.
    MMBBL_D : int
        Million barrels per day.
    BBL_Y : int
        Barrel per year.
    MBBL_Y : int
        Thousand barrels per year.
    MMBBL_Y : int
        Million barrels per year.
    M3_D : int
        Cubic meter per day.
    E3M3_D : int
        Standard cubic foot per day.
    E6M3_D : int
        Million cubic meters per day.
    SCF_D : int
        Standard cubic foot per day.
    MSCF_D : int
        Thousand standard cubic feet per day.
    MMSCF_D : int
        Million standard cubic feet per day.

    """

    PA = 1
    HPA = 2
    KPA = 3
    MPA = 4
    AT = 5
    ATM = 6
    BAR = 7
    PSI = 8

    BBL_D = 9
    MBBL_D = 10
    MMBBL_D = 11
    BBL_Y = 12
    MBBL_Y = 13
    MMBBL_Y = 14
    M3_D = 15
    E3M3_D = 16
    E6M3_D = 17
    SCF_D = 18
    MSCF_D = 19
    MMSCF_D = 20


conversion_factors = {
    'pressure': {
        Unit.PA: 1,
        Unit.HPA: 100,
        Unit.KPA: 1000,
        Unit.MPA: 1_000_000,
        Unit.AT: 98066.5,
        Unit.ATM: 101325,
        Unit.BAR: 1_000_00,
        Unit.PSI: 6894.76
    },
    'volume_flow_rate': {
        Unit.BBL_D: 1,
        Unit.MBBL_D: 999.9999999999999,
        Unit.MMBBL_D: 999999.9999999999,
        Unit.BBL_Y: 0.0027379093109240003,
        Unit.MBBL_Y: 2.737909310924,
        Unit.MMBBL_Y: 2737.9093109240002,
        Unit.M3_D: 6.289810770432104,
        Unit.E3M3_D: 6289.810770432104,
        Unit.E6M3_D: 6289810.770432104,
        Unit.SCF_D: 0.17810760667903522,
        Unit.MSCF_D: 178.10760667903523,
        Unit.MMSCF_D: 178107.60667903523
    }
}


class UnitConverter:

    @classmethod
    def convert_unit(cls, category: str, from_unit: Unit, to_unit: Unit,
                     value: [float | Iterable[float]]) -> [float | np.ndarray]:
        """
        Convert from one unit to another within a specified category (e.g., pressure or volume flow rate).

        Parameters
        ----------
        category : str
            The unit category ('pressure' or 'volume_flow_rate').
        from_unit : Unit
            The source unit within the category.
        to_unit : Unit
            The target unit within the category.
        value : [float, Iterable[float]]
            The value(s) to be converted (can be a single value or an iterable).

        Returns
        -------
        [float, np.ndarray]
            The converted value(s).

        """

        factors = conversion_factors[category]

        if isinstance(value, Iterable):
            values = np.array(value)
            factor_from = factors[from_unit]
            factor_to = factors[to_unit]
            return (values * factor_from) / factor_to
        else:
            factor_from = factors[from_unit]
            factor_to = factors[to_unit]
            return (value * factor_from) / factor_to


def output_result(from_unit: Unit, to_unit: Unit, quantity: [float | Iterable[float]],
                  result: [float | np.ndarray]) -> None:
    if isinstance(quantity, Iterable):
        for q, r in zip(quantity, result):
            print(f"{q} {from_unit.name} = {r} {to_unit.name}")
    else:
        print(f"{quantity} {from_unit.name} = {result} {to_unit.name}")
