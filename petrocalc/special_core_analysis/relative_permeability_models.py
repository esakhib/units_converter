from __future__ import annotations

__all__ = [
    "krow_corey",
    "krw_corey",
    "krow_let",
    "krw_let",
    "krow_honarpour_carb_inter_wet",
    "krow_honarpour_sand_inter_wet",
    "krw_honarpour_carb_inter_wet",
    "krw_honarpour_sand_inter_wet",
    "krow_honarpour_carb_water_wet",
    "krow_honarpour_sand_water_wet",
    "krw_honarpour_carb_water_wet",
    "krw_honarpour_sand_water_wet",
    "krcgl_k_gas_cond",
    "krgl_k_gas_cond",
    "krgl_k_gas_oil_carb",
    "krgl_k_gas_oil_sand",
    "krgw_ik_gas_water",
    "krog_ik_gas_oil_carb",
    "krog_ik_gas_oil_sand",
    "krowl_k_carb_oil_wet",
    "krowl_k_carb_water_wet",
    "krowl_k_carb_inter_wet",
    "krowl_k_carb_strong_water_wet",
    "krowl_k_sand_oil_wet",
    "krowl_k_sand_water_wet",
    "krowl_k_sand_inter_wet",
    "krowl_k_sand_strong_water_wet",
    "krwl_k_carb_oil_wet",
    "krwl_k_carb_water_wet",
    "krwl_k_carb_inter_wet",
    "krwl_k_carb_strong_water_wet",
    "krwl_k_gas_water",
    "krwl_k_sand_oil_wet",
    "krwl_k_sand_water_wet",
    "krwl_k_sand_inter_wet",
    "krwl_k_sand_strong_water_wet",
]


# Special core analysis

# Relative permeability models

# Corey correlation

def krow_corey(
        sw: float,
        swi: float,
        sorw: float,
        krow_swi: float,
        no: float,
) -> float:
    """
    Corey-type relative permeability to oil (**Kro**).

    Parameters
    ----------
    sw : float
        Current water saturation, fraction.
    swi : float
        Irreducible (minimum) water saturation, fraction.
    sorw : float
        Residual oil saturation after water flooding, fraction.
    krow_swi : float
        End-point oil relative permeability at *Swi* (usually 1.0), dimensionless.
    no : float
        Corey oil exponent, dimensionless.

    Returns
    -------
    float
        Oil relative permeability *Kro*, dimensionless.

    Notes
    -----
    Uses the normalised saturation

        ``Se = (Sw − Swi) / (1 − Swi − Sorw)``

    and the Corey expression

        ``Kro = KrowSwi · (1 − Se)ⁿᵒ``

    Result is clipped to the range 0 … KrowSwi.

    Source
    ------
    https://petroleumoffice.com/function/krowcorey/
    """
    if not (0 <= sw <= 1 and 0 <= swi < 1 and 0 <= sorw < 1 and no > 0 and krow_swi > 0):
        raise ValueError("Check saturation/exponent inputs.")
    denom = 1.0 - swi - sorw
    if denom <= 0:
        raise ValueError("Swi + Sorw must be < 1.")
    se = (sw - swi) / denom
    se = min(max(se, 0.0), 1.0)
    kro = krow_swi * (1.0 - se) ** no
    return max(0.0, min(kro, krow_swi))


def krw_corey(
        sw: float,
        swi: float,
        sorw: float,
        krw_sorw: float,
        nw: float,
) -> float:
    """
    Corey-type relative permeability to water (**Krw**).

    Parameters
    ----------
    sw : float
        Current water saturation, fraction.
    swi : float
        Irreducible (minimum) water saturation, fraction.
    sorw : float
        Residual oil saturation after water flooding, fraction.
    krw_sorw : float
        End-point water relative permeability at *Sorw*, dimensionless.
    nw : float
        Corey water exponent, dimensionless.

    Returns
    -------
    float
        Water relative permeability *Krw*, dimensionless.

    Notes
    -----
    Normalised saturation

        ``Se = (Sw − Swi) / (1 − Swi − Sorw)``

    Corey form

        ``Krw = KrwSorw · Seⁿʷ``

    Result is clipped to the range 0 … KrwSorw.

    Source
    ------
    https://petroleumoffice.com/function/krwcorey/
    """
    if not (0 <= sw <= 1 and 0 <= swi < 1 and 0 <= sorw < 1 and nw > 0 and krw_sorw > 0):
        raise ValueError("Check saturation/exponent inputs.")
    denom = 1.0 - swi - sorw
    if denom <= 0:
        raise ValueError("Swi + Sorw must be < 1.")
    se = (sw - swi) / denom
    se = min(max(se, 0.0), 1.0)
    krw = krw_sorw * se ** nw
    return max(0.0, min(krw, krw_sorw))


# LET correlation

# FIXME: не совпадает с источником
def krow_let(
        sw: float,
        swi: float,
        sorw: float,
        krow_swi: float,
        lo: float,
        eo: float,
        to: float,
) -> float:
    return -1


def krw_let(
        sw: float,
        swi: float,
        sorw: float,
        krw_sorw: float,
        lw: float,
        ew: float,
        tw: float,
) -> float:
    return -1


# Honarpour correlation
# FIXME: нет коэффициентов для точного вычисения каждой из функций
def krow_honarpour_carb_inter_wet() -> float:
    return -1


def krow_honarpour_sand_inter_wet() -> float:
    return -1


def krow_honarpour_carb_water_wet() -> float:
    return -1


def krow_honarpour_sand_water_wet() -> float:
    return -1


def krw_honarpour_carb_inter_wet() -> float:
    return -1


def krw_honarpour_sand_inter_wet() -> float:
    return -1


def krw_honarpour_carb_water_wet() -> float:
    return -1


def krw_honarpour_sand_water_wet() -> float:
    return -1


# Ibrahim-Koederitz correlation
# FIXME: нет коэффициентов для точного вычисения каждой из функций
def krcgl_k_gas_cond() -> float:
    return -1


def krgl_k_gas_cond() -> float:
    return -1


def krgl_k_gas_oil_carb() -> float:
    return -1


def krgl_k_gas_oil_sand() -> float:
    return -1


def krgw_ik_gas_water() -> float:
    return -1


def krog_ik_gas_oil_carb() -> float:
    return -1


def krog_ik_gas_oil_sand() -> float:
    return -1


def krowl_k_carb_oil_wet() -> float:
    return -1


def krowl_k_carb_water_wet() -> float:
    return -1


def krowl_k_carb_inter_wet() -> float:
    return -1


def krowl_k_carb_strong_water_wet() -> float:
    return -1


def krowl_k_sand_oil_wet() -> float:
    return -1


def krowl_k_sand_water_wet() -> float:
    return -1


def krowl_k_sand_inter_wet() -> float:
    return -1


def krowl_k_sand_strong_water_wet() -> float:
    return -1


def krwl_k_carb_oil_wet() -> float:
    return -1


def krwl_k_carb_water_wet() -> float:
    return -1


def krwl_k_carb_inter_wet() -> float:
    return -1


def krwl_k_carb_strong_water_wet() -> float:
    return -1


def krwl_k_sand_oil_wet() -> float:
    return -1


def krwl_k_sand_water_wet() -> float:
    return -1


def krwl_k_sand_inter_wet() -> float:
    return -1


def krwl_k_sand_strong_water_wet() -> float:
    return -1


def krwl_k_gas_water() -> float:
    return -1
