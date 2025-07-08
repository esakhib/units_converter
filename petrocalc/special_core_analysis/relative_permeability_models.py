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

# FIXME: нет точных коэффициентовов и не совпадает с источником


# ────────────────────────────────────────────────────────────────────
#   LET correlation
# ────────────────────────────────────────────────────────────────────
def krow_let(
        sw: float,
        swi: float,
        sorw: float,
        krow_swi: float,
        lo: float,
        eo: float,
        to: float,
) -> float:
    """
    Oil relative-permeability by **LET correlation**.

    Parameters
    ----------
    sw : float
        Water saturation (*Units['sw']*).
    swi : float
        Irreducible water saturation (*Units['swi']*).
    sorw : float
        Residual oil saturation after water flooding (*Units['sorw']*).
    krow_swi : float
        Oil relative permeability at `swi` (*Units['krow_swi']*).
    lo : float
        Empirical exponent *L* for oil phase (*Units['lo']*).
    eo : float
        Empirical exponent *E* for oil phase (*Units['eo']*).
    to : float
        Empirical exponent *T* for oil phase (*Units['to']*).

    Returns
    -------
    float
        Oil relative permeability (dimensionless).

    Source
    ------
    https://petroleumoffice.com/function/krowlet/
    """
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
    """
    Water relative-permeability by **LET correlation**.

    Parameters
    ----------
    sw : float
        Water saturation (*Units['sw']*).
    swi : float
        Irreducible water saturation (*Units['swi']*).
    sorw : float
        Residual oil saturation after water flooding (*Units['sorw']*).
    krw_sorw : float
        Water relative permeability at `sorw` (*Units['krw_sorw']*).
    lw : float
        Empirical exponent *L* for water phase (*Units['lw']*).
    ew : float
        Empirical exponent *E* for water phase (*Units['ew']*).
    tw : float
        Empirical exponent *T* for water phase (*Units['tw']*).

    Returns
    -------
    float
        Water relative permeability (dimensionless).

    Source
    ------
    https://petroleumoffice.com/function/krwlet/
    """
    return -1


# ────────────────────────────────────────────────────────────────────
#   Honarpour correlation
#   (oil / water; carbonate vs sandstone; wetting state)
# ────────────────────────────────────────────────────────────────────
def krow_honarpour_carb_inter_wet(sw: float, swi: float, sorw: float) -> float:
    """
    Oil kᵣ (limestone/dolomite, inter-wet) — Honarpour.

    Parameters
    ----------
    sw, swi, sorw : float
        See *Units* for individual units.

    Returns
    -------
    float
        Oil relative permeability (dimensionless).

    Source
    ------
    https://petroleumoffice.com/function/krowhonarpourcarbinterwet/
    """
    return -1


def krow_honarpour_sand_inter_wet(sw: float, swi: float, sorw: float) -> float:
    """See https://petroleumoffice.com/function/krowhonarpoursandinterwet/"""
    return -1


def krow_honarpour_carb_water_wet(sw: float, swi: float, sorw: float) -> float:
    """See https://petroleumoffice.com/function/krowhonarpourcarbwaterwet/"""
    return -1


def krow_honarpour_sand_water_wet(sw: float, swi: float, sorw: float) -> float:
    """See https://petroleumoffice.com/function/krowhonarpoursandwaterwet/"""
    return -1


def krw_honarpour_carb_inter_wet(sw: float, swi: float, sorw: float) -> float:
    """See https://petroleumoffice.com/function/krwhonarpourcarbinterwet/"""
    return -1


def krw_honarpour_sand_inter_wet(sw: float, swi: float, sorw: float) -> float:
    """See https://petroleumoffice.com/function/krwhonarpoursandinterwet/"""
    return -1


def krw_honarpour_carb_water_wet(sw: float, swi: float, sorw: float) -> float:
    """See https://petroleumoffice.com/function/krwhonarpourcarbwaterwet/"""
    return -1


