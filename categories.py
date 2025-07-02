from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class UnitData:
    """
    A base class for defining individual measurement units.

    Attributes
    ----------
    factor : float
        The conversion factor for the unit relative to the base unit.
    abbr : str
        A short textual representation of the unit.
    name : str
        Full textual representation of the unit.
    offset : float
        Shift in scales

    """

    factor: float
    abbr: str
    name: str = ""
    offset: float = 0.0


class UnitCategory(ABC):
    """
    A base class for organizing categories of measurement units.

    This class serves as a foundation for defining specific categories of units
    such as pressure or volume flow rate. It provides methods to retrieve
    all units defined in a category.

    """

    @classmethod
    def get_units(cls) -> list[UnitData]:
        # returns all UnitData that were defined in the class
        return [v for v in vars(cls).values() if isinstance(v, UnitData)]

    @abstractmethod
    def __str__(self) -> str:
        ...


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

    PA = UnitData(1, "Pa", "pascal")
    HPA = UnitData(100, "hPa", "hectopascal")
    KPA = UnitData(1000, "kPa", "kilopascal")
    MPA = UnitData(1000000, "MPa", "megapascal")
    AT = UnitData(98066.5, "at", "technical atmosphere")
    ATM = UnitData(101325, "atm", "standard atmosphere")
    BAR = UnitData(100000, "bar", "bar")
    PSI = UnitData(6894.76, "psi", "pound-force per square inch")

    def __str__(self):
        return "Pressure"


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

    BBL_D = UnitData(1, "bbl/d", "barrel per day")
    MBBL_D = UnitData(1000, "mbbl/d", "thousand barrels per day")
    MMBBL_D = UnitData(1000000, "mmbbl/d", "million barrels per day")
    BBL_Y = UnitData(0.00273791, "bbl/y", "barrels per year")
    MBBL_Y = UnitData(2.73791, "mbbl/y", "thousand barrels per year")
    MMBBL_Y = UnitData(2737.91, "mmbbl/y", "million barrels per year")
    M3_D = UnitData(6.28981, "m³/d", "cubic meter per day")
    E3M3_D = UnitData(6289.81, "E3m³/d", "thousand cubic meter per day")
    E6M3_D = UnitData(6289810.77, "E6m³/d", "million cubic meter per day")
    SCF_D = UnitData(0.1781, "scf/d", "standard cubic feet per day")
    MSCF_D = UnitData(178.1, "mscf/d", "thousand standard cubic feet per day")
    MMSCF_D = UnitData(178107.6, "mmscf/d", "million standard cubic feet per day")

    def __str__(self):
        return "Volume flow rate"


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

    M3_M3 = UnitData(1, "m³/m³", "cubic meter per cubic meter")
    SM3_SM3 = UnitData(1, "sm³/sm³", "standard cubic meter per standard cubic meter")
    SCF_STB = UnitData(0.17810760667903525, "scf/stb", "standard cubic foot per stock tank barrel")
    MSCF_STB = UnitData(178.10760667903526, "mscf/stb", "thousand standard cubic feet per stock tank barrel")
    STB_SCF = UnitData(5.614583333333334, "stb/scf", "stock tank barrel per standard cubic foot")
    STB_MSCF = UnitData(0.005614583333333333, "stb/mscf", "stock tank barrel per thousand standard cubic feet")

    def __str__(self):
        return "Volume rations"


class CompressibilityUnitCategory(UnitCategory):
    """
    Units having the dimension of 1/pressure
    """

    PER_PSI = UnitData(1.0 / 6894.76, "1/psi")
    PER_ATM = UnitData(1.0 / 101325, "1/atm")
    PER_PA = UnitData(1.0, "1/Pa")
    PER_BAR = UnitData(1.0 / 100000, "1/bar")

    def __str__(self):
        return "Compressibility"


class KinematicViscosityUnitCategory(UnitCategory):
    """
    Units that describes kinematic viscosity
    """

    M2_S = UnitData(1.0, "m2/s")
    ST = UnitData(1e-4, "St")
    CST = UnitData(1e-6, "cSt")

    def __str__(self):
        return "Kinematic viscosity"


class DynamicViscosityUnitCategory(UnitCategory):
    """
    Units that describes dynamic viscosity
    """

    PA_S = UnitData(1.0, "Pa·s")
    P = UnitData(0.1, "P")
    CP = UnitData(0.001, "cP")

    def __str__(self):
        return "Dynamic viscosity"


