import math
from math import exp, log

Units = {
    "Qi": "bbl/d",
    "Di": "1/d",
    "t": "d",
    "b": "безразмерный",
    "Dlim": "1/d",
    "n": "безразмерный",
    "Qi_intercept": "bbl/d",
    "Di_intercept": "1/d",
    "d_inf": "1/d",
    "time_buildup": "d",
    "time_plateau": "d",
    "Q_plateau": "bbl/d",
    "time_series": "d",
    "sg_gas": "безразмерный",
    "api": "°API",
    "r_s": "scf/STB",
    "t_f": "°F",
    "t_r": "°R",
    "bob": "bbl/STB",
    "co": "1/psi",
    "pb": "psia",
    "p": "psia",
    'Pb': 'psia',
    'Uob': 'cP',
    'rso': 'scf/STB',
    'rsob': 'scf/STB',
    'ppr': 'безразмерный',
    'tpr': 'безразмерный',
    'z_factor': 'безразмерный',
    'rswp': 'scf/STB',
    'rsw': 'scf/STB',
    'cs': 'g NaCl/L',
    'salinity': '%wt',
    'uw1': 'cP',
    "Ql": "bbl/d",
    "Ul": "cP",
    "Rho_l": "lb/ft³",
    "pipe_id": "in",
    "pipe_roughness": "безразмерный",
    "pipe_length": "ft",
    "pipe_angle": "deg",
    "P_in": "psia",
    "P_out": "psia",
    "Qg": "mscf/d",
    "Ug": "cP",
    "T": "°F",
    "IFTgl": "dyn/cm",
}


# temporary function for undefined functions in the tree
def stub(*args, kwargs):
    raise NotImplementedError("Эта функция ещё не реализована")


# functions that calculate rate
# FIXME:мы принимаем за правду, что входные данные корректны (проверяем только что float)
def exponential_decline_rate(Qi: float, Di: float, t: float) -> float:
    """
    Calculate the production rate at time t using the Arps exponential decline model.

    Parameters
    ----------
    Qi : float
        Initial production rate [L³/T].
    Di : float
        Initial decline rate [1/T].
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Production rate at time t.

    Source
    ------
    https://petroleumoffice.com/function/exponentialdeclinerate/
    """
    return Qi * exp(-Di * t)


def harmonic_decline_rate(Qi: float, Di: float, t: float) -> float:
    """
    Calculate the production rate at time t using the Arps harmonic decline model.

    Parameters
    ----------
    Qi : float
        Initial production rate [L³/T].
    Di : float
        Initial decline rate [1/T].
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Production rate at time t.

    Source
    ------
    https://petroleumoffice.com/function/harmonicdeclinerate/
    """
    return Qi / (1 + Di * t)


def hyperbolic_decline_rate(Qi: float, Di: float, b: float, t: float) -> float:
    """
    Calculate the production rate at time t using the Arps hyperbolic decline model.

    Parameters
    ----------
    Qi : float
        Initial production rate [L³/T].
    Di : float
        Initial decline rate [1/T].
    b : float
        Hyperbolic exponent (degree of curvature) [–].
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Production rate at time t.

    Source
    ------
    https://petroleumoffice.com/function/hyperbolicdeclinerate/
    """
    return Qi / (1 + b * Di * t) ** (1.0 / b)


def modified_hyperbolic_decline_rate(Qi: float, Dlim: float, Di: float, b: float, t: float) -> float:
    """
    Calculate the production rate at time t using the modified hyperbolic decline model,
    which transitions to exponential decline once the rate reaches the limit Dlim.

    Parameters
    ----------
    Qi : float
        Initial production rate [L³/T].
    Dlim : float
        Limiting decline rate at which the model switches to exponential decline [1/T].
    Di : float
        Initial decline rate [1/T].
    b : float
        Hyperbolic exponent (degree of curvature) [–].
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Production rate at time t.

    Source
    ------
    https://petroleumoffice.com/function/modifiedhyperbolicdeclinerate/
    """
    t_trans = (Di / Dlim - 1) / (b * Di)
    if t <= t_trans:
        return Qi / (1 + b * Di * t) ** (1.0 / b)
    q_trans = Qi / (1 + b * Di * t_trans) ** (1.0 / b)
    return q_trans * exp(-Dlim * (t - t_trans))


# FIXME: исправить эту функцию (что-то не то в источнике)
def ple_decline_rate(Qi_intercept: float, Di_intercept: float, d_inf: float, n: float, t: float) -> float:
    """
    Calculate the decline rate at time t using the Power Law Exponential (PLE) model.

    Parameters
    ----------
    Qi_intercept : float
        Rate “intercept” at t = 0 [L³/T].
    Di_intercept : float
        Decline constant defined by D₁/n, where D₁ is the decline constant at one time unit [1/T].
    d_inf : float
        Limiting decline rate as t → ∞ [1/T].
    n : float
        Time exponent (dimensionless).
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Decline rate at time t.

    Source
    ------
    https://petroleumoffice.com/function/powerlawexponentialdeclinerate/
    """
    return d_inf + (Qi_intercept - d_inf) * exp(-Di_intercept * t ** n)


