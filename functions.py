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
    "t_r": "°F",
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

def pbo_ai_marhoun(sg_gas: float, api: float, r_s: float, t_f: float) -> float:
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


# TODO: дописать все оставшиеся функции и их единицы измререния соответсвенно (units)

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
                "Pbo AI Marhoun": pbo_ai_marhoun,
                "Pbo Dokla Osman": pbo_dokla_osman,
                "Pbo Petrosky Farshad": pbo_petrosky_farshad,
                "Pbo Vasquez Beggs": pbo_vasquez_beggs,
                "Pbo Dindoruk Christman": pbo_dindoruk_christman,
                "Pbo Glaso": stub,
                "Pbo Standing": stub
            },
            "Oil Formation Volume Factor": stub,
            "Factor": stub,
            "Solution Gas-Oil Ratio": stub,
            "Oil Viscosity": stub,
            "Oil Compressibility": stub,
        },
        "Gas PVT": {
            "Z Factor": stub,
            "Pseudo Critical P and T": stub,
            "Gas Formation Volume Factor": stub,
            "Gas Viscosity": stub,
            "Gas Compressibility": stub,
            "Gas Density": stub,
        },
        "Water PVT": {
            "Water Formation Volume Factor": stub,
            "Solution Gas-Water Ratio": stub,
            "Water Compressibility": stub,
            "Water Viscosity": stub,
            "Interfacial Tension": stub,
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
