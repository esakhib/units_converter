from __future__ import annotations

__all__ = [
    "bw_mc_cain",
    "rsw_mc_cain",
    "rswp_mc_cain",
    "cw_sat_mc_cain",
    "cw_usat_osif",
    "uw_mc_cain",
    "uw1_mc_cain",
]


# Water PVT

# Water formation volume factor

def bw_mc_cain(p: float, t_f: float) -> float:
    """
    Calculate the water formation volume factor at reservoir conditions using the McCain (1990) correlation.

    Parameters
    ----------
    p : float
        Pressure [psia].
    t_f : float
        Temperature [°F].

    Returns
    -------
    float
        Water formation volume factor at reservoir pressure and temperature [bbl/STB].

    Source
    ------
    https://petroleumoffice.com/function/bwmccain/ :contentReference[oaicite:0]{index=0}
    """
    dv_p = (
            -1.95301e-9 * p * t_f
            - 1.72834e-13 * p ** 2 * t_f
            - 3.58922e-7 * p
            - 2.25341e-10 * p ** 2
    )
    dv_t = -1.0001e-2 + 1.33391e-4 * t_f + 5.50654e-7 * t_f ** 2
    return (1.0 + dv_p) * (1.0 + dv_t)


# Solution gas-water ratio

def rswp_mc_cain(p: float, t_f: float) -> float:
    """
    Calculate the solution gas–water ratio in pure water at pressure p and temperature t using the McCain (1990) correlation.

    Parameters
    ----------
    p : float
        Pressure [psia].
    t_f : float
        Temperature [°F].

    Returns
    -------
    float
        Solution gas–water ratio for pure water [scf/STB].

    Source
    ------
    https://petroleumoffice.com/function/rswpmccain/ :contentReference[oaicite:1]{index=1}
    """
    a = 8.15839 - 6.12265e-2 * t_f + 1.91663e-4 * t_f ** 2 - 2.1654e-7 * t_f ** 3
    b = 1.01021e-2 - 7.44241e-5 * t_f + 3.05553e-7 * t_f ** 2 - 2.94883e-10 * t_f ** 3
    c = -(9.02505 - 0.130237 * t_f + 8.53425e-4 * t_f ** 2
          - 2.34122e-6 * t_f ** 3 + 2.37049e-9 * t_f ** 4) * 1e-7
    return a + b * p + c * p ** 2


def rsw_mc_cain(rswp: float, salinity: float, t_f: float) -> float:
    """
    Calculate the solution gas–water ratio for reservoir water given pure-water ratio, salinity, and temperature using the McCain (1990) model.

    Parameters
    ----------
    rswp : float
        Solution gas–water ratio for pure water [scf/STB].
    salinity : float
        Salinity [% by weight solids].
    t_f : float
        Temperature [°F].

    Returns
    -------
    float
        Solution gas–water ratio for reservoir water [scf/STB].

    Source
    ------
    https://petroleumoffice.com/function/rswmccain/ :contentReference[oaicite:2]{index=2}
    """
    return rswp * 10 ** (-0.0840655 * salinity * t_f ** -0.285854)


# Water compressibility
# FIXME: присутствует погрешность в обоих функциях раздела
def cw_sat_mc_cain(p: float, t_f: float, cs: float) -> float:
    """
    Calculate the isothermal compressibility of reservoir water at saturation using the McCain (1990) correlation.

    Parameters
    ----------
    p : float
        Pressure [psia].
    t_f : float
        Temperature [°F].
    cs : float
        Salinity [g NaCl/L].

    Returns
    -------
    float
        Water compressibility at saturation [1/psi].

    Source
    ------
    https://petroleumoffice.com/function/cwsatmccain/ :contentReference[oaicite:3]{index=3}
    """
    a1, a2, a3, a4 = -1.95301e-9, -1.72834e-13, -3.58922e-7, -2.25341e-10
    d_bwp_dp = (a1 * t_f
                + 2.0 * a2 * p * t_f
                + a3
                + 2.0 * a4 * p)
    bwp = (1.0
           + (a1 * p * t_f + a2 * p ** 2 * t_f
              + a3 * p + a4 * p ** 2))
    cw_pure = -d_bwp_dp / bwp

    return cw_pure * (1.0 - 4.5e-4 * cs)


def cw_usat_osif(p: float, t_f: float, cs: float) -> float:
    """
    Calculate the isothermal compressibility of reservoir water above bubble point pressure using the Osif (2013) correlation.

    Parameters
    ----------
    p : float
        Pressure [psia].
    t_f : float
        Temperature [°F].
    cs : float
        Salinity [g NaCl/L].

    Returns
    -------
    float
        Water compressibility above bubble point [1/psi].

    Source
    ------
    https://petroleumoffice.com/function/cwusatosif/ :contentReference[oaicite:4]{index=4}
    """
    c0 = (5.135e-6
          + 1.045e-8 * t_f
          - 6.13e-11 * t_f ** 2)
    c1 = (1.07e-8
          + 6.03e-11 * t_f
          - 1.221e-13 * t_f ** 2)
    cw_pure = c0 + c1 * p
    return cw_pure * (1.0 - 2.0e-4 * cs)


# Water viscosity

def uw1_mc_cain(t_f: float, salinity: float) -> float:
    """
    Calculate the dead (atmospheric pressure) water viscosity using the McCain (1990) correlation.

    Parameters
    ----------
    t_f : float
        Temperature [°F].
    salinity : float
        Salinity [% by weight solids].

    Returns
    -------
    float
        Water viscosity at atmospheric pressure [cP].

    Source
    ------
    https://petroleumoffice.com/function/uw1mccain/ :contentReference[oaicite:5]{index=5}
    """
    s = salinity
    A = 109.574 - 8.40564 * s + 0.313314 * s ** 2 + 8.72213e-3 * s ** 3
    B = -1.12166 + 2.63951e-2 * s - 6.79461e-4 * s ** 2 \
        - 5.47119e-5 * s ** 3 + 1.55586e-6 * s ** 4
    return A * t_f ** B


def uw_mc_cain(p: float, uw1: float) -> float:
    """
    Calculate the water viscosity at reservoir pressure using the McCain (1990) correlation.

    Parameters
    ----------
    p : float
        Pressure [psia].
    uw1 : float
        Water viscosity at atmospheric pressure [cP].

    Returns
    -------
    float
        Water viscosity at reservoir pressure [cP].

    Source
    ------
    https://petroleumoffice.com/function/uwmccain/ :contentReference[oaicite:6]{index=6}
    """
    return uw1 * (0.9994 + 4.0295e-5 * p + 3.1062e-9 * p ** 2)
