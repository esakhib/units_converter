from __future__ import annotations

from math import log, exp

__all__ = [
    "basic_field_profile",
    "combined_field_profile"
]

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