def exponential_decline_cumulative(Qi: float, Di: float, t: float) -> float:
    """
    Calculate cumulative production at time t using the Arps exponential decline model.

    Parameters
    ----------
    Qi : float
        Initial production rate [L³/T].
    Di : float
        Decline rate [1/T].
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Cumulative production at time t [L³].

    Source
    ------
    https://petroleumoffice.com/function/exponentialdeclinecumulative/
    """
    return (Qi / Di) * (1 - exp(-Di * t))


def harmonic_decline_cumulative(Qi: float, Di: float, t: float) -> float:
    """
    Calculate cumulative production at time t using the Arps harmonic decline model.

    Parameters
    ----------
    Qi : float
        Initial production rate [L³/T].
    Di : float
        Decline rate [1/T].
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Cumulative production at time t [L³].

    Source
    ------
    https://petroleumoffice.com/function/harmonicdeclinecumulative/
    """
    return (Qi / Di) * log(1 + Di * t)


def hyperbolic_decline_cumulative(Qi: float, Di: float, b: float, t: float) -> float:
    """
    Calculate cumulative production at time t using the Arps hyperbolic decline model.

    Parameters
    ----------
    Qi : float
        Initial production rate [L³/T].
    Di : float
        Decline rate [1/T].
    b : float
        Hyperbolic exponent (dimensionless).
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Cumulative production at time t [L³].

    Source
    ------
    https://petroleumoffice.com/function/hyperbolicdeclinecumulative/
    """
    return (Qi / ((b - 1) * Di)) * (1 - (1 + b * Di * t) ** (1 - 1.0 / b))


def modified_hyperbolic_decline_cumulative(Qi: float, Di: float, Dlim: float, b: float, t: float) -> float:
    """
    Calculate cumulative production at time t using the modified hyperbolic decline model,
    which transitions to exponential decline once the decline rate reaches Dlim.

    Parameters
    ----------
    Qi : float
        Initial production rate [L³/T].
    Di : float
        Initial decline rate [1/T].
    Dlim : float
        Limiting decline rate at switch-over [1/T].
    b : float
        Hyperbolic exponent (dimensionless).
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Cumulative production at time t [L³].

    Source
    ------
    https://petroleumoffice.com/function/modifiedhyperbolicdeclinecumulative/
    """
    t_trans = (Di / Dlim - 1) / (b * Di)

    def N_hyp(tt: float) -> float:
        return (Qi / ((b - 1) * Di)) * ((1 + b * Di * tt) ** ((b - 1) / b) - 1)

    if t <= t_trans:
        return N_hyp(t)
    N1 = N_hyp(t_trans)
    q_trans = Qi / (1 + b * Di * t_trans) ** (1.0 / b)
    tail = q_trans / Dlim * (1 - exp(-Dlim * (t - t_trans)))
    return N1 + tail


def basic_field_profile(time_buildup: float, time_plateau: float, Q_plateau: float, Di: float, t: float) -> float:
    """
    Calculate the production rate at time t for a basic field production profile
    consisting of a linear buildup, constant plateau, and exponential decline.

    Parameters
    ----------
    time_buildup : float
        Duration of the linear buildup phase [T].
    time_plateau : float
        Duration of the constant-rate plateau phase [T].
    Q_plateau : float
        Production rate during the plateau [L³/T].
    Di : float
        Decline rate during the decline phase [1/T].
    t : float
        Time since start of production [T].

    Returns
    -------
    float
        Production rate at time t [L³/T].

    Source
    ------
    https://petroleumoffice.com/function/basicfieldprofile/
    """
    if t <= time_buildup:
        return Q_plateau * t / time_plateau
    elif t <= time_buildup + time_plateau:
        return Q_plateau
    else:
        return Q_plateau * exp(-Di * (t - time_buildup - time_plateau))


# FIXME: что-то не то с вводом, непонятно списки или нет
def combined_field_profile(time_series, profile, schedule, t):
    """
    Calculate the total field production at time t by summing individual well profiles
    according to their start times and drilling schedule.

    Parameters
    ----------
    time_series : float or list of float
        Start times for each well or group of wells [T].
    profile : float or list of float
        Production rate (or multiplier) for each well profile [L³/T].
    schedule : float or list of float
        Number of wells (or weighting) brought online at each corresponding time in time_series.
    t : float
        Evaluation time at which total field production is calculated [T].

    Returns
    -------
    float
        Total field production rate at time t [L³/T].

    Source
    ------
    https://petroleumoffice.com/function/combinedfieldprofile/
    """
    if not isinstance(time_series, (list, tuple)):
        time_series = [time_series]
    if not isinstance(profile, (list, tuple)):
        profile = [profile]
    if not isinstance(schedule, (list, tuple)):
        schedule = [schedule]

    total = 0.0
    for ts, pr, sc in zip(time_series, profile, schedule):
        if t >= ts:
            total += pr * sc
    return total


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

    a = c1 * sg_gas * exp((c3 * api) / (t_r))
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


# Pipe flow

