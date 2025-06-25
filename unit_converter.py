from dataclasses import dataclass
from typing import Iterable
import numpy as np


@dataclass
class UnitData:
    """
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
    """
    A base class for organizing categories of measurement units.

    This class serves as a foundation for defining specific categories of units
    such as pressure or volume flow rate. It provides methods to retrieve
    all units defined in a category.

    """

    @classmethod
    def get_units(cls):
        return [attr for attr in cls.__dict__.values() if isinstance(attr, UnitData)]


class PressureUnitCategory(UnitCategory):
    """
    A unit category representing pressure measurements.

    This category includes common units of pressure and their conversion factors
    relative to the base
    unit (Pascal). Examples include atmospheric pressure, bar, and psi.

    Attributes
    ----------
    PA : UnitData
        Pascal, the SI base unit of pressure.
    HPA : UnitData
        Hectopascal, equivalent to 100 pascals.
    KPA : UnitData
        Kilopascal, equivalent to 1,000 pascals.
    MPA : UnitData
        Megapascal, equivalent to 1,000,000 pascals.
    AT : UnitData
        Technical atmosphere, used in engineering.
    ATM : UnitData
        Standard atmosphere, based on average sea-level pressure.
    BAR : UnitData
        Bar, equivalent to 100,000 pascals.
    PSI : UnitData
        Pounds per square inch, commonly used in the US.

    """

    PA = UnitData(1, "Pa: pascal")
    HPA = UnitData(100, "hPa: hectopascal")
    KPA = UnitData(1000, "kPa: kilopascal")
    MPA = UnitData(1000000, "MPa: megapascal")
    AT = UnitData(98066.5, "at: technical atmosphere")
    ATM = UnitData(101325, "atm: standard atmosphere")
    BAR = UnitData(100000, "bar: bar")
    PSI = UnitData(6894.76, "psi: pound-force per square inch")


class VolumeFlowRateUnitCategory(UnitCategory):
    """
    A unit category representing volume flow rate measurements.

    This category defines commonly used units for flow rate, including barrels per day
    and standard cubic feet per day, along with their conversion factors.

    Attributes
    ----------
    BBL_D : UnitData
        Barrel per day, a common unit in oil production.
    MBBL_D : UnitData
        Thousand barrels per day.
    MMBBL_D : UnitData
        Million barrels per day.
    BBL_Y : UnitData
        Barrel per year.
    MBBL_Y : UnitData
        Thousand barrels per year.
    MMBBL_Y : UnitData
        Million barrels per year.
    M3_D : UnitData
        Cubic meter per day.
    E3M3_D : UnitData
        Thousand cubic meters per day.
    E6M3_D : UnitData
        Million cubic meters per day.
    SCF_D : UnitData
        Standard cubic feet per day.
    MSCF_D : UnitData
        Thousand standard cubic feet per day.
    MMSCF_D : UnitData
        Million standard cubic feet per day.

    """

    BBL_D = UnitData(1, "bbl/d: barrel per day")
    MBBL_D = UnitData(1000, "mbbl/d: thousand barrels per day")
    MMBBL_D = UnitData(1000000, "mmbbl/d: million barrels per day")
    BBL_Y = UnitData(0.00273791, "bbl/y: barrels per year")
    MBBL_Y = UnitData(2.73791, "mbbl/y: thousand barrels per year")
    MMBBL_Y = UnitData(2737.91, "mmbbl/y: million barrels per year")
    M3_D = UnitData(6.28981, "m³/d: cubic meter per day")
    E3M3_D = UnitData(6289.81, "E3m³/d: thousand cubic meter per day")
    E6M3_D = UnitData(6289810.77, "E6m³/d: million cubic meter per day")
    SCF_D = UnitData(0.1781, "scf/d: standard cubic feet per day")
    MSCF_D = UnitData(178.1, "mscf/d: thousand standard cubic feet per day")
    MMSCF_D = UnitData(178107.6, "mmscf/d: million standard cubic feet per day")


class VolumeRationsUnitCategory(UnitCategory):
    """
    A unit category representing volume-to-volume and gas-liquid ratio measurements.

    This category defines commonly used units for representing ratios of volume to volume,
    as well as standard gas-liquid ratio units such as standard cubic feet per stock tank barrel.

    Attributes
    ----------
    M3_M3 : UnitData
        Cubic meter per cubic meter, a dimensionless ratio commonly used in volume calculations.
    SM3_SM3 : UnitData
        Standard cubic meter per standard cubic meter, another dimensionless volume ratio.
    SCF_STB : UnitData
        Standard cubic feet per stock tank barrel, used to measure gas production relative to oil.
    MSCF_STB : UnitData
        Thousand standard cubic feet per stock tank barrel, a scaled version of SCF/STB.
    STB_SCF : UnitData
        Stock tank barrel per standard cubic foot, a reciprocal unit used in specific calculations.
    STB_MSCF : UnitData
        Stock tank barrel per thousand standard cubic feet, a scaled reciprocal of MSCF/STB.

    """

    M3_M3 = UnitData(1, "m³/m³: cubic meter per cubic meter")
    SM3_SM3 = UnitData(1, "sm³/sm³: standard cubic meter per standard cubic meter")
    SCF_STB = UnitData(0.17810760667903525, "scf/stb: standard cubic foot per stock tank barrel")
    MSCF_STB = UnitData(178.10760667903526, "mscf/stb: thousand standard cubic feet per stock tank barrel")
    STB_SCF = UnitData(5.614583333333334, "stb/scf: stock tank barrel per standard cubic foot")
    STB_MSCF = UnitData(0.005614583333333333, "stb/mscf: stock tank barrel per thousand standard cubic feet")


class UnitConverter:
    @staticmethod
    def convert_unit(from_unit: UnitData, to_unit: UnitData, value: [float | Iterable[float]]) -> [float | np.ndarray]:
        """
        Convert from one unit to another within a specified category.

        Parameters
        ----------
        from_unit : UnitData
            The source unit.
        to_unit : UnitData
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


def output_result(from_unit: UnitData, to_unit: UnitData, values: [float | Iterable[float]],
                  result: [float | np.ndarray]) -> None:
    """
    Outputs the results of unit conversion.

    Parameters
    ----------
    from_unit : UnitData
        The unit being converted from.
    to_unit : UnitData
        The unit being converted to.
    values : float | Iterable[float]
        The original values in the source unit.
    result : float | np.ndarray
        The converted values in the target unit.

    """

    if isinstance(values, Iterable):
        for q, r in zip(values, result):
            print(f"{q} {from_unit.symbol} = {r} {to_unit.symbol}")
    else:
        print(f"{values} {from_unit.symbol} = {result} {to_unit.symbol}")
