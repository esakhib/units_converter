from __future__ import annotations

__all__ = [
    "pta_cd",
    "pta_ld",
    "pta_pd",
    "pta_rwd",
    "pta_td",
]


# dimensionless

# FIXME: не совпадает с источником
def pta_cd(c: float, poro: float, ct: float, h: float, rw: float) -> float:
    """
    Dimensionless wellbore-storage coefficient **Cᴅ**.

    Parameters
    ----------
    c : float
        Wellbore storage coefficient (*Units['c']* = bbl/psi).
    poro : float
        Rock porosity (*Units['poro']*), dimensionless.
    ct : float
        Total compressibility (*Units['ct']*), 1/psi.
    h : float
        Net formation thickness (*Units['h']*), ft.
    rw : float
        Wellbore radius (*Units['rw']*), ft.

    Returns
    -------
    float
        Dimensionless coefficient *Cᴅ* (placeholder value −1).

    Source
    ------
    https://petroleumoffice.com/function/ptacd/
    """
    return -1


def pta_ld(l: float, rw: float) -> float:
    """
    Dimensionless distance *Lᴅ* = L / rₚ.

    Parameters
    ----------
    l : float
        Distance from well, ft.
    rw : float
        Wellbore radius, ft.

    Returns
    -------
    float
        Dimensionless distance.
    """
    if any(x <= 0 for x in (l, rw)):
        raise ValueError("l and rw must be positive.")
    return l / rw


def pta_pd(
        p: float,
        pi: float,
        q: float,
        k: float,
        h: float,
        b: float,
        mu: float,
) -> float:
    """
    Dimensionless pressure drop for constant-rate production.

    Parameters
    ----------
    p : float
        Measured pressure, psi.
    pi : float
        Initial reservoir pressure, psi.
    q : float
        Surface flow rate, STB/d.
    k : float
        Permeability, mD.
    h : float
        Net pay thickness, ft.
    b : float
        Formation-volume factor, bbl/STB.
    mu : float
        Viscosity, cP.

    Returns
    -------
    float
        Dimensionless pressure drop *Pᴅ*.

    Notes
    -----
    ``Pd = 0.00708 · k · h · (Pi – P) / (q · B · μ)``.

    Source
    ------
    https://petroleumoffice.com/function/ptapd/
    """
    if any(x <= 0 for x in (q, k, h, b, mu)):
        raise ValueError("k, h, q, B, and μ must be positive.")
    return 0.00708 * k * h * (pi - p) / (q * b * mu)


def pta_rwd(r: float, rw: float) -> float:
    """
    Dimensionless radial distance *rᴅ* = r / rₚ.

    Parameters
    ----------
    r : float
        Radial distance from well, ft.
    rw : float
        Wellbore radius, ft.

    Returns
    -------
    float
        Dimensionless radius.
    """
    if any(x <= 0 for x in (r, rw)):
        raise ValueError("r and rw must be positive.")
    return r / rw


def pta_td(
        t: float,
        k: float,
        poro: float,
        mu: float,
        ct: float,
        rw: float,
) -> float:
    """
    Dimensionless time *tᴅ*.

    Parameters
    ----------
    t : float
        Elapsed time, h.
    k : float
        Permeability, mD.
    poro : float
        Porosity, fraction.
    mu : float
        Viscosity, cP.
    ct : float
        Total compressibility, 1/psi.
    rw : float
        Wellbore radius, ft.

    Returns
    -------
    float
        Dimensionless time *tᴅ*.

    Notes
    -----
    ``td = 0.0002637 · k · t / (φ · μ · Ct · rw²)``.

    Source
    ------
    https://petroleumoffice.com/function/ptatd/
    """
    if any(x <= 0 for x in (t, k, poro, mu, ct, rw)):
        raise ValueError("All inputs must be positive.")
    return 0.0002637 * k * t / (poro * mu * ct * rw ** 2)
