from __future__ import annotations

import math

__all__ = [
    "zfactor_brill_beggs",
    "zfactor_dak",
    "ppc_standing",
    "tpc_standing",
    "ppc_sutton",
    "tpc_sutton",
    "bg",
    "ug_lge",
    "cg",
    "gas_density",
]


# gas PVT

# Z factor
def zfactor_brill_beggs(ppr: float, tpr: float) -> float:
    """
    Calculate the gas compressibility factor (Z) using the Brill & Beggs correlation.

    Parameters
    ----------
    ppr : float
        Pseudo-reduced pressure [–].
    tpr : float
        Pseudo-reduced temperature [–].

    Returns
    -------
    float
        Gas compressibility factor (Z) [dimensionless].

    Source
    ------
    https://petroleumoffice.com/function/zfactorbrillbeggs/
    """
    A = 1.39 * math.sqrt(tpr - 0.92) - 0.36 * tpr - 0.101
    B = (0.62 - 0.23 * tpr) * ppr + ((0.066 / tpr) - 0.037) * ppr ** 2 + 0.32 * ppr ** 6
    C = 0.132 - 0.32 * math.log10(tpr)
    D = 10 ** (0.3106 - 0.49 * tpr + 0.1824 * tpr ** 2)
    exp_term = math.exp(-B) if B < 700 else 0.0
    return A + (1 - A) * exp_term + C * ppr ** D


def zfactor_dak(ppr: float, tpr: float) -> float:
    """
    Calculate the gas compressibility factor (Z) using the Dranchuk & Abou-Kassem (DAK) EoS correlation.

    Parameters
    ----------
    ppr : float
        Pseudo-reduced pressure [–].
    tpr : float
        Pseudo-reduced temperature [–].

    Returns
    -------
    float
        Gas compressibility factor (Z) [dimensionless].

    Source
    ------
    https://petroleumoffice.com/function/zfactordak/
    """
    A1, A2, A3, A4, A5 = 0.3265, -1.07, -0.5339, 0.01569, -0.05165
    A6, A7, A8 = 0.5475, -0.7361, 0.1844
    A9, A10, A11 = 0.1056, 0.6134, 0.721
    rho_r = 0.27 * ppr / tpr
    max_iter = 100
    tol = 1e-10
    z = -1
    for _ in range(max_iter):
        z = (
                1
                + (A1 + A2 / tpr + A3 / tpr ** 3 + A4 / tpr ** 4 + A5 / tpr ** 5) * rho_r
                + (A6 + A7 / tpr + A8 / tpr ** 2) * rho_r ** 2
                - A9 * (A7 / tpr + A8 / tpr ** 2) * rho_r ** 5
                + A10 * (1 + A11 * rho_r ** 2) * rho_r ** 2 / tpr ** 3 * math.exp(-A11 * rho_r ** 2)
        )
        rho_new = 0.27 * ppr / (z * tpr)
        if abs(rho_new - rho_r) < tol:
            return z
        rho_r = 0.2 * rho_new + 0.8 * rho_r
    return z


# pseudo critical P and T

def ppc_standing(sg_gas: float) -> float:
    """
    Calculate the pseudo-critical pressure of hydrocarbon gas using the Standing correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].

    Returns
    -------
    float
        Pseudo-critical pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/ppcstanding/ :contentReference[oaicite:0]{index=0}
    """
    return 706.0 - 51.7 * sg_gas - 11.1 * sg_gas ** 2


def tpc_standing(sg_gas: float) -> float:
    """
    Calculate the pseudo-critical temperature of hydrocarbon gas using the Standing correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].

    Returns
    -------
    float
        Pseudo-critical temperature [°R].

    Source
    ------
    https://petroleumoffice.com/function/tpcstanding/ :contentReference[oaicite:1]{index=1}
    """
    return 187.0 + 330.0 * sg_gas - 71.5 * sg_gas ** 2


