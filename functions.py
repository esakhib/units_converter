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
    "D_inf": "1/d",
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
    'Rso': 'scf/STB',
    'Rsob': 'scf/STB',
    'ppr': 'безразмерный',
    'tpr': 'безразмерный',
    'zfactor': 'безразмерный',
    'rswp': 'scf/STB',
    'rsw': 'scf/STB',
    'cs': 'g NaCl/L',
    'salinity': '%wt',
    'Uw1': 'cP',
}


# temporary function for undefined functions in the tree
def stub(*args, kwargs):
    raise NotImplementedError("Эта функция ещё не реализована")


# functions that calculate rate
# FIXME:мы принимаем за правду что входные данные корректны (проверяем только что float)
def exponential_decline_rate(Qi: float, Di: float, t: float) -> float:
    return Qi * exp(-Di * t)


def harmonic_decline_rate(Qi: float, Di: float, t: float) -> float:
    return Qi / (1 + Di * t)


def hyperbolic_decline_rate(Qi: float, Di: float, b: float, t: float) -> float:
    return Qi / (1 + b * Di * t) ** (1.0 / b)


def modified_hyperbolic_decline_rate(Qi: float, Dlim: float, Di: float, b: float, t: float) -> float:
    t_trans = (Di / Dlim - 1) / (b * Di)
    if t <= t_trans:
        return Qi / (1 + b * Di * t) ** (1.0 / b)
    q_trans = Qi / (1 + b * Di * t_trans) ** (1.0 / b)
    return q_trans * exp(-Dlim * (t - t_trans))


# FIXME: исправить эту функцию (что-то не то в источнике)
def ple_decline_rate(Qi_intercept: float, Di_intercept: float, D_inf: float, n: float, t: float) -> float:
    return D_inf + (Qi_intercept - D_inf) * exp(-Di_intercept * t ** n)


# cumulative functions

def exponential_decline_cumulative(Qi: float, Di: float, t: float) -> float:
    return (Qi / Di) * (1 - exp(-Di * t))


def harmonic_decline_cumulative(Qi: float, Di: float, t: float) -> float:
    return (Qi / Di) * log(1 + Di * t)


def hyperbolic_decline_cumulative(Qi: float, Di: float, b: float, t: float) -> float:
    return (Qi / ((b - 1) * Di)) * (1 - (1 + b * Di * t) ** (1 - 1.0 / b))


def modified_hyperbolic_decline_cumulative(Qi: float, Di: float, Dlim: float, b: float, t: float) -> float:
    t_trans = (Di / Dlim - 1) / (b * Di)

    def N_hyp(tt: float) -> float:
        return (Qi / ((b - 1) * Di)) * ((1 + b * Di * tt) ** ((b - 1) / b) - 1)

    if t <= t_trans:
        return N_hyp(t)
    N1 = N_hyp(t_trans)
    q_trans = Qi / (1 + b * Di * t_trans) ** (1.0 / b)
    tail = q_trans / Dlim * (1 - exp(-Dlim * (t - t_trans)))
    return N1 + tail


# production profiles

def basic_field_profile(time_buildup: float, time_plateau: float, Q_plateau: float, Di: float, t: float) -> float:
    if t <= time_buildup:
        return Q_plateau * t / time_plateau
    elif t <= time_buildup + time_plateau:
        return Q_plateau
    else:
        return Q_plateau * exp(-Di * (t - time_buildup - time_plateau))


# FIXME: что-то не то с вводом, непонятно списки или нет
def combined_field_profile(time_series, profile, schedule, t):
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


# Oil bubble point pressure

