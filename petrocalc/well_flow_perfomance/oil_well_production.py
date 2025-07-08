from __future__ import annotations

__all__ = [
    "flow_rate_pss",
    "flow_rate_pss_vogel",
    "prod_index_hor_well_bo",
    "prod_index_hor_well_bo2",
    "prod_index_pss",
    "time_to_pss",
    "flow_rate_ss",
    "flow_rate_ss_vogel",
    "prod_index_hor_well_borisov",
    "prod_index_hor_well_grj",
    "prod_index_hor_well_joshi",
    "prod_index_hor_well_rd",
    "prod_index_ss",
    "flow_rate_tf",
    "flow_rate_tf_vogel",
    "prod_index_tf",
]


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

    Source
    ------
    https://petroleumoffice.com/function/flowratepssvogel/
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


def flow_rate_pss(j: float, p_avg: float, pwf: float) -> float:
    r"""
    Pseudosteady-state production flow rate for an oil well.

    Parameters
    ----------
    j : float
        *Pseudosteady*-state productivity index, [STB/(d·psi)].
    p_avg : float
        Average reservoir pressure, [psi].
    pwf : float
        Bottom-hole flowing pressure, [psi].

    Returns
    -------
    float
        Flow rate, [STB/d].

    Notes
    -----
    The pseudosteady-state inflow equation is

    A negative result is physically meaningless; in practice, rates
    are considered zero when :math:`P_\text{wf} \ge P_\text{avg}`.

    Source
    ------
    https://petroleumoffice.com/function/flowratepss/
    """
    q = j * (p_avg - pwf)
    return max(q, 0.0)


# FIXME: не нашел правильной реализации, совпадающей с образцом
def prod_index_hor_well_bo() -> float:
    return -1


def prod_index_hor_well_bo2() -> float:
    return -1


import math


def prod_index_pss(k: float, h: float, bl: float, ul: float, re: float, rw: float, s: float) -> float:
    r"""
    Pseudosteady-state productivity index for a vertical oil well.

    The correlation is derived from radial-flow Darcy theory for a bounded
    reservoir that has reached pseudosteady conditions:

    Parameters
    ----------
    k : float
        Permeability, [mD].
    h : float
        Net pay (reservoir height), [ft].
    bl : float
        Oil formation-volume factor, [bbl / STB].
    ul : float
        Oil viscosity, [cP].
    re : float
        Drainage radius, [ft].
    rw : float
        Wellbore radius, [ft].
    s : float
        Skin factor, dimensionless.

    Returns
    -------
    float
        Productivity index *J*, [STB / (d·psi)].

    Source
    ------
    https://petroleumoffice.com/function/prodindexpss/
    """
    denom = math.log(re / rw) - 0.75 + s
    if denom <= 0.0:
        return 0.0
    return 0.00708 * k * h / (bl * ul * denom)


def time_to_pss(re: float, k: float, ul: float, porosity: float, ct: float) -> float:
    r"""
    Time (in hours) for a reservoir to reach pseudosteady-state flow.

    For a regularly shaped drainage area with a centrally placed vertical
    well, the empirical relation is

    Parameters
    ----------
    re : float
        Drainage radius, [ft].
    k : float
        Permeability, [mkD].
    ul : float
        Liquid viscosity, [cP].
    porosity : float
        Rock porosity, fraction.
    ct : float
        Total compressibility (rock + fluid), [1/psi].

    Returns
    -------
    float
        Time to pseudosteady state, [h].

    Source
    ------
    https://petroleumoffice.com/function/timetopss/
    """
    if k <= 0:
        raise ValueError("Permeability K must be positive.")
    t_pss = 1190.0 * porosity * ul * ct * re ** 2 / k
    return max(t_pss, 0.0)


# Oil steady state flow

def flow_rate_ss(j: float, pe: float, pwf: float) -> float:
    """
    Steady-state production flow rate for an oil well.

    Parameters
    ----------
    j : float
        Steady-state productivity index, [STB/(d·psi)].
    pe : float
        Reservoir (external-boundary) pressure, [psia].
    pwf : float
        Bottom-hole flowing pressure, [psia].

    Returns
    -------
    float
        Flow rate, [STB/d].

    Notes
    -----
    Uses the proportional inflow relationship

        q = J · (Pe – Pwf)

    A negative differential (Pwf ≥ Pe) gives zero production.

    Source
    ------
    https://petroleumoffice.com/function/flowratess/
    """
    q = j * (pe - pwf)
    return max(q, 0.0)