class DensityUnitCategory(UnitCategory):
    """
    Units related to density
    """
    KG_M3 = UnitData(1.0, "kg/m3")
    G_CM3 = UnitData(1000.0, "g/cm3")
    LBM_FT3 = UnitData(16.018463, "lbm/ft3")

    def __str__(self):
        return "Density"


class LengthUnitCategory(UnitCategory):
    """
    Units related to length
    """

    m = UnitData(1.0, "m")
    cm = UnitData(0.01, "cm")
    dam = UnitData(10.0, "dam")
    dm = UnitData(0.1, "dm")
    ft = UnitData(0.3048, "ft")
    inch = UnitData(0.0254, "in")
    km = UnitData(1000.0, "km")
    mi = UnitData(1609.344, "mi")
    mm = UnitData(0.001, "mm")
    yd = UnitData(0.9144, "yd")

    def __str__(self):
        return "Length"


class AreaUnitCategory(UnitCategory):
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

    def __str__(self):
        return "Area"


class ForceUnitCategory(UnitCategory):
    """
    Units related to force
    """
    N = UnitData(1.0, "N")
    DYNE = UnitData(1e-5, "dyne")
    LBF = UnitData(4.448221615, "lbf")

    def __str__(self):
        return "Force"


class VolumeUnitCategory(UnitCategory):
    """
    Units related to volume
    """
    BBL = UnitData(0.158_987_294_928, "bbl")
    MBBL = UnitData(158.987_294_928, "Mbbl")
    MMBBL = UnitData(158_987.294_928, "MMbbl")
    FT3 = UnitData(0.028_316_846_592, "ft3")
    SCF = UnitData(0.028_316_846_592, "scf")
    MSCF = UnitData(28.316_846_592, "Mscf")
    MMSCF = UnitData(28_316.846_592, "MMscf")
    BCF = UnitData(28_316_846.592, "Bcf")
    M3 = UnitData(1.0, "m3")
    E3M3 = UnitData(1_000.0, "E3m3")
    E6M3 = UnitData(1_000_000.0, "E6m3")
    KM3 = UnitData(1_000_000_000, "km3")
    DM3 = UnitData(1e-3, "dm3")
    CM3 = UnitData(1e-6, "cm3")
    MM3 = UnitData(1e-9, "mm3")
    MI3 = UnitData(4_168_181_825.44058, "mi3")
    YD3 = UnitData(0.764_554_857_984, "yd3")
    IN3 = UnitData(1.638_7064e-5, "in3")
    L = UnitData(1e-3, "l")
    ML = UnitData(1e-6, "ml")
    GAL = UnitData(0.003_785_411_784, "gal")
    ACRE_FT = UnitData(1_233.481_837_547_52, "acre.ft")

    def __str__(self):
        return "Volume"


class MassUnitCategory(UnitCategory):
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

    def __str__(self):
        return "Mass"


class EnergyUnitCategory(UnitCategory):
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

    def __str__(self):
        return "Energy"


class PowerUnitCategory(UnitCategory):
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

    def __str__(self):
        return "Power"


class TimeUnitCategory(UnitCategory):
    MS = UnitData(0.001, "ms")
    S = UnitData(1.0, "s")
    MIN = UnitData(60.0, "min")
    H = UnitData(3600.0, "h")
    D = UnitData(86400.0, "d")
    WK = UnitData(604800.0, "wk")
    MO = UnitData(2629746.0, "mo")
    Y = UnitData(31556952.0, "y")

    def __str__(self):
        return "Time"


class VelocityUnitCategory(UnitCategory):
    M_S = UnitData(1.0, "m/s")
    M_H = UnitData(1.0 / 3600, "m/h")
    M_D = UnitData(1.0 / 86400, "m/d")
    FT_S = UnitData(0.3048, "ft/s")
    FT_H = UnitData(0.3048 / 3600, "ft/h")
    FT_D = UnitData(0.3048 / 86400, "ft/d")
    KM_H = UnitData(1000.0 / 3600, "km/h")
    MI_H = UnitData(1609.344 / 3600, "mi/h")
    KNOT = UnitData(0.514444, "knot")

    def __str__(self):
        return "Velocity"


class TemperatureUnitCategory(UnitCategory):
    degK = UnitData(factor=1.0, offset=0.0, abbr="degK")
    degC = UnitData(factor=1.0, offset=273.15, abbr="degC")
    degF = UnitData(factor=5 / 9, offset=459.67, abbr="degF")
    degR = UnitData(factor=5 / 9, offset=0.0, abbr="degR")

    def __str__(self):
        return "Temperature"


