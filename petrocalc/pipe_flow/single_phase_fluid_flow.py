from __future__ import annotations

import math

__all__ = [
    "reynolds_number_liquid",
    "friction_pressure_drop_liquid",
    "outlet_pipe_pressure_liquid",
    "inlet_pipe_pressure_liquid",
    "potential_energy_pressure_drop_liquid",
    "reynolds_number_gas",
    "inlet_pipe_pressure_gas",
    "outlet_pipe_pressure_gas",
]

GC = 32.174
FT2_PER_IN2 = 144.0
BBL_TO_FT3 = 5.615
SEC_PER_DAY = 86400

# Gas pipe flow constants
SCF_PER_MSCF = 1_000
AIR_DENS_STP = 0.0764
CP_TO_LB_FTS = 0.000671969


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