# Single-phase fluid flow

# Liquid pipe flow

def reynolds_number_liquid(Ql, Rho_l, pipe_id, Ul) -> float:
    """
    Calculate the Reynolds number for liquid flow in a pipe.

    Parameters
    ----------
    Ql : float
        Liquid flow rate [bbl/day].
    Rho_l : float
        Liquid density [lb/ft³].
    pipe_id : float
        Pipe inner diameter [in].
    Ul : float
        Liquid viscosity [cP].

    Returns
    -------
    float
        Reynolds number (dimensionless).

    Source
    ------
    https://petroleumoffice.com/function/reynoldsnumberliquid/
    """
    q = (Ql * BBL_TO_FT3) / SEC_PER_DAY
    d = pipe_id / 12.0
    v = q / (math.pi * d ** 2 / 4.0)
    mu = Ul * CP_TO_LB_FTS
    return (Rho_l * v * d) / mu


def friction_pressure_drop_liquid(Ql, Ul, Rho_l,
                                  pipe_id, pipe_roughness, pipe_length) -> float:
    """
    Calculate frictional pressure drop for liquid flow in a pipe using the Fanning equation.

    Parameters
    ----------
    Ql : float
        Liquid flow rate [bbl/day].
    Ul : float
        Liquid viscosity [cP].
    Rho_l : float
        Liquid density [lb/ft³].
    pipe_id : float
        Pipe inner diameter [in].
    pipe_roughness : float
        Absolute roughness [ft].
    pipe_length : float
        Pipe length [ft].

    Returns
    -------
    float
        Frictional pressure drop [psi].

    Source
    ------
    https://petroleumoffice.com/function/frictionpressuredropliquid/
    """
    Re: float = reynolds_number_liquid(Ql, Rho_l, pipe_id, Ul)
    if Re < 2100.0:
        f = 16.0 / Re
    else:
        f = 0.25 / (math.log10(pipe_roughness / 3.7 + 5.74 / (Re ** 0.9))) ** 2 / 4.0
    q = Ql * BBL_TO_FT3 / SEC_PER_DAY
    d = pipe_id / 12.0
    v = q / (math.pi * d ** 2 / 4.0)
    return 2.0 * f * Rho_l * v ** 2 * pipe_length / d / GC / FT2_PER_IN2


def outlet_pipe_pressure_liquid(P_in: float, Ql: float, Ul: float, Rho_l: float,
                                pipe_id: float, pipe_roughness: float,
                                pipe_length: float, pipe_angle: float) -> float:
    """
    Calculate outlet pressure for liquid flow in a pipe, accounting for friction and elevation.

    Parameters
    ----------
    P_in : float
        Inlet pressure [psia].
    Ql : float
        Liquid flow rate [bbl/day].
    Ul : float
        Liquid viscosity [cP].
    Rho_l : float
        Liquid density [lb/ft³].
    pipe_id : float
        Pipe inner diameter [in].
    pipe_roughness : float
        Absolute roughness [ft].
    pipe_length : float
        Pipe length [ft].
    pipe_angle : float
        Pipe inclination angle from horizontal [deg].

    Returns
    -------
    float
        Outlet pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/outletpipepressureliquid/
    """
    dp_fric = friction_pressure_drop_liquid(Ql, Ul, Rho_l, pipe_id, pipe_roughness, pipe_length)
    dp_grav = Rho_l * GC * pipe_length * math.sin(math.radians(pipe_angle)) / FT2_PER_IN2
    return P_in - dp_fric - dp_grav


def potential_energy_pressure_drop_liquid(Rho_l: float,
                                          pipe_length: float,
                                          pipe_angle: float) -> float:
    """
    Calculate elevation-induced pressure drop for liquid flow in a pipe.

    Parameters
    ----------
    Rho_l : float
        Liquid density [lb/ft³].
    pipe_length : float
        Pipe length [ft].
    pipe_angle : float
        Pipe inclination angle from horizontal [deg].

    Returns
    -------
    float
        Pressure drop due to elevation change [psi].

    Source
    ------
    https://petroleumoffice.com/function/potentialenergypressuredropliquid/
    """
    return Rho_l * pipe_length * math.sin(math.radians(pipe_angle)) / FT2_PER_IN2


def inlet_pipe_pressure_liquid(P_out: float, Ql: float, Ul: float, Rho_l: float,
                               pipe_id: float, pipe_roughness: float,
                               pipe_length: float, pipe_angle: float) -> float:
    """
    Calculate inlet pressure for liquid flow in a pipe given outlet pressure.

    Parameters
    ----------
    P_out : float
        Outlet pressure [psia].
    Ql : float
        Liquid flow rate [bbl/day].
    Ul : float
        Liquid viscosity [cP].
    Rho_l : float
        Liquid density [lb/ft³].
    pipe_id : float
        Pipe inner diameter [in].
    pipe_roughness : float
        Absolute roughness [ft].
    pipe_length : float
        Pipe length [ft].
    pipe_angle : float
        Pipe inclination angle from horizontal [deg].

    Returns
    -------
    float
        Inlet pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/inletpipepressureliquid/
    """
    dp_fric = friction_pressure_drop_liquid(Ql, Ul, Rho_l,
                                            pipe_id, pipe_roughness, pipe_length)
    dp_grav = potential_energy_pressure_drop_liquid(Rho_l, pipe_length, pipe_angle)
    return P_out + dp_fric + dp_grav


