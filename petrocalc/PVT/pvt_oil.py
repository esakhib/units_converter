from __future__ import annotations

import math

__all__ = [
    "pbo_al_marhoun",
    "pbo_dokla_osman",
    "pbo_petrosky_farshad",
    "pbo_vasquez_beggs",
    "pbo_dindoruk_christman",
    "pbo_glaso",
    "pbo_standing",
    "bo_sat_al_marhoun_1988",
    "bo_sat_glaso_1980",
    "bo_sat_standing_1947",
    "bo_u_sat",
    "bo_sat_dindoruk_christman_2001",
    "bo_sat_petrosky_1990",
    "bo_sat_vasquez_beggs_1980",
    "rso_al_marhoun_1988",
    "rso_glaso_1980",
    "rso_standing_1981",
    "rso_dindoruk_christman_2001",
    "rso_petrosky_farshad_1993",
    "rso_vasquez_beggs_1980",
    "uod_egbogah_1983",
    "uo_usat_vasquez_beggs_1980",
    "uo_sat_beggs_robinson_1975",
    "co_sat_villena_lanzi_1985",
    "co_usat_vasquez_beggs_1980",
]


def pbo_al_marhoun(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Estimate the oil bubble-point pressure using the Al-Marhoun correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    r_s : float
        Solution gas-oil ratio at bubble point [scf/STB].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Bubble-point pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/pboalmarhoun/
    """
    rho_o = 141.5 / (131.5 + api)
    t_r = t_f + 459.67

    a1 = 5.38088e-3
    a2 = 0.7151
    a3 = -1.8778
    a4 = 3.1437
    a5 = 1.32657

    pb = a1 * (r_s ** a2) * (sg_gas ** a3) * (rho_o ** a4) * (t_r ** a5)
    return pb


def pbo_dokla_osman(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Estimate the oil bubble-point pressure using the Dokla & Osman correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    r_s : float
        Solution gas-oil ratio at bubble point [scf/STB].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Bubble-point pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/pbodoklaosman/
    """
    rho_o = 141.5 / (131.5 + api)
    t_r = t_f + 460
    return 0.836386e4 * (r_s ** 0.724047) * (sg_gas ** -1.01049) * (rho_o ** 0.107991) * (t_r ** -0.952584)


# FIXME: тоже не сходится с оригиналом
def pbo_petrosky_farshad(sg_gas: float, api: float, r_s: float, t_f) -> float:
    """
    Estimate the oil bubble-point pressure using the Petrosky & Farshad correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    r_s : float
        Solution gas–oil ratio at bubble point [scf/STB].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Bubble-point pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/pbopetroskyfarshad/ :contentReference[oaicite:0]{index=0}
    """
    X = 7.916e-4 * api ** 1.5410 - 4.561e-5 * t_f ** 1.3911
    pb = (r_s ** 1.73184) * (sg_gas ** (-0.8439)) * (10 ** X)
    return pb


def pbo_vasquez_beggs(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Estimate the oil bubble-point pressure using the Vasquez & Beggs correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    r_s : float
        Solution gas–oil ratio at bubble point [scf/STB].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Bubble-point pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/pbovasquezbeggs/ :contentReference[oaicite:1]{index=1}
    """
    t_r = t_f + 459.67
    if api <= 30.0:
        C1, C2, C3 = 0.0362, 1.0937, 25.7240
    else:
        C1, C2, C3 = 0.0178, 1.1870, 23.9310
    return (r_s / (C1 * sg_gas * math.exp(C3 * api / t_r))) ** (1.0 / C2)


# FIXME: тоже не сходится с оригиналом
def pbo_dindoruk_christman(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Estimate the oil bubble-point pressure using the Dindoruk & Christman correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0).
    api : float
        Oil API gravity (°API).
    r_s : float
        Solution gas–oil ratio at bubble point (scf/STB).
    t_f : float
        Reservoir temperature (°F).

    Returns
    -------
    float
        Bubble-point pressure (psia).

    Source
    ------
    https://petroleumoffice.com/function/pbodindorukchristman/
    """
    A = (
            2.84459e-4 * t_f
            + 1.22523 * api
            - 0.272946 * math.log10(r_s)
            + 0.0842261 * sg_gas
            - 1.43e-6 * t_f ** 2
            + 6.74e-10 * api ** 2
            - 0.033833 * math.log10(sg_gas)
    )

    log_pb = (
            1.22145
            + 1.37051 * math.log10(r_s)
            + 1.86998 * math.log10(sg_gas)
            - 0.011688 * sg_gas
            + A
    )

    return 10 ** log_pb


# FIXME: есть небольшая погрешность из-за незнания точных коефициентов
def pbo_glaso(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Estimate the oil bubble-point pressure using the Glaso correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0).
    api : float
        Oil API gravity (°API).
    r_s : float
        Solution gas–oil ratio at bubble point (scf/STB).
    t_f : float
        Reservoir temperature (°F).

    Returns
    -------
    float
        Bubble-point pressure (psia).

    Source
    ------
    https://petroleumoffice.com/function/pboglaso/
    """
    X = (r_s ** 0.816) * (t_f ** 0.172) / (sg_gas * api ** 0.989)
    L = math.log10(X)
    log_pb = -0.30218 * (L ** 2) + 1.7447 * L + 1.7669
    return 10 ** log_pb


def pbo_standing(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Estimate the oil bubble-point pressure using the Standing correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0).
    api : float
        Oil API gravity (°API).
    r_s : float
        Solution gas–oil ratio at bubble point (scf/STB).
    t_f : float
        Reservoir temperature (°F).

    Returns
    -------
    float
        Bubble-point pressure (psia).

    Source
    ------
    https://petroleumoffice.com/function/pbostanding/
    """
    return 18.2 * ((r_s / sg_gas) ** 0.83 * 10 ** (0.00091 * t_f - 0.0125 * api) - 1.4)


def bo_sat_al_marhoun_1988(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Calculate the saturated oil formation volume factor using the Al-Marhoun (1988) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0).
    api : float
        Oil API gravity (°API).
    r_s : float
        Solution gas–oil ratio at bubble point (scf/STB).
    t_f : float
        Reservoir temperature (°F).

    Returns
    -------
    float
        Oil formation volume factor at saturation (bbl/STB).

    Source
    ------
    https://petroleumoffice.com/function/bosatalmarhoun1988/
    """
    gamma_o = 141.5 / (131.5 + api)

    a1 = 0.177342e-3
    a2 = 0.220163e-3
    a3 = 4.292580e-6
    a4 = 0.528707e-3

    return (
            1.0
            + a1 * r_s
            + a2 * r_s * sg_gas / gamma_o
            + a3 * r_s * (t_f - 60.0) * (1.0 - gamma_o)
            + a4 * (t_f - 60.0)
    )


# FIXME: есть небольшая погрешность из-за незнания точных коефициентов
def bo_sat_glaso_1980(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Calculate the saturated oil formation volume factor using the Glaso (1980) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0).
    api : float
        Oil API gravity (°API).
    r_s : float
        Solution gas–oil ratio at bubble point (scf/STB).
    t_f : float
        Reservoir temperature (°F).

    Returns
    -------
    float
        Oil formation volume factor at saturation (bbl/STB).

    Source
    ------
    https://petroleumoffice.com/function/bosatglaso1980/
    """
    gamma_o = 141.5 / (131.5 + api)
    F = r_s * (sg_gas / gamma_o) ** 0.526 + 0.968 * t_f
    logF = math.log10(F)
    A = -6.58611 + 2.91329 * logF - 0.27683 * (logF ** 2)
    return 1 + 10 ** A


def bo_sat_standing_1947(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Calculate the saturated oil formation volume factor using the Standing (1947) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0).
    api : float
        Oil API gravity (°API).
    r_s : float
        Solution gas–oil ratio at bubble point (scf/STB).
    t_f : float
        Reservoir temperature (°F).

    Returns
    -------
    float
        Oil formation volume factor at saturation (bbl/STB).

    Source
    ------
    https://petroleumoffice.com/function/bosatstanding1947/
    """
    gamma_o = 141.5 / (131.5 + api)
    F = r_s * (sg_gas / gamma_o) ** 0.5 + 1.25 * t_f
    return 0.972 + 0.000147 * (F ** 1.175)


def bo_u_sat(bob: float, co: float, pb: float, p: float) -> float:
    """
    Calculate the oil formation volume factor above bubble-point pressure.

    Parameters
    ----------
    bob : float
        Oil formation volume factor at bubble point (bbl/STB).
    co : float
        Oil compressibility (1/psi).
    pb : float
        Bubble-point pressure (psia).
    p : float
        Current reservoir pressure (psia).

    Returns
    -------
    float
        Oil formation volume factor at pressure p (bbl/STB).

    Source
    ------
    https://petroleumoffice.com/function/bousat/
    """
    return bob * math.exp(co * (pb - p))


# FIXME:нет коэфов
def bo_sat_dindoruk_christman_2001(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Calculate the saturated oil formation volume factor using the Dindoruk & Christman (2001) correlation.
    Note: Coefficients for this correlation are currently not available.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    r_s : float
        Solution gas–oil ratio at bubble point [scf/STB].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Oil formation volume factor at saturation [bbl/STB] (placeholder value).

    Source
    ------
    https://petroleumoffice.com/function/bosatdindorukchristman2001/
    """
    return -1


# FIXME:нет коэфов
def bo_sat_petrosky_1990(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Calculate the saturated oil formation volume factor using the Petrosky (1990) correlation.
    Note: Coefficients for this correlation are currently not available.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    r_s : float
        Solution gas–oil ratio at bubble point [scf/STB].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Oil formation volume factor at saturation [bbl/STB] (placeholder value).

    Source
    ------
    https://petroleumoffice.com/function/bosatpetrosky1990/
    """
    return -1


def bo_sat_vasquez_beggs_1980(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    """
    Calculate the saturated oil formation volume factor using the Vasquez & Beggs (1980) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    r_s : float
        Solution gas–oil ratio at bubble point [scf/STB].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Oil formation volume factor at saturation [bbl/STB].

    Source
    ------
    https://petroleumoffice.com/function/bosatvasquezbeggs1980/
    """
    if api <= 30.0:
        c1 = 4.677e-4
        c2 = 1.751e-5
        c3 = 1.811e-8
    else:
        c1 = 4.670e-4
        c2 = 1.100e-5
        c3 = 1.377e-9

    factor = api / sg_gas

    return (
            1.0
            + c1 * r_s
            + c2 * (t_f - 60.0) * factor
            + c3 * r_s * (t_f - 60.0) * factor
    )


# solution gas_oil ratio

# FIXME: есть небольшая погрешность из-за незнания точных коефициентов
def rso_al_marhoun_1988(sg_gas: float, api: float, p: float, t_f: float) -> float:
    """
    Estimate the solution gas–oil ratio at pressure p using the Al-Marhoun (1988) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    p : float
        Reservoir pressure [psia].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Solution gas–oil ratio [scf/STB].

    Source
    ------
    https://petroleumoffice.com/function/rsoalmarhoun1988/
    """
    gamma_o = 141.5 / (131.5 + api)

    a1 = 1.4903e3
    a2 = 2.626
    a3 = 1.3984
    a4 = -4.3963
    a5 = -1.86

    return a1 * (sg_gas ** a2) * (p ** a3) * (gamma_o ** a4) * ((t_f + 460.0) ** a5)


# FIXME: нет коэфов
def rso_glaso_1980(sg_gas: float, api: float, p: float, t_f: float) -> float:
    """
    Estimate the solution gas–oil ratio at pressure p using the Glaso (1980) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    p : float
        Reservoir pressure [psia].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Solution gas–oil ratio [scf/STB].

    Source
    ------
    https://petroleumoffice.com/function/rsoglaso1980/
    """
    p_star = 10 ** (2.8869 - math.sqrt(14.1811 - 3.3093 * math.log10(p)))
    return (api / (t_f + 460.0)) ** 0.989 * sg_gas ** 0.172 * p_star ** 1.2255


# FIXME: нет коэфов
def rso_standing_1981(sg_gas: float, api: float, p: float, t_f: float) -> float:
    """
    Estimate the solution gas–oil ratio at pressure p using the Standing (1981) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    p : float
        Reservoir pressure [psia].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Solution gas–oil ratio [scf/STB].

    Source
    ------
    https://petroleumoffice.com/function/rsostanding1981/
    """
    x = 0.0125 * api - 0.00091 * (t_f - 460.0)
    term = (p / 18.2) + 1.4
    return sg_gas * (term * 10 ** x) ** (1 / 0.83)


# FIXME: нет коэфов
def rso_dindoruk_christman_2001(sg_gas: float, api: float, p: float, t_f: float) -> float:
    """
    Estimate the solution gas–oil ratio at pressure p using the Dindoruk & Christman (2001) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    p : float
        Reservoir pressure [psia].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Solution gas–oil ratio [scf/STB].

    Source
    ------
    https://petroleumoffice.com/function/rsodindorukchristman2001/
    """
    x = 7.916e-4 * api ** 1.5410 - 4.561e-5 * t_f ** 1.3911
    return ((p / 112.727 + 12.340) * sg_gas ** 0.8439 * 10 ** x) ** 1.787


def rso_petrosky_farshad_1993(sg_gas: float, api: float, p: float, t_f: float) -> float:
    """
    Estimate the solution gas–oil ratio at pressure p using the Petrosky & Farshad (1993) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    p : float
        Reservoir pressure [psia].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Solution gas–oil ratio [scf/STB].

    Source
    ------
    https://petroleumoffice.com/function/rsopetroskyfarshad1993/
    """
    x = 7.916e-4 * api ** 1.5410 - 4.561e-5 * t_f ** 1.3911
    return ((p / 112.727 + 12.340) * sg_gas ** 0.8439 * 10 ** x) ** 1.73184


def rso_vasquez_beggs_1980(sg_gas: float, api: float, p: float, t_f: float) -> float:
    """
    Estimate the solution gas–oil ratio at pressure p using the Vasquez & Beggs (1980) correlation.

    Parameters
    ----------
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    p : float
        Reservoir pressure [psia].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Solution gas–oil ratio [scf/STB].

    Source
    ------
    https://petroleumoffice.com/function/rsovasquezbeggs1980/
    """
    t_r = t_f + 459.67

    if api <= 30:
        c1 = 0.0362
        c2 = 1.0937
        c3 = 25.724
    else:
        c1 = 0.0178
        c2 = 1.187
        c3 = 23.931

    a = c1 * sg_gas * math.exp((c3 * api) / (t_r))
    rso = a * (p ** c2)

    return rso


# Oil viscosity

def uod_egbogah_1983(api: float, t_f: float) -> float:
    """
    Calculate dead (solution-free) oil viscosity using the Egbogah (1983) correlation.

    Parameters
    ----------
    api : float
        Oil API gravity [°API].
    t_f : float
        Reservoir temperature [°F].

    Returns
    -------
    float
        Dead oil viscosity [cP].

    Raises
    ------
    ValueError
        If api or t_f is non-positive.

    Source
    ------
    https://petroleumoffice.com/function/uodegbogah1983/
    """
    if api <= 0 or t_f <= 0:
        raise ValueError("API и температура должны быть положительными.")
    x = 1.8653 - 0.025086 * api - 0.5644 * math.log10(t_f)
    return 10.0 ** (10.0 ** x) - 1.0


def uo_usat_vasquez_beggs_1980(p: float, pb: float, uob: float) -> float:
    """
    Calculate undersaturated oil viscosity using the Vasquez & Beggs (1980) correlation.

    Parameters
    ----------
    p : float
        Current reservoir pressure [psia].
    pb : float
        Bubble-point pressure [psia].
    uob : float
        Oil viscosity at bubble-point pressure [cP].

    Returns
    -------
    float
        Undersaturated oil viscosity [cP].

    Source
    ------
    https://petroleumoffice.com/function/uousatvasquezbeggs1980/
    """
    m = 2.6 * p ** 1.187 * math.exp(-11.513 - 8.98e-5 * p)
    return uob * (p / pb) ** m


def uo_sat_beggs_robinson_1975(rso: float, uod: float) -> float:
    """
    Calculate saturated oil viscosity using the Beggs & Robinson (1975) correlation.

    Parameters
    ----------
    rso : float
        Solution gas–oil ratio [scf/STB].
    uod : float
        Dead oil viscosity [cP].

    Returns
    -------
    float
        Saturated oil viscosity [cP].

    Source
    ------
    https://petroleumoffice.com/function/uosatbeggsrobinson1975/
    """
    a = 10.715 * (rso + 100) ** -0.515
    b = 5.44 * (rso + 150) ** -0.338
    return a * uod ** b


# oil compressebility

def co_sat_villena_lanzi_1985(p: float, pb: float, t_f: float, rsob: float, api: float) -> float:
    """
    Calculate oil compressibility at saturation using the Villena & Lanzi (1985) correlation.

    Parameters
    ----------
    p : float
        Current reservoir pressure [psia].
    pb : float
        Bubble-point pressure [psia].
    t_f : float
        Reservoir temperature [°F].
    rsob : float
        Solution gas–oil ratio at bubble-point [scf/STB].
    api : float
        Oil API gravity [°API].

    Returns
    -------
    float
        Oil compressibility at saturation [1/psi].

    Source
    ------
    https://petroleumoffice.com/function/cosatvillenalanzi1985/
    """
    return math.exp(
        -0.664
        - 1.430 * math.log(p)
        - 0.395 * math.log(pb)
        + 0.390 * math.log(t_f)
        + 0.455 * math.log(rsob)
        + 0.262 * math.log(api)
    )


def co_usat_vasquez_beggs_1980(rsob: float, sg_gas: float, api: float, t_f: float, p: float) -> float:
    """
    Calculate undersaturated oil compressibility using the Vasquez & Beggs (1980) correlation.

    Parameters
    ----------
    rsob : float
        Solution gas–oil ratio at bubble-point [scf/STB].
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    api : float
        Oil API gravity [°API].
    t_f : float
        Reservoir temperature [°F].
    p : float
        Current reservoir pressure [psia].

    Returns
    -------
    float
        Undersaturated oil compressibility [1/psi].

    Source
    ------
    https://petroleumoffice.com/function/cousatvasquezbeggs1980/
    """
    return (
            -1433
            + 5 * rsob
            + 17.2 * t_f
            - 1180 * sg_gas
            + 12.61 * api
    ) / (1e5 * p)
