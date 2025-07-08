from __future__ import annotations

from math import log, exp

__all__ = [
    "exponential_decline_rate",
    "harmonic_decline_rate",
    "hyperbolic_decline_rate",
    "modified_hyperbolic_decline_rate",
    "ple_decline_rate",
    "exponential_decline_cumulative",
    "harmonic_decline_cumulative",
    "hyperbolic_decline_cumulative",
    "modified_hyperbolic_decline_cumulative",
]


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