def reynolds_number_gas(Qg: float, sg_gas: float, pipe_id: float, Ug: float) -> float:
    """
    Calculate the Reynolds number for gas flow in a pipe.

    Parameters
    ----------
    Qg : float
        Gas flow rate [Mscf/day].
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    pipe_id : float
        Pipe inner diameter [in].
    Ug : float
        Gas viscosity [cP].

    Returns
    -------
    float
        Reynolds number (dimensionless).

    Source
    ------
    https://petroleumoffice.com/function/reynoldsnumbergas/
    """
    q_std_cfs = Qg * SCF_PER_MSCF / SEC_PER_DAY
    d_ft = pipe_id / 12.0
    v_std = q_std_cfs / (math.pi * d_ft ** 2 / 4.0)
    rho_std = AIR_DENS_STP * sg_gas
    mu_lbfts = Ug * CP_TO_LB_FTS
    return rho_std * v_std * d_ft / mu_lbfts


# ─────────── вспомогательные функции для потока газа ────────────
def _gas_density(P: float, T: float, z: float, sg_gas: float) -> float:
    return AIR_DENS_STP * sg_gas * (P / 14.7) * (520.0 / (T + 460.0)) / z


def _gas_vol_rate(Qg: float, P: float, T: float, z: float) -> float:
    q_std = Qg * SCF_PER_MSCF
    return q_std * 520.0 / (T + 460.0) * (14.7 / (P * z)) / SEC_PER_DAY


def _fanning_friction(re: float, eps_rel: float) -> float:
    if re < 2100.0:
        return 16.0 / re
    fD = 0.25 / (math.log10(eps_rel / 3.7 + 5.74 / re ** 0.9)) ** 2
    return fD / 4.0


def _friction_dp_gas(Qg, P_ref, T, z_factor, sg_gas, Ug, pipe_id, eps_rel, L):
    rho = _gas_density(P_ref, T, z_factor, sg_gas)
    q = _gas_vol_rate(Qg, P_ref, T, z_factor)
    d = pipe_id / 12.0
    v = q / (math.pi * d ** 2 / 4.0)
    Re = rho * v * d / (Ug * CP_TO_LB_FTS)
    f = _fanning_friction(Re, eps_rel)
    return 2.0 * f * rho * v ** 2 * L / d / GC / FT2_PER_IN2


def _gravity_dp_gas(rho, L, angle):
    return rho * L * math.sin(math.radians(angle)) / FT2_PER_IN2


# --------------------Конец вспомогательных функций------------


def inlet_pipe_pressure_gas(Qg: float, p_out: float, pipe_length: float, pipe_id: float,
                            pipe_angle: float, pipe_roughness: float, z_factor: float,
                            T: float, sg_gas: float, Ug: float) -> float:
    """
    Calculate inlet pressure for gas flow in a pipe given outlet pressure, accounting for friction and elevation.

    Parameters
    ----------
    Qg : float
        Gas flow rate [Mscf/day].
    p_out : float
        Outlet pressure [psia].
    pipe_length : float
        Pipe length [ft].
    pipe_id : float
        Pipe inner diameter [in].
    pipe_angle : float
        Pipe inclination angle from horizontal [deg].
    pipe_roughness : float
        Absolute roughness [ft].
    z_factor : float
        Gas compressibility factor (Z), dimensionless.
    T : float
        Temperature [°R].
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    Ug : float
        Gas viscosity [cP].

    Returns
    -------
    float
        Inlet pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/inletpipepressuregas/
    """
    rho = _gas_density(p_out, T, z_factor, sg_gas)
    dp_fric = _friction_dp_gas(Qg, p_out, T, z_factor, sg_gas, Ug,
                               pipe_id, pipe_roughness, pipe_length)
    dp_grav = _gravity_dp_gas(rho, pipe_length, pipe_angle)
    return p_out + dp_fric + dp_grav


def outlet_pipe_pressure_gas(Qg: float, p_in: float, pipe_length: float, pipe_id: float,
                             pipe_angle: float, pipe_roughness: float, z_factor: float,
                             T: float, sg_gas: float, Ug: float) -> float:
    """
    Calculate outlet pressure for gas flow in a pipe, accounting for friction and elevation.

    Parameters
    ----------
    Qg : float
        Gas flow rate [Mscf/day].
    p_in : float
        Inlet pressure [psia].
    pipe_length : float
        Pipe length [ft].
    pipe_id : float
        Pipe inner diameter [in].
    pipe_angle : float
        Pipe inclination angle from horizontal [deg].
    pipe_roughness : float
        Absolute roughness [ft].
    z_factor : float
        Gas compressibility factor (Z), dimensionless.
    T : float
        Temperature [°R].
    sg_gas : float
        Gas specific gravity (air = 1.0) [–].
    Ug : float
        Gas viscosity [cP].

    Returns
    -------
    float
        Outlet pressure [psia].

    Source
    ------
    https://petroleumoffice.com/function/outletpipepressuregas/
    """
    rho = _gas_density(p_in, T, z_factor, sg_gas)
    dp_fric = _friction_dp_gas(Qg, p_in, T, z_factor, sg_gas, Ug,
                               pipe_id, pipe_roughness, pipe_length)
    dp_grav = _gravity_dp_gas(rho, pipe_length, pipe_angle)
    return p_in - dp_fric - dp_grav


