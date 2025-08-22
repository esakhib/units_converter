from __future__ import annotations

__all__ = [
    "pressure_gradient_har_brown",
    "inlet_pressure_har_brown",
    "outlet_pressure_har_brown",
    "pressure_gradient_beggs_brill",
    "inlet_pressure_beggs_brill",
    "outlet_pressure_beggs_brill",
    "pressure_gradient_gray",
    "inlet_pressure_gray",
    "outlet_pressure_gray",
]


# FIXME: нужно очень много всего и непонятно где брать

# Multiphase Pipe Flow

# ────────────────────── Hagedorn & Brown ──────────────────────
def pressure_gradient_har_brown(
        Ql: float,
        Rho_l: float,
        Ul: float,
        Qg: float,
        Ug: float,
        sg_gas: float,
        z_factor: float,
        IFTgl: float,
        pipe_id: float,
        pipe_length: float,
        pipe_roughness: float,
        p: float,
        T: float,
) -> float:
    """
    Vertical pressure gradient by the Hagedorn & Brown correlation, [psi/ft].

    Parameters
    ----------
    Ql, Rho_l, Ul, Qg, Ug, sg_gas, z_factor, IFTgl, pipe_id,
    pipe_length, pipe_roughness, p, T : float
        См. словарь *Units* — единицы выводятся автоматически.

    Returns
    -------
    float
        dP/dL, [psi/ft].

    Source
    ------
    https://petroleumoffice.com/function/pressuregradientharbrown/
    """
    return -1


def inlet_pressure_har_brown(
        Ql: float,
        Rho_l: float,
        Ul: float,
        Qg: float,
        sg_gas: float,
        IFTgl: float,
        pipe_id: float,
        pipe_length: float,
        pipe_roughness: float,
        P_out: float,
        T: float,
) -> float:
    """
    Inlet pressure (Hagedorn & Brown), [psia].

    Other notes — см. стр. выше.
    """
    return -1


def outlet_pressure_har_brown(
        Ql: float,
        Rho_l: float,
        Ul: float,
        Qg: float,
        sg_gas: float,
        IFTgl: float,
        pipe_id: float,
        pipe_length: float,
        pipe_roughness: float,
        P_in: float,
        T: float,
) -> float:
    """
    Outlet pressure (Hagedorn & Brown), [psia].
    """
    return -1


# ────────────────────── Beggs & Brill ──────────────────────
def pressure_gradient_beggs_brill(
        Ql: float,
        Rho_l: float,
        Ul: float,
        Qg: float,
        Ug: float,
        sg_gas: float,
        z_factor: float,
        IFTgl: float,
        pipe_id: float,
        pipe_length: float,
        pipe_roughness: float,
        pipe_angle: float,
        p: float,
        T: float,
) -> float:
    """
    Pressure gradient by Beggs & Brill (any angle), [psi/ft].
    """
    return -1


def inlet_pressure_beggs_brill(
        Ql: float,
        Rho_l: float,
        Ul: float,
        Qg: float,
        sg_gas: float,
        IFTgl: float,
        pipe_id: float,
        pipe_length: float,
        pipe_roughness: float,
        pipe_angle: float,
        P_out: float,
        T: float,
) -> float:
    """
    Inlet pressure (Beggs & Brill), [psia].
    """
    return -1


def outlet_pressure_beggs_brill(
        Ql: float,
        Rho_l: float,
        Ul: float,
        Qg: float,
        sg_gas: float,
        IFTgl: float,
        pipe_id: float,
        pipe_length: float,
        pipe_roughness: float,
        pipe_angle: float,
        P_in: float,
        T: float,
) -> float:
    """
    Outlet pressure (Beggs & Brill), [psia].
    """
    return -1


# ─────────────────────────── Gray ───────────────────────────
def pressure_gradient_gray(
        Ql: float,
        Rho_l: float,
        Ul: float,
        Qg: float,
        Ug: float,
        sg_gas: float,
        z_factor: float,
        IFTgl: float,
        pipe_id: float,
        pipe_length: float,
        pipe_roughness: float,
        pipe_angle: float,
        p: float,
        T: float,
) -> float:
    """
    Pressure gradient by Gray correlation, [psi/ft].
    """
    return -1


def inlet_pressure_gray(
        Ql: float,
        Rho_l: float,
        Ul: float,
        Qg: float,
        sg_gas: float,
        IFTgl: float,
        pipe_id: float,
        pipe_length: float,
        pipe_roughness: float,
        pipe_angle: float,
        P_out: float,
        T: float,
) -> float:
    """
    Inlet pressure (Gray), [psia].
    """
    return -1


def outlet_pressure_gray(
        Ql: float,
        Rho_l: float,
        Ul: float,
        Qg: float,
        sg_gas: float,
        IFTgl: float,
        pipe_id: float,
        pipe_length: float,
        pipe_roughness: float,
        pipe_angle: float,
        P_in: float,
        T: float,
) -> float:
    """
    Outlet pressure (Gray), [psia].
    """
    return -1
