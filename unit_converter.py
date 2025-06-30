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
    def get_units(cls) -> list[UnitData]:
        #returns all UnitData that were defined in the class
        return [v for v in vars(cls).values() if isinstance(v, UnitData)]


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

class CompressibilityCategory(UnitCategory):
    """
    Units having the dimension of 1/pressure
    """

    PER_PSI = UnitData(1.0 / 6894.76, "1/psi")
    PER_ATM = UnitData(1.0 / 101325, "1/atm")
    PER_PA = UnitData(1.0, "1/Pa")
    PER_BAR = UnitData(1.0 / 100000, "1/bar")

class KinematicViscosityCategory(UnitCategory):
    """
    Units that describes kinematic viscosity
    """

    M2_S = UnitData(1.0, "m2/s")
    ST = UnitData(1e-4, "St")
    CST = UnitData(1e-6, "cSt")

class DynamicViscosityCategory(UnitCategory):
    """
    Units that describes dynamic viscosity
    """

    PA_S = UnitData(1.0, "Pa·s")
    P = UnitData(0.1, "P")
    CP = UnitData(0.001, "cP")
class DensityCategory(UnitCategory):
    """
    Units related to density
    """
    KG_M3 = UnitData(1.0, "kg/m3")
    G_CM3 = UnitData(1000.0, "g/cm3")
    LBM_FT3 = UnitData(16.018463, "lbm/ft3")

class LengthCategory(UnitCategory):
    """
    Units related to length
    """

    KG_M3 = UnitData(1.0, "kg/m3")
    G_CM3 = UnitData(1000.0, "g/cm3")
    LBM_FT3 = UnitData(16.018463, "lbm/ft3")

class AreaCategory(UnitCategory):
    """
    Units related to area
    """
    M2 = UnitData(1.0, "m2")
    KM2 = UnitData(1e6, "km2")
    DM2 = UnitData(0.01, "dm2")
    CM2 = UnitData(0.0001, "cm2")
    MM2 = UnitData(1e-6, "mm2")
    MI2 = UnitData(2589988.110336, "mi2")
    YD2 = UnitData(0.83612736, "yd2")
    FT2 = UnitData(0.09290304, "ft2")
    IN2 = UnitData(0.00064516, "in2")
    HA = UnitData(1e4, "ha")
    ACRE = UnitData(4046.8564224, "acre")
    ARE = UnitData(100.0, "are")


class ForceCategory(UnitCategory):
    """
    Units related to force
    """
    N = UnitData(1.0, "N")
    DYNE = UnitData(1e-5, "dyne")
    LBF = UnitData(4.448221615, "lbf")

class VolumeCategory(UnitCategory):
    """
    Units related to volume
    """
    bbl = UnitData(0.158987294928, "bbl")
    mbbl = UnitData(158.987294928, "mbbl")
    mmbbl = UnitData(158987.294928, "mmbbl")
    ft3 = UnitData(0.028316846592, "ft3")
    scf = UnitData(0.028316846592, "scf")
    mscf = UnitData(28.316846592, "mscf")
    mmscf = UnitData(28316.846592, "mmscf")
    bcf = UnitData(28316846.592, "bcf")
    m3 = UnitData(1.0, "m3")
    E3m3 = UnitData(1000.0, "E3m3")
    E6m3 = UnitData(1000000.0, "E6m3")
    km3 = UnitData(1000000000.0, "km3")
    dm3 = UnitData(0.001, "dm3")
    cm3 = UnitData(0.000001, "cm3")
    mm3 = UnitData(1e-9, "mm3")
    mi3 = UnitData(4168181825.44058, "mi3")
    yd3 = UnitData(0.764554857984, "yd3")
    in3 = UnitData(1.6387064e-05, "in3")
    l = UnitData(0.001, "l")
    ml = UnitData(1e-6, "ml")
    gal = UnitData(0.003785411784, "gal")
    acre_ft = UnitData(1233.48183754752, "acre.ft")