# FIXME: нужно очеь много всего и непонятно где брать
# Multiphase Pipe Flow

# Hagedorn and Brown Correlation


def pressure_gradient_har_brown() -> float:
    return -1


def inlet_pressure_har_brown() -> float:
    return -1


def outlet_pressure_har_brown() -> float:
    return -1


# Beggs and Brill Correlation
def pressure_gradient_beggs_brill() -> float:
    return -1


def inlet_pressure_beggs_brill() -> float:
    return -1


def outlet_pressure_beggs_brill() -> float:
    return -1


# Gray Correaltion

def pressure_gradient_gray() -> float:
    return -1


def inlet_pressure_gray() -> float:
    return -1


def outlet_pressure_gray() -> float:
    return -1


# Well Flow Perfomance

# Oil Well Production

# Oil Pseudosteady State Flow

def flow_rate_pss_vogel(J, P_avg, Pwf, Pb):
    """
    Vogel inflow performance for pseudosteady-state flow (oil wells).

    Parameters
    ----------
    J : float
        Pseudosteady-state productivity index, [STB/(d·psi)].
    P_avg : float
        Average reservoir pressure, [psi].
    Pwf : float
        Bottom-hole flowing pressure, [psi].
    Pb : float
        Bubble-point pressure, [psi].

    Returns
    -------
    float
        Flow rate, [STB/d].
    """
    # Проверки
    if J <= 0:
        raise ValueError("J must be positive.")
    if P_avg <= 0 or Pb <= 0 or Pwf < 0:
        raise ValueError("Pressures must be positive.")

    if Pwf >= P_avg:
        return 0.0

    if Pwf >= Pb:
        return J * (P_avg - Pwf)

    q_b = J * (P_avg - Pb)

    f_b = 1 - 0.2 * (Pb / P_avg) - 0.8 * (Pb / P_avg) ** 2
    if f_b <= 0:
        raise ValueError("Check pressures: Vogel factor ≤ 0.")

    q_max = q_b / f_b

    # Vogel для Pwf < Pb
    return q_max * (1 - 0.2 * (Pwf / P_avg) - 0.8 * (Pwf / P_avg) ** 2)


def flow_rate_pss() -> float:
    return -1


def prod_index_hor_well_bo() -> float:
    return -1


def prod_index_hor_well_bo2() -> float:
    return -1


def prod_index_pss() -> float:
    return -1


def time_to_pss() -> float:
    return -1


# Oil steady state flow

def flow_rate_ss() -> float:
    return -1


def flow_rate_ss_vogel() -> float:
    return -1


def prod_index_hor_well_borisov() -> float:
    return -1


def prod_index_hor_well_grj() -> float:
    return -1


def prod_index_hor_well_joshi() -> float:
    return -1


def prod_index_hor_well_rd() -> float:
    return -1


def prod_index_ss() -> float:
    return -1


# Oil transient flow

def flow_rate_tf() -> float:
    return -1


def flow_rate_tf_vogel() -> float:
    return -1


def prod_index_tf() -> float:
    return -1


# Gas Well Production

# Gas Pseudosteady State Flow

def gas_flow_rate_pss() -> float:
    return -1


def gas_flow_rate_pss_non_darcy() -> float:
    return -1


def non_darcy_coefficient() -> float:
    return -1


def time_to_pss_gas() -> float:
    return -1


# Miscellaneous

# Drainage geometry

def drainage_area_hor_well_1() -> float:
    return -1


def drainage_area_hor_well_2() -> float:
    return -1


def drainage_radius() -> float:
    return -1


def effective_wellbore_radius() -> float:
    return -1


def equivalent_skin_factor() -> float:
    return -1


# Pressure transient analysis

# PTA models

def pw_vwihr() -> float:
    return -1


def pw_vwihrlcpb() -> float:
    return -1


def pw_vwihrlsfb() -> float:
    return -1


def pw_vwihrpcpb() -> float:
    return -1


def pw_vwihrpmb() -> float:
    return -1


def pw_vwihrpsfb() -> float:
    return -1


# PTA dimensionless models

def pd_lssihr() -> float:
    return -1


def pdw_vwihr() -> float:
    return -1


def pdw_vwihrlcpb() -> float:
    return -1


def pdw_vwihrlsfb() -> float:
    return -1


def pdw_vwihrpcpb() -> float:
    return -1


def pdw_vwihrpmb() -> float:
    return -1


def pdw_vwihrpsfb() -> float:
    return -1


# dimensionless