def krw_honarpour_sand_water_wet(sw: float, swi: float, sorw: float) -> float:
    """See https://petroleumoffice.com/function/krwhonarpoursandwaterwet/"""
    return -1


# ────────────────────────────────────────────────────────────────────
#   Ibrahim-Koederitz correlation
#   (gas–liquid systems; uses gas saturation sg)
# ────────────────────────────────────────────────────────────────────
def krcgi_k_gas_cond(sg: float) -> float:
    """
    Condensate-oil kᵣᴄᵍ: Ibrahim-Koederitz gas-condensate correlation.

    Parameters
    ----------
    sg : float
        Gas saturation (*Units['sg']*).

    Returns
    -------
    float
        Condensate relative permeability (dimensionless).

    Source
    ------
    https://petroleumoffice.com/function/krcgikgascond/
    """
    return -1


def krgi_k_gas_cond(sg: float) -> float:
    """See https://petroleumoffice.com/function/krgikgascond/"""
    return -1


def krgi_k_gas_oil_carb(sg: float) -> float:
    """See https://petroleumoffice.com/function/krgikgasoilcarb/"""
    return -1


def krgl_k_gas_oil_sand(sg: float) -> float:
    """See https://petroleumoffice.com/function/krglkgasoilsand/"""
    return -1


def krgw_ik_gas_water(sg: float) -> float:
    """See https://petroleumoffice.com/function/krgwikgaswater/"""
    return -1


def krog_ik_gas_oil_carb(sg: float) -> float:
    """See https://petroleumoffice.com/function/krogikgasoilcarb/"""
    return -1


def krog_ik_gas_oil_sand(sg: float) -> float:
    """See https://petroleumoffice.com/function/krogikgasoilsand/"""
    return -1


#  — “krowl / krwl” (limestone & sandstone, various wetting)
def _krowl_template(sw: float) -> float:  # internal helper
    return -1


def krowi_k_carb_oil_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krowikcarboilwet/"""
    return _krowl_template(sw)


def krowi_k_carb_water_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krowikcarbwaterwet/"""
    return _krowl_template(sw)


def krowi_k_carb_inter_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krowikcarbinterwet/"""
    return _krowl_template(sw)


def krowi_k_carb_strong_water_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krowikcarbstrongwaterwet/"""
    return _krowl_template(sw)


def krowi_k_sand_oil_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krowiksandoilwet/"""
    return _krowl_template(sw)


def krowi_k_sand_water_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krowiksandwaterwet/"""
    return _krowl_template(sw)


def krowi_k_sand_inter_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krowiksandinterwet/"""
    return _krowl_template(sw)


def krowi_k_sand_strong_water_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krowiksandstrongwaterwet/"""
    return _krowl_template(sw)


def krwi_k_carb_oil_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krwikcarboilwet/"""
    return _krowl_template(sw)


def krwi_k_carb_water_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krwikcarbwaterwet/"""
    return _krowl_template(sw)


def krwi_k_carb_inter_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krwikcarbinterwet/"""
    return _krowl_template(sw)


def krwi_k_carb_strong_water_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krwikcarbstrongwaterwet/"""
    return _krowl_template(sw)


def krwi_k_sand_oil_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krwiksandoilwet/"""
    return _krowl_template(sw)


def krwi_k_sand_water_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krwiksandwaterwet/"""
    return _krowl_template(sw)


def krwi_k_sand_inter_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krwiksandinterwet/"""
    return _krowl_template(sw)


def krwi_k_sand_strong_water_wet(sw: float) -> float:
    """See https://petroleumoffice.com/function/krwiksandstrongwaterwet/"""
    return _krowl_template(sw)


def krwi_k_gas_water(sg: float) -> float:
    """
    Gas–water relative permeability (Ibrahim-Koederitz).

    Parameters
    ----------
    sg : float
        Gas saturation (*Units['sg']*).

    Returns
    -------
    float
        Gas relative permeability (dimensionless).

    Source
    ------
    https://petroleumoffice.com/function/krwikgaswater/
    """
    return -1