def pbo_al_marhoun(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
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
    rho_o = 141.5 / (131.5 + api)
    t_r = t_f + 460
    return 0.836386e4 * (r_s ** 0.724047) * (sg_gas ** -1.01049) * (rho_o ** 0.107991) * (t_r ** -0.952584)


# FIXME: тоже не сходится с оригиналом
def pbo_petrosky_farshad(sg_gas: float, api: float, r_s: float, t_f) -> float:
    X = 7.916e-4 * api ** 1.5410 - 4.561e-5 * t_f ** 1.3911
    pb = (r_s ** 1.73184) * (sg_gas ** (-0.8439)) * (10 ** X)
    return pb


def pbo_vasquez_beggs(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    t_r = t_f + 459.67
    if api <= 30.0:
        C1, C2, C3 = 0.0362, 1.0937, 25.7240
    else:
        C1, C2, C3 = 0.0178, 1.1870, 23.9310
    return (r_s / (C1 * sg_gas * math.exp(C3 * api / t_r))) ** (1.0 / C2)


# FIXME: тоже не сходится с оригиналом
def pbo_dindoruk_christman(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    A = (
            2.84459e-4 * t_f
            + 1.22523 * api
            - 0.272946 * math.log10(r_s)
            + 0.0842261 * sg_gas
            - 1.43e-6 * t_f ** 2
            + 6.74e-10 * api ** 2
            - 0.033833 * math.log10(sg_gas))

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
    X = (r_s ** 0.816) * (t_f ** 0.172) / (sg_gas * api ** 0.989)
    L = math.log10(X)
    log_pb = -0.30218 * (L ** 2) + 1.7447 * L + 1.7669
    return 10 ** log_pb


def pbo_standing(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    return 18.2 * ((r_s / sg_gas) ** 0.83 * 10 ** (0.00091 * t_f - 0.0125 * api) - 1.4)


# Oil formation volume factor

def bo_sat_al_marhoun_1988(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    gamma_o = 141.5 / (131.5 + api)

    a1 = 0.177342e-3
    a2 = 0.220163e-3
    a3 = 4.292580e-6
    a4 = 0.528707e-3

    return (1.0 + a1 * r_s + a2 * r_s * sg_gas / gamma_o + a3 * r_s * (t_f - 60.0) * (1.0 - gamma_o) + a4 * (
            t_f - 60.0))


# FIXME: есть небольшая погрешность из-за незнания точных коефициентов
def bo_sat_glaso_1980(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    gamma_o = 141.5 / (131.5 + api)
    F = r_s * (sg_gas / gamma_o) ** 0.526 + 0.968 * t_f
    logF = math.log10(F)
    A = -6.58611 + 2.91329 * logF - 0.27683 * (logF ** 2)
    return 1 + 10 ** A


def bo_sat_standing_1947(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    gamma_o = 141.5 / (131.5 + api)
    F = r_s * (sg_gas / gamma_o) ** 0.5 + 1.25 * t_f
    return 0.972 + 0.000147 * (F ** 1.175)


def bo_u_sat(bob: float, co: float, pb: float, p: float) -> float:
    return bob * math.exp(co * (pb - p))


# FIXME:нет коэфов
def bo_sat_dindoruk_christman_2001(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    return -1


# FIXME:нет коэфов
def bo_sat_petrosky_1990(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    return -1


def bo_sat_vasquez_beggs_1980(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
    if api <= 30.0:
        c1 = 4.677e-4
        c2 = 1.751e-5
        c3 = 1.811e-8
    else:
        c1 = 4.670e-4
        c2 = 1.100e-5
        c3 = 1.377e-9

    factor = api / sg_gas

    return 1.0 \
        + c1 * r_s \
        + c2 * (t_f - 60.0) * factor \
        + c3 * r_s * (t_f - 60.0) * factor


# solution gas_oil ratio

# FIXME: есть небольшая погрешность из-за незнания точных коефициентов
def rso_al_marhoun_1988(sg_gas: float, api: float, p: float, t_f: float) -> float:
    gamma_o = 141.5 / (131.5 + api)

    a1 = 1.4903e3
    a2 = 2.626
    a3 = 1.3984
    a4 = -4.3963
    a5 = -1.86

    return a1 * (sg_gas ** a2) * (p ** a3) * (gamma_o ** a4) * ((t_f + 460.0) ** a5)


# FIXME: нет коэфов
def rso_glaso_1980(sg_gas: float, api: float, p: float, t_f: float) -> float:
    p_star = 10 ** (2.8869 - math.sqrt(14.1811 - 3.3093 * math.log10(p)))
    return (api / (t_f + 460.0)) ** 0.989 * sg_gas ** 0.172 * p_star ** 1.2255


# FIXME: нет коэфов
def rso_standing_1981(sg_gas: float, api: float, p: float, t_f: float) -> float:
    x = 0.0125 * api - 0.00091 * (t_f - 460.0)
    term = (p / 18.2) + 1.4
    return sg_gas * (term * 10 ** x) ** (1 / 0.83)


# FIXME: нет коэфов
def rso_dindoruk_christman_2001(sg_gas: float, api: float, p: float, t_f: float) -> float:
    x = 7.916e-4 * api ** 1.5410 - 4.561e-5 * t_f ** 1.3911
    return ((p / 112.727 + 12.340) * sg_gas ** 0.8439 * 10 ** x) ** 1.787


def rso_petrosky_farshad_1993(sg_gas: float, api: float, p: float, t_f: float) -> float:
    x = 7.916e-4 * api ** 1.5410 - 4.561e-5 * t_f ** 1.3911
    return ((p / 112.727 + 12.340) * sg_gas ** 0.8439 * 10 ** x) ** 1.73184


def rso_vasquez_beggs_1980(sg_gas: float, api: float, p: float, t_f: float) -> float:
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
    if api <= 0 or t_f <= 0:
        raise ValueError("API и температура должны быть положительными.")
    x = 1.8653 - 0.025086 * api - 0.5644 * math.log10(t_f)
    return 10.0 ** (10.0 ** x) - 1.0


def uo_usat_vasquez_beggs_1980(p: float, pb: float, uob: float) -> float:
    m = 2.6 * p ** 1.187 * math.exp(-11.513 - 8.98e-5 * p)
    return uob * (p / pb) ** m


def uo_sat_beggs_robinson_1975(rso: float, uod: float) -> float:
    a = 10.715 * (rso + 100) ** -0.515
    b = 5.44 * (rso + 150) ** -0.338
    return a * uod ** b


# oil compressebility


def co_sat_villena_lanzi_1985(p: float, pb: float, t_f: float, rsob: float, api: float) -> float:
    return math.exp(
        -0.664
        - 1.430 * math.log(p)
        - 0.395 * math.log(pb)
        + 0.390 * math.log(t_f)
        + 0.455 * math.log(rsob)
        + 0.262 * math.log(api)
    )


def co_usat_vasquez_beggs_1980(rsob: float, sg_gas: float, api: float, t_f: float, p: float) -> float:
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
    A = 1.39 * math.sqrt(tpr - 0.92) - 0.36 * tpr - 0.101
    B = (0.62 - 0.23 * tpr) * ppr + ((0.066 / tpr) - 0.037) * ppr ** 2 + 0.32 * ppr ** 6
    C = 0.132 - 0.32 * math.log10(tpr)
    D = 10 ** (0.3106 - 0.49 * tpr + 0.1824 * tpr ** 2)
    exp_term = math.exp(-B) if B < 700 else 0.0
    return A + (1 - A) * exp_term + C * ppr ** D


def zfactor_dak(ppr: float, tpr: float) -> float:
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
    return 706.0 - 51.7 * sg_gas - 11.1 * sg_gas ** 2


def tpc_standing(sg_gas: float) -> float:
    return 187.0 + 330.0 * sg_gas - 71.5 * sg_gas ** 2


def ppc_sutton(sg_gas: float) -> float:
    return 756.8 - 131.0 * sg_gas - 3.6 * sg_gas ** 2


def tpc_sutton(sg_gas: float) -> float:
    return 169.2 + 349.5 * sg_gas - 74.0 * sg_gas ** 2


# Gas formation volume factor

def bg(p: float, t_r: float, zfactor: float) -> float:
    return 0.02827 * zfactor * t_r / p


# gas viscosity

def ug_lge(zfactor: float, sg_gas: float, p: float, t_r: float) -> float:
    m = 28.967 * sg_gas
    k = (9.4 + 0.02 * m) * t_r ** 1.5 / (209 + 19 * m + t_r)
    x = 3.5 + 986 / t_r + 0.01 * m
    y = 2.4 - 0.2 * x
    rho = 28.967 * sg_gas * p / (zfactor * 10.7316 * t_r)
    return 1.0e-4 * k * math.exp(x * (rho / 62.4) ** y)


# gas compressibility

def cg(p: float, t_r: float, sg_gas: float) -> float:
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

def gas_density(p: float, t_r: float, sg_gas: float, zfactor: float) -> float:
    return 0.016018463 * 28.97 * sg_gas * p / (zfactor * 10.7316 * t_r)


# Water PVT

# Water formation volume factor

def bw_mc_cain(p: float, t_f: float) -> float:
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
    a = 8.15839 - 6.12265e-2 * t_f + 1.91663e-4 * t_f ** 2 - 2.1654e-7 * t_f ** 3
    b = 1.01021e-2 - 7.44241e-5 * t_f + 3.05553e-7 * t_f ** 2 - 2.94883e-10 * t_f ** 3
    c = -(9.02505 - 0.130237 * t_f + 8.53425e-4 * t_f ** 2
          - 2.34122e-6 * t_f ** 3 + 2.37049e-9 * t_f ** 4) * 1e-7
    return a + b * p + c * p ** 2


def rsw_mc_cain(rswp: float, salinity: float, t_f: float) -> float:
    return rswp * 10 ** (-0.0840655 * salinity * t_f ** -0.285854)


# Water compressibility
# FIXME: присутствует погрешность в обоих функциях раздела
def cw_sat_mc_cain(p: float, t_f: float, cs: float) -> float:
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
    s = salinity
    A = 109.574 - 8.40564 * s + 0.313314 * s ** 2 + 8.72213e-3 * s ** 3
    B = -1.12166 + 2.63951e-2 * s - 6.79461e-4 * s ** 2 \
        - 5.47119e-5 * s ** 3 + 1.55586e-6 * s ** 4
    return A * t_f ** B


def uw_mc_cain(p: float, uw1: float) -> float:
    return uw1 * (0.9994 + 4.0295e-5 * p + 3.1062e-9 * p ** 2)

#Interfacial Tension

def iftgo_abdul_majeed(api: float, t_f: float, rso: float) -> float:
    sigma_od = (1.17013 - 1.694e-3 * t_f) * (38.085 - 0.259 * api)
    ratio = 0.056379 + 0.94362 * math.exp(-3.8491e-3 * rso)
    return sigma_od * ratio


def iftgo_baker_swerdloff(api: float, t_f: float, p: float) -> float:
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
            "Liquid Pipe Flow": stub,
            "Gas Pipe Flow": stub,
        },
        "Multiphase Pipe Flow": {
            "Hagedorn and Brown": stub,
            "Beggs and Brill": stub,
            "Gray Correlation": stub,
        },
    },
    "Well Flow Performance": {
        "Oil Well Production": {
            "Oil Pseudo-steady State Flow": stub,
            "Oil Steady State Flow": stub,
            "Oil Transient Flow": stub,
        },
        "Gas Well Production": {
            "Gas Pseudo-steady State Flow": stub,
        },
        "Miscellaneous": {
            "Drainage Geometry": stub,
        },
    },

    "Pressure Transient Analysis": {
        "PTA Models": stub,
        "PTA Dimensionless Models": stub,
        "Dimensionless": stub,
    },
    "Special Core Analysis": {
        "Relative Permeability Models": stub,
        "Corey Correlation": stub,
        "LET Correlation": stub,
        "Honarpur Correlation": stub,
        "Ibrahim-Koederitz Correlation": stub,
        "Rock Compressibility": stub,
    },
    "Utilities": {
        "Interpolation": stub,
        "Conversion": stub,
        "Special Functions": stub,
    },
}