def flow_rate_ss_vogel(
        j: float,
        pe: float,
        pwf: float,
        pb: float,
) -> float:
    """
    Vogel inflow performance for **steady-state** flow.

    Parameters
    ----------
    j : float
        Steady-state productivity index, [STB/(d·psi)].
    pe : float
        Reservoir (external-boundary) pressure, [psia].
    pwf : float
        Bottom-hole flowing pressure, [psia].
    pb : float
        Bubble-point pressure, [psia].

    Returns
    -------
    float
        Flow rate, [STB/d].

    Notes
    -----
    * When *Pwf ≥ Pb*, single-phase oil flow is assumed and the
      linear relationship *q = J · (Pe – Pwf)* is applied.
    * When *Pwf < Pb*, solution-gas drive dominates; Vogel’s quadratic fit
      is used with *Pe* as the upstream pressure:

        q = J · (Pe – Pb) · (1 – 0.2·r – 0.8·r²)
        where r = Pwf / Pb.

    Source
    ------
    https://petroleumoffice.com/function/flowratessvogel/
    """
    if pwf >= pb:
        return flow_rate_ss(j, pe, pwf)

    r = pwf / pb
    q = j * (pe - pb) * (1.0 - 0.2 * r - 0.8 * r * r)
    return max(q, 0.0)


# FIXME: не смог найти подходящую реализацию
def prod_index_hor_well_borisov() -> float:
    return -1


def prod_index_hor_well_grj() -> float:
    return -1


def prod_index_hor_well_joshi() -> float:
    return -1


def prod_index_hor_well_rd() -> float:
    return -1


def prod_index_ss(
        k: float,
        h: float,
        bl: float,
        ul: float,
        re: float,
        rw: float,
        s: float,
) -> float:
    """
    Steady-state productivity index for a vertical oil well.

    Parameters
    ----------
    k : float
        Permeability, [mD].
    h : float
        Net pay thickness, [ft].
    bl : float
        Oil formation-volume factor, [bbl/STB].
    ul : float
        Oil viscosity, [cP].
    re : float
        Drainage (external-boundary) radius, [ft].
    rw : float
        Wellbore radius, [ft].
    s : float
        Skin factor (dimensionless).

    Returns
    -------
    float
        Productivity index *J*, [STB/(d·psi)].

    Notes
    -----
    The steady-state radial Darcy expression is

        J = 0.00708 · k · h / [Bl · μl · (ln(Re/Rw) + S)].

    If the denominator is ≤ 0, the function returns zero.

    Source
    ------
    https://petroleumoffice.com/function/prodindexss/ :contentReference[oaicite:2]{index=2}
    """
    denom = math.log(re / rw) + s
    if denom <= 0.0:
        return 0.0
    return 0.00708 * k * h / (bl * ul * denom)


# Oil transient flow

def flow_rate_tf(j: float, pi: float, pwf: float) -> float:
    """
    Transient-state production flow rate for an oil well.

    Parameters
    ----------
    j : float
        Time-dependent productivity index for transient flow, STB/(d·psi).
    pi : float
        Initial (undisturbed) reservoir pressure, psia.
    pwf : float
        Bottom-hole flowing pressure, psia.

    Returns
    -------
    float
        Flow rate, STB/d.

    Notes
    -----
    Uses the linear inflow relationship ``q = J · (Pi − Pwf)``.
    If *Pwf ≥ Pi* the result is forced to 0.

    Source
    ------
    https://petroleumoffice.com/function/flowratetf/
    """
    q = j * (pi - pwf)
    return max(q, 0.0)


# FIXME: не сходится с источником
def flow_rate_tf_vogel(j: float, pi: float, pwf: float, pb: float) -> float:
    return -1


def prod_index_tf(
        time: float,
        k: float,
        h: float,
        bl: float,
        ul: float,
        porosity: float,
        ct: float,
        rw: float,
        s: float,
) -> float:
    return -1
