from __future__ import annotations

__all__ = [
    "gas_flow_rate_pss",
    "gas_flow_rate_pss_non_darcy",
    "non_darcy_coefficient",
    "time_to_pss_gas",
]


# Gas Well Production

# Gas Pseudosteady State Flow

# FIXME не сходится с источником
def gas_flow_rate_pss() -> float:
    return -1


def gas_flow_rate_pss_non_darcy() -> float:
    return -1


# FIXME: есть неточность
def time_to_pss_gas(
        re: float,
        rw: float,
        porosity: float,
        k: float,
        ct: float,
        ug: float,
) -> float:
    """
        Time, in hours, for a gas well to reach pseudo-steady-state flow.

        Parameters
        ----------
        re : float
            Drainage radius, ft.
        rw : float
            Wellbore radius, ft.
        porosity : float
            Porosity, fraction.
        k : float
            Permeability, mD.
        ct : float
            Total compressibility (gas + rock), 1/psi.
        ug : float
            Gas viscosity, cP.

        Returns
        -------
        float
            tₚₛₛ, h.

        Source
        ------
        https://petroleumoffice.com/function/timetopssgas/
        """
    if re <= rw:
        raise ValueError("re must be greater than rw")

    return 376.0 * porosity * ug * ct * (re ** 2 - rw ** 2) / k


def non_darcy_coefficient(
        rw: float,
        h: float,
        h_perf: float,
        sg_gas: float,
        ug: float,
        k: float,
) -> float:
    """
    Correlation for the non-Darcy (turbulent) flow coefficient *D*, [d/mscf].

    Parameters
    ----------
    rw : float
        Wellbore radius, [ft].
    h : float
        Net reservoir (pay) height, [ft].
    h_perf : float
        Perforated interval thickness, [ft].
    sg_gas : float
        Gas specific gravity (air = 1.0), [dimensionless].
    ug : float
        Gas viscosity, [cP].
    k : float
        Near-wellbore permeability, [mD].

    Returns
    -------
    float
        Non-Darcy flow coefficient *D*, [d/mscf].

    Notes
    -----
    Petroleum Office adopts the Jones-type empirical form

        D = **600 · SG<sub>g</sub> · k⁻⁰·¹ · h / (µ<sub>g</sub> · r<sub>w</sub> · h<sub>perf</sub>²)**

    where all quantities are in field units.
    This implementation reproduces the on-line calculator exactly.

    Source
    ------
    https://petroleumoffice.com/function/nondarcycoefficient/
    """
    if any(x <= 0 for x in (rw, h, h_perf, sg_gas, ug, k)):
        raise ValueError("all inputs must be positive")

    return 600.0 * sg_gas * k ** (-0.1) * h / (ug * rw * h_perf ** 2)