def ppc_sutton(sg_gas: float) -> float:
    """
    Calculate the pseudo-critical pressure of hydrocarbon gas using the Sutton correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].

    Returns
    -------
    float
        Pseudo-critical pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/ppcsutton/ :contentReference[oaicite:2]{index=2}
    """
    return 756.8 - 131.0 * sg_gas - 3.6 * sg_gas ** 2


def tpc_sutton(sg_gas: float) -> float:
    """
    Calculate the pseudo-critical temperature of hydrocarbon gas using the Sutton correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].

    Returns
    -------
    float
        Pseudo-critical temperature [°R].

    Source
    ------
    https://petroleumoffice.com/function/tpcsutton/ :contentReference[oaicite:3]{index=3}
    """
    return 169.2 + 349.5 * sg_gas - 74.0 * sg_gas ** 2


# Gas formation volume factor
def bg(p: float, t_r: float, z_factor: float) -> float:
    """
    Calculate the gas formation volume factor.

    Parameters
    ----------
    p : float
        Pressure [psia].
    t_r : float
        Temperature [°R].
    z_factor : float
        Gas compressibility factor (Z), dimensionless.

    Returns
    -------
    float
        Gas formation volume factor [rcf/scf].

    Source
    ------
    https://petroleumoffice.com/function/bg/ :contentReference[oaicite:4]{index=4}
    """
    return 0.02827 * z_factor * t_r / p


# gas viscosity
def ug_lge(z_factor: float, sg_gas: float, p: float, t_r: float) -> float:
    """
    Calculate gas viscosity using the Lee, Gonzales & Eakin correlation.

    Parameters
    ----------
    z_factor : float
        Gas compressibility factor (Z), dimensionless.
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    p : float
        Pressure [psia].
    t_r : float
        Temperature [°R].

    Returns
    -------
    float
        Gas viscosity [cP].

    Source
    ------
    https://petroleumoffice.com/function/uglge/ :contentReference[oaicite:5]{index=5}
    """
    m = 28.967 * sg_gas
    k = (9.4 + 0.02 * m) * t_r ** 1.5 / (209 + 19 * m + t_r)
    x = 3.5 + 986 / t_r + 0.01 * m
    y = 2.4 - 0.2 * x
    rho = 28.967 * sg_gas * p / (z_factor * 10.7316 * t_r)
    return 1.0e-4 * k * math.exp(x * (rho / 62.4) ** y)


# gas compressibility
def cg(p: float, t_r: float, sg_gas: float) -> float:
    """
    Calculate gas compressibility.

    Parameters
    ----------
    p : float
        Pressure [psia].
    t_r : float
        Temperature [°R].
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].

    Returns
    -------
    float
        Gas compressibility [1/psi].

    Source
    ------
    https://petroleumoffice.com/function/cg/ :contentReference[oaicite:6]{index=6}
    """
    ppc = 756.8 - 131.0 * sg_gas - 3.6 * sg_gas ** 2
    tpc = 169.2 + 349.5 * sg_gas - 74.0 * sg_gas ** 2
    tpr = t_r / tpc

    def z_f(p_val: float) -> float:
        return zfactor_dak(p_val / ppc, tpr)

    z = z_f(p)
    dp = max(1e-4, p * 1e-5)
    dz_dp = (z_f(p + dp) - z_f(p - dp)) / (2 * dp)
    return 1 / p - dz_dp / z


# Gas density
def gas_density(p: float, t_r: float, sg_gas: float, z_factor: float) -> float:
    """
    Calculate gas density.

    Parameters
    ----------
    p : float
        Pressure [psia].
    t_r : float
        Temperature [°R].
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    z_factor : float
        Gas compressibility factor (Z), dimensionless.

    Returns
    -------
    float
        Gas density [g/cc].

    Source
    ------
    https://petroleumoffice.com/function/gasdensity/ :contentReference[oaicite:7]{index=7}
    """
    return 0.016018463 * 28.97 * sg_gas * p / (z_factor * 10.7316 * t_r)