class MassCategory(UnitCategory):
    KG = UnitData(1.0, "kg")
    G = UnitData(0.001, "g")
    MG = UnitData(1e-6, "mg")
    T = UnitData(1000.0, "t")
    ST = UnitData(6.35029318, "st")
    LBM = UnitData(0.45359237, "lbm")
    OZM = UnitData(0.028349523125, "ozm")
    OZM_TROY = UnitData(0.0311034768, "ozm[troy]")
    TON_UK = UnitData(1016.0469088, "ton[UK]")
    TON_US = UnitData(907.18474, "ton[US]")
    TONNE = UnitData(1000.0, "tonne")

class EnergyCategory(UnitCategory):
    J = UnitData(1.0, "J")
    kJ = UnitData(1e3, "kJ")
    mJ = UnitData(1e-3, "mJ")
    MJ = UnitData(1e6, "MJ")
    E6_BtuIT = UnitData(1e6 * 1055.05585262, "1E6 Btu[IT]")
    BtuIT = UnitData(1055.05585262, "Btu[IT]")
    BtuUK = UnitData(1055.05585262, "Btu[UK]")
    Btu_th = UnitData(1054.35026445, "Btu[th]")
    kW_h = UnitData(3.6e6, "kW.h")
    MW_h = UnitData(3.6e9, "MW.h")
    GW_h = UnitData(3.6e12, "GW.h")
    GeV = UnitData(1.602176634e-10, "GeV")
    MeV = UnitData(1.602176634e-13, "MeV")
    keV = UnitData(1.602176634e-16, "keV")
    meV = UnitData(1.602176634e-22, "meV")

class PowerCategory(UnitCategory):
    W = UnitData(1.0, "W")
    EW = UnitData(1e18, "EW")
    GW = UnitData(1e9, "GW")
    MW = UnitData(1e6, "MW")
    TW = UnitData(1e12, "TW")
    cW = UnitData(1e-2, "cW")
    dW = UnitData(1e-1, "dW")
    fW = UnitData(1e-15, "fW")
    hp = UnitData(745.69987158227, "hp")
    hp_elec = UnitData(746.0, "hp[elec]")
    hp_hyd = UnitData(745.69987158227, "hp[hyd]")
    hp_metric = UnitData(735.49875, "hp[metric]")
    kW = UnitData(1e3, "kW")
    mW = UnitData(1e-3, "mW")
    nW = UnitData(1e-9, "nW")
    pW = UnitData(1e-12, "pW")
    uW = UnitData(1e-6, "uW")
    tonRefrig = UnitData(3516.852842, "tonRefrig")

class TimeCategory(UnitCategory):
    MS = UnitData(0.001, "ms")
    S = UnitData(1.0, "s")
    MIN = UnitData(60.0, "min")
    H = UnitData(3600.0, "h")
    D = UnitData(86400.0, "d")
    WK = UnitData(604800.0, "wk")
    MO = UnitData(2629746.0, "mo")
    Y = UnitData(31556952.0, "y")

class VelocityCategory(UnitCategory):
    M_S = UnitData(1.0, "m/s")
    M_H = UnitData(1.0 / 3600, "m/h")
    M_D = UnitData(1.0 / 86400, "m/d")
    FT_S = UnitData(0.3048, "ft/s")
    FT_H = UnitData(0.3048 / 3600, "ft/h")
    FT_D = UnitData(0.3048 / 86400, "ft/d")
    KM_H = UnitData(1000.0 / 3600, "km/h")
    MI_H = UnitData(1609.344 / 3600, "mi/h")
    KNOT = UnitData(0.514444, "knot")

class UnitConverter:
    @staticmethod
    def convert_unit(from_unit: UnitData, to_unit: UnitData, value: float | Iterable[float]) -> float | np.ndarray:
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


def output_result(from_unit: UnitData, to_unit: UnitData, values: float | Iterable[float], result: float | np.ndarray) -> None:
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
        for original, converted in zip(values, result):
            print(f"{original} {from_unit.symbol} = {converted} {to_unit.symbol}")
    else:
        print(f"{values} {from_unit.symbol} = {result} {to_unit.symbol}")
