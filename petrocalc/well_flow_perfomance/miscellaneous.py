from __future__ import annotations

import math

__all__ = [
    "drainage_area_hor_well_1",
    "drainage_area_hor_well_2",
    "drainage_radius",
    "effective_wellbore_radius",
    "equivalent_skin_factor",
]


# Miscellaneous

# Drainage geometry

def drainage_area_hor_well_1(l: float, b_length: float) -> float:
    """
    Drainage area of a horizontal well – **Joshi Method 1**
    (rectangle *L × 2 b* plus two half-circles of radius *b*).

    Parameters
    ----------
    l : float
        Length of the horizontal section, ft.
    b_length : float
        Radius of the end half-circles, ft.

    Returns
    -------
    float
        Drainage area, **acres**.

    Source
    ------
    https://petroleumoffice.com/function/drainageareahorwell1/
    """
    area_ft2 = (math.pi * b_length ** 2) + (2.0 * b_length * l)
    return area_ft2 / 43_560.0


def drainage_area_hor_well_2(l: float, b_length: float) -> float:
    """
    Drainage area of a horizontal well – **Joshi Method 2**
    (ellipse with semi-minor axis *b* and semi-major axis *a = L/2 + b*).

    Parameters
    ----------
    l : float
        Length of the horizontal section, ft.
    b_length : float
        Semi-minor axis of the ellipse, ft.

    Returns
    -------
    float
        Drainage area, **acres**.

    Source
    ------
    https://petroleumoffice.com/function/drainageareahorwell2/
    """
    a = l * 0.5 + b_length
    area_ft2 = math.pi * a * b_length
    return area_ft2 / 43_560.0


def drainage_radius(a: float) -> float:
    """
    Effective drainage radius that gives the same area as a circle.

    Parameters
    ----------
    a : float
        Drainage area, **acres**.

    Returns
    -------
    float
        Equivalent radius *Re*, ft.

    Source
    ------
    https://petroleumoffice.com/function/drainageradius/
    """
    return math.sqrt(a * 43_560.0 / math.pi)


def effective_wellbore_radius(rw: float, s: float) -> float:
    """
    Effective wellbore radius that reproduces a given skin factor.

    Parameters
    ----------
    rw : float
        Actual wellbore radius, ft.
    s : float
        Skin factor (dimensionless).

    Returns
    -------
    float
        Effective wellbore radius *rₑ*, ft.

    Notes
    -----
    Uses the classical relation *rₑ = r_w · e^(–S)*.

    Source
    ------
    https://petroleumoffice.com/function/effectivewellboreradius/
    """
    return rw * math.exp(-s)


# FIXME: не совпадает с источником
def equivalent_skin_factor(
    xf: float,
    w: float,
    k_fracture: float,
    k: float,
    rw: float,
) -> float:
    """
    Equivalent skin factor for a **vertically fractured** well.

    Parameters
    ----------
    xf : float
        Fracture half-length, ft (*Units['xf']*).
    w : float
        Fracture width, ft (*Units['w']*).
    k_fracture : float
        Fracture permeability, mD (*Units['k_fracture']*).
    k : float
        Reservoir permeability, mD (*Units['k']*).
    rw : float
        Wellbore radius, ft (*Units['rw']*).

    Returns
    -------
    float
        Equivalent skin factor (dimensionless).

    Source
    ------
    https://petroleumoffice.com/function/equivalentskinfactor/
    """
    return -1