def pta_cd() -> float:
    return -1


def pta_ld() -> float:
    return -1


def pta_pd() -> float:
    return -1


def pta_rwd() -> float:
    return -1


def pta_td() -> float:
    return -1


# Special core analysis

# Relative permeability models

# Corey correlation

def krow_corey() -> float():
    return -1


def krw_corey() -> float():
    return -1


# LET correlation

def krow_let() -> float:
    return -1


def krw_let() -> float:
    return -1


# Honarpour correlation

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


# Rock compressibility

def cf_newman_l() -> float:
    return -1


def cf_newman_s() -> float:
    return -1


# Utilities

# Interpolation

def cubic_spline_differentiate() -> float:
    return -1


def cubic_spline_integrate() -> float:
    return -1


def cubic_spline_integrate_t1_t2() -> float:
    return -1


def cubic_spline_interpolate() -> float:
    return -1


def cubic_splines_intersection() -> float:
    return -1


def data_differentiate() -> float:
    return -1


def linear_spline_differentiate() -> float:
    return -1


def linear_spline_integrate() -> float:
    return -1


def linear_spline_integrate_t1_t2() -> float:
    return -1


def linear_spline_interpolate() -> float:
    return -1


def linear_splines_intersection() -> float:
    return -1


def step_interpolate() -> float:
    return -1


def proximal_interpolate() -> float:
    return -1


# Conversion

def api_2sg() -> float:
    return -1


def sg2_api() -> float:
    return -1


def unit_converter() -> float():
    return -1


# Special Functions

def exp_integral_ei() -> float:
    return -1


