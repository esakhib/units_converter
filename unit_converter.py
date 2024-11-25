from dataclasses import dataclass
from typing import Iterable
import numpy as np


@dataclass
class UnitEnum:
    r"""
    A base class for defining individual measurement units.

    Attributes
    ----------
    factor : float
        The conversion factor for the unit relative to the base unit.
    symbol : str
        A textual representation of the unit.

    """

    factor: float
    symbol: str


class UnitCategory:
    r"""
    A base class for organizing categories of measurement units.

    This class serves as a foundation for defining specific categories of units
    such as pressure or volume flow rate. It provides methods to retrieve
    all units defined in a category.

    """

    @classmethod
    def get_units(cls):
        return [attr for attr in cls.__dict__.values() if isinstance(attr, UnitEnum)]


class Pressure(UnitCategory):
    r"""
    A unit category representing pressure measurements.

    This category includes common units of pressure and their conversion factors
    relative to the base unit (Pascal). Examples include atmospheric pressure, bar, and psi.

    Attributes
    ----------
    PA : UnitEnum
        Pascal, the SI base unit of pressure.
    HPA : UnitEnum
        Hectopascal, equivalent to 100 pascals.
    KPA : UnitEnum
        Kilopascal, equivalent to 1,000 pascals.
    MPA : UnitEnum
        Megapascal, equivalent to 1,000,000 pascals.
    AT : UnitEnum
        Technical atmosphere, used in engineering.
    ATM : UnitEnum
        Standard atmosphere, based on average sea-level pressure.
    BAR : UnitEnum
        Bar, equivalent to 100,000 pascals.
    PSI : UnitEnum
        Pounds per square inch, commonly used in the US.

    """

    PA = UnitEnum(1, "Pa: pascal")
    HPA = UnitEnum(100, "hPa: hectopascal")
    KPA = UnitEnum(1000, "kPa: kilopascal")
    MPA = UnitEnum(1000000, "MPa: megapascal")
    AT = UnitEnum(98066.5, "at: technical atmosphere")
    ATM = UnitEnum(101325, "atm: standard atmosphere")
    BAR = UnitEnum(100000, "bar: bar")
    PSI = UnitEnum(6894.76, "psi: pound-force per square inch")


class VolumeFlowRate(UnitCategory):
    r"""
    A unit category representing volume flow rate measurements.

    This category defines commonly used units for flow rate, including barrels per day
    and standard cubic feet per day, along with their conversion factors.

    Attributes
    ----------
    BBL_D : UnitEnum
        Barrel per day, a common unit in oil production.
    MBBL_D : UnitEnum
        Thousand barrels per day.
    MMBBL_D : UnitEnum
        Million barrels per day.
    BBL_Y : UnitEnum
        Barrel per year.
    MBBL_Y : UnitEnum
        Thousand barrels per year.
    MMBBL_Y : UnitEnum
        Million barrels per year.
    M3_D : UnitEnum
        Cubic meter per day.
    E3M3_D : UnitEnum
        Thousand cubic meters per day.
    E6M3_D : UnitEnum
        Million cubic meters per day.
    SCF_D : UnitEnum
        Standard cubic feet per day.
    MSCF_D : UnitEnum
        Thousand standard cubic feet per day.
    MMSCF_D : UnitEnum
        Million standard cubic feet per day.

    """

    BBL_D = UnitEnum(1, "bbl/d: barrel per day")
    MBBL_D = UnitEnum(1000, "mbbl/d: thousand barrels per day")
    MMBBL_D = UnitEnum(1000000, "mmbbl/d: million barrels per day")
    BBL_Y = UnitEnum(0.00273791, "bbl/y: barrels per year")
    MBBL_Y = UnitEnum(2.73791, "mbbl/y: thousand barrels per year")
    MMBBL_Y = UnitEnum(2737.91, "mmbbl/y: million barrels per year")
    M3_D = UnitEnum(6.28981, "m³/d: cubic meter per day")
    E3M3_D = UnitEnum(6289.81, "E3m³/d: thousand cubic meter per day")
    E6M3_D = UnitEnum(6289810.77, "E6m³/d: million cubic meter per day")
    SCF_D = UnitEnum(0.1781, "scf/d: standard cubic feet per day")
    MSCF_D = UnitEnum(178.1, "mscf/d: thousand standard cubic feet per day")
    MMSCF_D = UnitEnum(178107.6, "mmscf/d: million standard cubic feet per day")


class UnitConverter:
    @staticmethod
    def convert_unit(from_unit: UnitEnum, to_unit: UnitEnum, value: [float | Iterable[float]]) -> [float | np.ndarray]:
        """
        Convert from one unit to another within a specified category.

        Parameters
        ----------
        from_unit : UnitEnum
            The source unit.
        to_unit : UnitEnum
            The target unit.
        value : float | Iterable[float]
            The value(s) to be converted.

        Returns
        -------
        float | np.ndarray
            The converted value.

        """

        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            value = np.array(value)
        return value * (from_unit.factor / to_unit.factor)


def output_result(from_unit: UnitEnum, to_unit: UnitEnum, quantity: [float | Iterable[float]],
                  result: [float | np.ndarray]) -> None:
    """
    Outputs the results of unit conversion.

    Parameters
    ----------
    from_unit : UnitEnum
        The unit being converted from.
    to_unit : UnitEnum
        The unit being converted to.
    quantity : float | Iterable[float]
        The original quantity in the source unit.
    result : float | np.ndarray
        The converted quantity in the target unit.

    """

    if isinstance(quantity, Iterable):
        for q, r in zip(quantity, result):
            print(f"{q} {from_unit.symbol} = {r} {to_unit.symbol}")
    else:
        print(f"{quantity} {from_unit.symbol} = {result} {to_unit.symbol}")