class TemperatureIntervalUnitCategory(UnitCategory):
    deltaK = UnitData(1.0, "deltaK")
    deltaC = UnitData(1.0, "deltaC")
    deltaF = UnitData(5 / 9, "deltaF")
    deltaR = UnitData(5 / 9, "deltaR")

    def __str__(self):
        return "Temperature interval"


class ElectricResistanceUnitCategory(UnitCategory):
    ohm = UnitData(1.0, "ohm")
    Eohm = UnitData(1e18, "Eohm")
    Gohm = UnitData(1e9, "Gohm")
    Mohm = UnitData(1e6, "Mohm")
    Tohm = UnitData(1e12, "Tohm")
    cohm = UnitData(1e-2, "cohm")
    dohm = UnitData(1e-1, "dohm")
    fohm = UnitData(1e-15, "fohm")
    kohm = UnitData(1e3, "kohm")
    mohm = UnitData(1e-3, "mohm")
    nohm = UnitData(1e-9, "nohm")
    pohm = UnitData(1e-12, "pohm")
    uohm = UnitData(1e-6, "uohm")

    def __str__(self):
        return "Electric resistance"


class ElectricConductanceUnitCategory(UnitCategory):
    S = UnitData(1.0, "S")
    ES = UnitData(1e18, "ES")
    GS = UnitData(1e9, "GS")
    MS = UnitData(1e6, "MS")
    TS = UnitData(1e12, "TS")
    cS = UnitData(1e-2, "cS")
    dS = UnitData(1e-1, "dS")
    fS = UnitData(1e-15, "fS")
    kS = UnitData(1e3, "kS")
    mS = UnitData(1e-3, "mS")
    nS = UnitData(1e-9, "nS")
    pS = UnitData(1e-12, "pS")
    uS = UnitData(1e-6, "uS")

    def __str__(self):
        return "Electric conductance"


class ElectricCurrentUnitCategory(UnitCategory):
    A = UnitData(1.0, "A")
    EA = UnitData(1e18, "EA")
    GA = UnitData(1e9, "GA")
    MA = UnitData(1e6, "MA")
    TA = UnitData(1e12, "TA")
    cA = UnitData(1e-2, "cA")
    dA = UnitData(1e-1, "dA")
    fA = UnitData(1e-15, "fA")
    kA = UnitData(1e3, "kA")
    mA = UnitData(1e-3, "mA")
    nA = UnitData(1e-9, "nA")
    pA = UnitData(1e-12, "pA")
    uA = UnitData(1e-6, "uA")

    def __str__(self):
        return "Electric current"


class InductanceUnitCategory(UnitCategory):
    H = UnitData(1.0, "H")
    EH = UnitData(1e18, "EH")
    TH = UnitData(1e12, "TH")
    GH = UnitData(1e9, "GH")
    MH = UnitData(1e6, "MH")
    kH = UnitData(1e3, "kH")
    dH = UnitData(1e-1, "dH")
    cH = UnitData(1e-2, "cH")
    mH = UnitData(1e-3, "mH")
    uH = UnitData(1e-6, "uH")
    nH = UnitData(1e-9, "nH")
    fH = UnitData(1e-15, "fH")

    def __str__(self):
        return "Inductance"


class CapacitanceUnitCategory(UnitCategory):
    F = UnitData(1.0, "F")
    EF = UnitData(1e18, "EF")
    GF = UnitData(1e9, "GF")
    MF = UnitData(1e6, "MF")
    TF = UnitData(1e12, "TF")
    cF = UnitData(1e-2, "cF")
    dF = UnitData(1e-1, "dF")
    fF = UnitData(1e-15, "fF")
    kF = UnitData(1e3, "kF")
    mF = UnitData(1e-3, "mF")
    nF = UnitData(1e-9, "nF")
    pF = UnitData(1e-12, "pF")
    uF = UnitData(1e-6, "uF")

    def __str__(self):
        return "Capacitance"


class AmountOfSubstanceUnitCategory(UnitCategory):
    mol = UnitData(1.0, "mol")
    kmol = UnitData(1000.0, "kmol")
    lbmol = UnitData(453.59237, "lbmol")
    mmol = UnitData(1e-3, "mmol")
    umol = UnitData(1e-6, "umol")

    def __str__(self):
        return "Amount of substance"


class MolecularWeightUnitCategory(UnitCategory):
    KG_PER_MOL = UnitData(1.0, "kg/mol")
    G_PER_MOL = UnitData(0.001, "g/mol")
    LBM_PER_LBMOL = UnitData(0.45359237, "lbm/lbmol")

    def __str__(self):
        return "Molecular weight"