function_tree = {
    "Decline Curve Analysis": {
        "Decline Curves": {
            "Exponential": {
                "Rate": exponential_decline_rate,
                "Cumulative": exponential_decline_cumulative,
            },
            "Harmonic": {
                "Rate": harmonic_decline_rate,
                "Cumulative": harmonic_decline_cumulative,
            },
            "Hyperbolic": {
                "Rate": hyperbolic_decline_rate,
                "Cumulative": hyperbolic_decline_cumulative,
            },
            "Modified Hyperbolic": {
                "Rate": modified_hyperbolic_decline_rate,
                "Cumulative": modified_hyperbolic_decline_cumulative,
            },
            "PLE": {
                "Rate": ple_decline_rate,
            },
        },
        "Production Profiles": {
            "Basic Field Profile": basic_field_profile,
            "Combined Field Profile": combined_field_profile,
        },
    },
    "PVT": {
        "Oil PVT": {
            "Oil Bubble Point Pressure": {
                "Pbo AI Marhoun": pbo_al_marhoun,
                "Pbo Dokla Osman": pbo_dokla_osman,
                "Pbo Petrosky Farshad": pbo_petrosky_farshad,
                "Pbo Vasquez Beggs": pbo_vasquez_beggs,
                "Pbo Dindoruk Christman": pbo_dindoruk_christman,
                "Pbo Glaso": pbo_glaso,
                "Pbo Standing": pbo_standing
            },
            "Oil Formation Volume Factor": {
                "Bo Sat Al Marhoun 1988": bo_sat_al_marhoun_1988,
                "Bo Sat Glaso 1980": bo_sat_glaso_1980,
                "Bo Sat Standing 1988": bo_sat_standing_1947,
                "Bo U Sat": bo_u_sat,
                "Bo Sat Dindoruk Christman 2001": bo_sat_dindoruk_christman_2001,
                "Bo Sat Petrosky 1990": bo_sat_petrosky_1990,
                "Bo Sat Vasquez Beggs 1980": bo_sat_vasquez_beggs_1980
            },
            "Solution Gas-Oil Ratio": {
                "Rso Al Marhoun 1988": rso_al_marhoun_1988,
                "Rso Glaso 1980": rso_glaso_1980,
                "Rso Standing 1981": rso_standing_1981,
                "Rso Dindoruk Christman 2001": rso_dindoruk_christman_2001,
                "Rso Petrosky Farshad 1993": rso_petrosky_farshad_1993,
                "Rso Vasquez Beggs 1980": rso_vasquez_beggs_1980
            },
            "Oil Viscosity": {
                "Uod Egbogah 1983": uod_egbogah_1983,
                "Uo USat Vasquez Beggs 1980": uo_usat_vasquez_beggs_1980,
                "Uo Sat Beggs Robinson 1975": uo_sat_beggs_robinson_1975
            },
            "Oil Compressibility": {
                "Co Sat Villena Lanzi 1985": co_sat_villena_lanzi_1985,
                "Co USat Vasquez Beggs 1980": co_usat_vasquez_beggs_1980
            },
        },
        "Gas PVT": {
            "Z Factor": {
                "Zfactor Brill Beggs": zfactor_brill_beggs,
                "Zfactor Dak": zfactor_dak
            },
            "Pseudo Critical P and T": {
                "Ppc Standing": ppc_standing,
                "Tpc Standing": tpc_standing,
                "Ppc Sutton": ppc_sutton,
                "Tpc Sutton": tpc_sutton
            },
            "Gas Formation Volume Factor": {
                "Bg": bg
            },
            "Gas Viscosity": {
                "Ug LGE": ug_lge
            },
            "Gas Compressibility": {
                "Cg": cg
            },
            "Gas Density": {
                "Gas density": gas_density
            },
        },
        "Water PVT": {
            "Water Formation Volume Factor": {
                "Bw Mc Cain": bw_mc_cain
            },
            "Solution Gas-Water Ratio": {
                "Rsw Mc Cain": rsw_mc_cain,
                "Rswp Mc Cain": rswp_mc_cain
            },
            "Water Compressibility": {
                "Cw Sat Mc Cain": cw_sat_mc_cain,
                "Cw USat Osif": cw_usat_osif
            },
            "Water Viscosity": {
                "Uw Mc Cain": uw_mc_cain,
                "Uw1 Mc Cain": uw1_mc_cain
            },
        },
        "Interfacial Tension": {
            "IFTgo Abdul Majeed": iftgo_abdul_majeed,
            "IFTgo Baker Swerdloff": iftgo_baker_swerdloff,
        },
    },
    "Pipe Flow": {
        "Single-Phase Fluid Flow": {
            "Liquid Pipe Flow": {
                "Friction Pressure Drop Liquid": friction_pressure_drop_liquid,
                "Outlet Pipe Pressure Liquid": outlet_pipe_pressure_liquid,
                "Reynolds Number Liquid": reynolds_number_liquid,
                "Inlet Pipe Pressure Liquid": inlet_pipe_pressure_liquid,
                "Potential Energy Drop Pressure Liquid": potential_energy_pressure_drop_liquid
            },
            "Gas Pipe Flow": {
                "Inlet Pipe Pressure Gas": inlet_pipe_pressure_gas,
                "Reynolds Number Gas": reynolds_number_gas,
                "Outlet Pipe Pressure Gas": outlet_pipe_pressure_gas
            },
        },
        "Multiphase Pipe Flow": {
            "Hagedorn and Brown Correlation": {
                "Inlet Pressure Har Brown": inlet_pressure_har_brown,
                "Outlet Pressure Har Brown": outlet_pressure_har_brown,
                "Pressure Gradient Har Brown": pressure_gradient_har_brown
            },
            "Beggs and Brill Correlation": {
                "Inlet Pressure Beggs Brill": inlet_pressure_beggs_brill,
                "Outlet Pressure Beggs Brill": outlet_pressure_beggs_brill,
                "Pressure Gradient Beggs Brill": pressure_gradient_beggs_brill
            },
            "Gray Correlation": {
                "Inlet Pressure Gray": inlet_pressure_gray,
                "Outlet Pressure Gray": outlet_pressure_gray,
                "Pressure Gradient Gray": pressure_gradient_gray
            },
        },
    },
    "Well Flow Performance": {
        "Oil Well Production": {
            "Oil Pseudo-steady State Flow": {
                "Flow Rate PSS": flow_rate_pss,
                "Flow Rate PSS Vogel": flow_rate_pss_vogel,
                "Prod Index Hor Well BO": prod_index_hor_well_bo,
                "Prod Index Hor Well BO2": prod_index_hor_well_bo2,
                "Prod Index PSS": prod_index_pss,
                "Time To PSS": time_to_pss
            },
            "Oil Steady State Flow": {
                "Flow Rate SS": flow_rate_ss,
                "Flow Rate SS Vogel": flow_rate_ss_vogel,
                "Prod Index Hor Well Borisov": prod_index_hor_well_borisov,
                "Prod Index Hor Well GRJ": prod_index_hor_well_grj,
                "Prod Index Hor Well Joshi": prod_index_hor_well_joshi,
                "Prod Index Hor Well RD": prod_index_hor_well_rd,
                "Prod Index SS": prod_index_ss
            },
            "Oil Transient Flow": {
                "Flow Rate TF": flow_rate_tf,
                "Flow Rate TF Vogel": flow_rate_tf_vogel,
                "Prod Index TF": prod_index_tf
            },
        },
        "Gas Well Production": {
            "Gas Pseudo-steady State Flow": {
                "Gas Flow Rate PSS": gas_flow_rate_pss,
                "Gas Flow Rate PSS Non Darcy": gas_flow_rate_pss_non_darcy,
                "Non Darcy Coefficient": non_darcy_coefficient,
                "Time To PSS Gas": time_to_pss_gas
            }
        },
        "Miscellaneous": {
            "Drainage Geometry": {
                "Drainage Area Hor Well 1": drainage_area_hor_well_1,
                "Drainage Area Hor Well 2": drainage_area_hor_well_2,
                "Drainage Radius": drainage_radius,
                "Effective Wellbore Radius": effective_wellbore_radius,
                "Equivalent Skin Factor": equivalent_skin_factor
            },
        },
    },

    "Pressure Transient Analysis": {
        "PTA Models": {
            "Pw VWIHR": pw_vwihr,
            "Pw VWIHRLCPB": pw_vwihrlcpb,
            "Pw VWIHRLSFB": pw_vwihrlsfb,
            "Pw VWIHRPCPB": pw_vwihrpcpb,
            "Pw VWIHRPMB": pw_vwihrpmb,
            "Pw VWIHRPSFB": pw_vwihrpsfb
        },
        "PTA Dimensionless Models": {
            "Pd LSSIHR": pd_lssihr,
            "Pdw VWIHR": pdw_vwihr,
            "Pdw VWIHRLCPB": pdw_vwihrlcpb,
            "Pdw VWIHRLSFB": pdw_vwihrlsfb,
            "Pdw VWIHRPCPB": pdw_vwihrpcpb,
            "Pdw VWIHRPMB": pdw_vwihrpmb,
        },
        "Dimensionless": {
            "pta Cd": pta_cd,
            "pta Ld": pta_ld,
            "pta Pd": pta_pd,
            "pta Rwd": pta_rwd,
            "pta Td": pta_td
        },
    },
    "Special Core Analysis": {
        "Relative Permeability Models": {
            "Corey Correlation": {
                "Krow Corey": krow_corey,
                "Krw Corey": krw_corey
            },
            "LET Correlation": {
                "Krow LET": krow_let,
                "Krw LET": krw_let
            },
            "Honarpur Correlation": {
                "Krow Honarpour Carb InterWet": krow_honarpour_carb_inter_wet,
                "Krow Honarpour Sand InterWet": krow_honarpour_sand_inter_wet,
                "Krw Honarpour Carb InterWet": krw_honarpour_carb_inter_wet,
                "Krw Honarpour Sand InterWet": krw_honarpour_sand_inter_wet,
                "Krow Honarpour Carb WaterWet": krow_honarpour_carb_water_wet,
                "Krow Honarpour Sand WaterWet": krow_honarpour_sand_water_wet,
                "Krw Honarpour Carb WaterWet": krw_honarpour_carb_water_wet,
                "Krw Honarpour Sand WaterWet": krw_honarpour_sand_water_wet
            },
            "Ibrahim-Koederitz Correlation": {
                "Krcgl KGasCond": krcgl_k_gas_cond,
                "Krgl KGasCond": krgl_k_gas_cond,
                "Krgl KGasOilCarb": krgl_k_gas_oil_carb,
                "Krgl KGasOilSand": krgl_k_gas_oil_sand,
                "Krgw IKGasWater": krgw_ik_gas_water,
                "Krogl KGasOilCarb": krog_ik_gas_oil_carb,
                "Krogl KGasOilSand": krog_ik_gas_oil_sand,
                "Krowl KCarbOilWet": krowl_k_carb_oil_wet,
                "Krowl KCarbWaterWet": krowl_k_carb_water_wet,
                "Krowl KCarbInterWet": krowl_k_carb_inter_wet,
                "Krowl KCarbStrongWaterWet": krowl_k_carb_strong_water_wet,
                "Krowl KSandOilWet": krowl_k_sand_oil_wet,
                "Krowl KSandWaterWet": krowl_k_sand_water_wet,
                "Krowl KSandInterWet": krowl_k_sand_inter_wet,
                "Krowl KSandStrongWaterWet": krowl_k_sand_strong_water_wet,
                "Krw IKCarbOilWet": krwl_k_carb_oil_wet,
                "Krw IKCarbWaterWet": krwl_k_carb_water_wet,
                "Krw IKCarbInterWet": krwl_k_carb_inter_wet,
                "Krw IKCarbStrongWaterWet": krwl_k_carb_strong_water_wet,
                "Krw IKGasWater": krwl_k_gas_water,
                "Krw IKSandOilWet": krwl_k_sand_oil_wet,
                "Krw IKSandWaterWet": krwl_k_sand_water_wet,
                "Krw IKSandInterWet": krwl_k_sand_inter_wet,
                "Krw IKSandStrongWaterWet": krwl_k_sand_strong_water_wet,
            },
        },
        "Rock Compressibility": {
            "Cf Newman L": cf_newman_l,
            "Cf Newman S": cf_newman_s
        }
    },
    "Utilities": {
        "Interpolation": {
            "CubicSplineDifferentiate": cubic_spline_differentiate,
            "CubicSplineIntegrate": cubic_spline_integrate,
            "CubicSplineIntegrateT1T2": cubic_spline_integrate_t1_t2,
            "CubicSplineInterpolate": cubic_spline_interpolate,
            "CubicSplinesIntersection": cubic_splines_intersection,
            "DataDifferentiate": data_differentiate,
            "LinearSplineDifferentiate": linear_spline_differentiate,
            "LinearSplineIntegrate": linear_spline_integrate,
            "LinearSplineIntegrateT1T2": linear_spline_integrate_t1_t2,
            "LinearSplineInterpolate": linear_spline_interpolate,
            "LinearSplinesIntersection": linear_splines_intersection,
            "StepInterpolate": step_interpolate,
            "ProximalInterpolate": proximal_interpolate,
        },
        "Conversion": {
            "API 2SG": api_2sg,
            "SG2 API": sg2_api
        },
        "Special Functions": {
            "Exp Integral Ei": exp_integral_ei
        },
    },
}
