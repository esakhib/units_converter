from __future__ import annotations

import math

__all__ = [
    "iftgo_abdul_majeed",
    "iftgo_baker_swerdloff",
]

# Interfacial Tension

# Pipe flow constants
GC = 32.174
FT2_PER_IN2 = 144.0
BBL_TO_FT3 = 5.615
SEC_PER_DAY = 86400

# Gas pipe flow constants
SCF_PER_MSCF = 1_000
AIR_DENS_STP = 0.0764
CP_TO_LB_FTS = 0.000671969


def iftgo_abdul_majeed(api: float, t_f: float, rso: float) -> float:
    """
    Calculate live-oil interfacial tension using the Abdul-Majeed correlation.

    Parameters
    ----------
    api : float
        Oil API gravity [°API].
    t_f : float
        Reservoir temperature [°F].
    rso : float
        Solution gas–oil ratio [scf/STB].

    Returns
    -------
    float
        Oil–water interfacial tension [dynes/cm].

    Source
    ------
    https://petroleumoffice.com/function/iftgoabdulmajeed/
    """
    sigma_od = (1.17013 - 1.694e-3 * t_f) * (38.085 - 0.259 * api)
    ratio = 0.056379 + 0.94362 * math.exp(-3.8491e-3 * rso)
    return sigma_od * ratio


def iftgo_baker_swerdloff(api: float, t_f: float, p: float) -> float:
    """
    Calculate live-oil interfacial tension using the Baker & Swerdloff correlation.

    Parameters
    ----------
    api : float
        Oil API gravity [°API].
    t_f : float
        Reservoir temperature [°F].
    p : float
        Pressure [psia].

    Returns
    -------
    float
        Oil–water interfacial tension [dynes/cm].

    Source
    ------
    https://petroleumoffice.com/function/iftgobakerswerdloff/
    """
    if t_f <= 68:
        sigma_od = 39.0 - 0.2571 * api
    elif t_f >= 100:
        sigma_od = 37.5 - 0.2571 * api
    else:
        sigma68 = 39.0 - 0.2571 * api
        sigma100 = 37.5 - 0.2571 * api
        sigma_od = sigma68 - (t_f - 68.0) * (sigma68 - sigma100) / 32.0

    p_mpa = p * 0.00689476
    f_live = 1.0 - 0.024 * (p_mpa ** 0.45)
    return sigma_od * f_live
