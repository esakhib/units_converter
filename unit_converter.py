from enum import Enum


class UnitPressure(Enum):
    r"""Enum representing units of pressure.

        This enumeration provides a list of units for pressure measurements,
        such as pascals, atmospheres, and bar. Each unit is associated with an
        integer value for easy selection.

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

    """
    PA = 1
    HPA = 2
    KPA = 3
    MPA = 4
    AT = 5
    ATM = 6
    BAR = 7
    PSI = 8


class UnitVolumeFlowRate(Enum):
    r"""Enum representing units of volume flow rate.

        This enumeration provides a list of units for volume flow rate measurements,
        such as barrels per day and cubic meters per day. Each unit is associated
        with an integer value for easy selection.

        Attributes
        ----------
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

    BBL_D = 1
    MBBL_D = 2
    MMBBL_D = 3
    BBL_Y = 4
    MBBL_Y = 5
    MMBBL_Y = 6
    M3_D = 7
    E3M3_D = 8
    E6M3_D = 9
    SCF_D = 10
    MSCF_D = 11
    MMSCG_D = 12


class UnitConverter:
    r"""Converters for various units of volume flow rate and pressure.

    This module provides two separate converter classes: - `UnitConverter`: Converts between different units of
    volume flow rate, such as barrels per day and cubic meters per day. - `UnitPAConverter`: Converts between
    different units of pressure, such as pascals, atmospheres, and bars.

    Both classes use pre-defined conversion factors, mapping each unit to a base unit for conversion.

    Attributes ---------- UnitConverter: conversion_factors : dict A dictionary mapping each `Unit` to its conversion
    factor to barrels per day (bbl/d), which acts as the base unit. UnitPAConverter: conversion_factors : dict A
    dictionary mapping each `UnitPA` to its conversion factor to pascals (PA), which acts as the base unit.

    Methods
    -------
    UnitConverter:
        __init__(from_unit, to_unit, amount)
            Initializes the converter with a source unit, target unit, and quantity to convert.
        convert()
            Performs the conversion from the source unit to the target unit.

    UnitPAConverter:
        __init__(from_unit, to_unit, amount)
            Initializes the converter with a source pressure unit, target pressure unit, and quantity to convert.
        convert()
            Performs the conversion from the source pressure unit to the target pressure unit.

    """

    conversion_factors: dict[UnitVolumeFlowRate, float] = {
        UnitVolumeFlowRate.BBL_D: 1,
        UnitVolumeFlowRate.MBBL_D: 999.9999999999999,
        UnitVolumeFlowRate.MMBBL_D: 999999.9999999999,
        UnitVolumeFlowRate.BBL_Y: 0.0027379093109240003,
        UnitVolumeFlowRate.MBBL_Y: 2.737909310924,
        UnitVolumeFlowRate.MMBBL_Y: 2737.9093109240002,
        UnitVolumeFlowRate.M3_D: 6.289810770432104,
        UnitVolumeFlowRate.E3M3_D: 6289.810770432104,
        UnitVolumeFlowRate.E6M3_D: 6289810.770432104,
        UnitVolumeFlowRate.SCF_D: 0.17810760667903522,
        UnitVolumeFlowRate.MSCF_D: 178.10760667903523,
        UnitVolumeFlowRate.MMSCG_D: 178107.60667903523
    }

    @classmethod
    def convert_unit(cls, from_unit: UnitVolumeFlowRate, to_unit: UnitVolumeFlowRate, value: float) -> float:
        value_in_bbl_per_day = value * cls.conversion_factors[from_unit]
        return value_in_bbl_per_day / cls.conversion_factors[to_unit]


class UnitPAConverter:
    conversion_factors: dict[UnitPressure, float] = {
        UnitPressure.PA: 1,
        UnitPressure.HPA: 100,
        UnitPressure.KPA: 1000,
        UnitPressure.MPA: 1_000_000,
        UnitPressure.AT: 98066.5,
        UnitPressure.ATM: 101325,
        UnitPressure.BAR: 100000,
        UnitPressure.PSI: 6894.76
    }

    @classmethod
    def convert_unit(cls, from_unit: UnitPressure, to_unit: UnitPressure, value: float) -> float:
        value_in_pa = value * cls.conversion_factors[from_unit]
        return value_in_pa / cls.conversion_factors[to_unit]


def output_result(from_unit: Enum, to_unit: Enum, quantity: float, result: float) -> None:
    print(f"{quantity} {from_unit.name} = {result} {to_unit.name}")
