from __future__ import annotations

__all__ = [
    "pw_vwihr",
    "pw_vwihrlcpb",
    "pw_vwihrlsfb",
    "pw_vwihrpcpb",
    "pw_vwihrpmb",
    "pw_vwihrpsfb",
]


# Pressure transient analysis

# PTA models

# FIXME: не совпадает с источником
def pw_vwihr(
    time: float,
    prod_data: float,
    bl: float,
    ul: float,
    c: float,
    rw: float,
    s: float,
    ct: float,
    porosity: float,
    h: float,
    k: float,
) -> float:
    """
    Wellbore pressure drop **P<sub>w</sub>** for a *vertical well in an infinite,
    homogeneous reservoir* (no boundaries).

    Parameters
    ----------
    time : float
        Elapsed time (*Units['time']*).
    prod_data : float
        Production-rate array or single flow-rate value at the surface
        (*user-defined units*).
    bl : float
        Formation volume factor (*Units['bl']*).
    ul : float
        Viscosity (*Units['ul']*).
    c : float
        Wellbore storage coefficient (*Units['c']*).
    rw : float
        Wellbore radius (*Units['rw']*).
    s : float
        Skin factor (*Units['s']*).
    ct : float
        Total compressibility (*Units['ct']*).
    porosity : float
        Reservoir porosity (*Units['porosity']*).
    h : float
        Net formation thickness (*Units['h']*).
    k : float
        Permeability (*Units['k']*).

    Returns
    -------
    float
        Wellbore pressure drop, **psi** (placeholder –1).

    Notes
    -----
    This is a *stub*: only the interface is defined.

    Source
    ------
    https://petroleumoffice.com/function/pwvwihr/
    """
    return -1


def pw_vwihrlcpb(
    time: float,
    prod_data: float,
    bl: float,
    ul: float,
    c: float,
    rw: float,
    s: float,
    ct: float,
    porosity: float,
    h: float,
    k: float,
    l: float,
) -> float:
    """
    Vertical well in an infinite reservoir with a **linear constant-pressure**
    boundary at distance *L*.

    Additional parameter
    --------------------
    l : float
        Distance to boundary (*Units['l']*).

    Returns
    -------
    float
        Pressure drop, **psi** (placeholder –1).

    Source
    ------
    https://petroleumoffice.com/function/pwvwihrlcpb/
    """
    return -1


def pw_vwihrlsfb(
    time: float,
    prod_data: float,
    bl: float,
    ul: float,
    c: float,
    rw: float,
    s: float,
    ct: float,
    porosity: float,
    h: float,
    k: float,
    l: float,
) -> float:
    """
    Vertical well with a **linear sealing-fault** boundary at distance *L*.

    See `pw_vwihrlcpb` for common arguments.

    Source
    ------
    https://petroleumoffice.com/function/pwvwihrlsfb/
    """
    return -1


def pw_vwihrpcpb(
    time: float,
    prod_data: float,
    bl: float,
    ul: float,
    c: float,
    rw: float,
    s: float,
    ct: float,
    porosity: float,
    h: float,
    k: float,
    l1: float,
    l2: float,
) -> float:
    """
    Vertical well with **perpendicular constant-pressure** boundaries.

    Extra parameters
    ----------------
    l1, l2 : float
        Distances to boundary 1 and 2 (*Units['l']*).

    Returns
    -------
    float
        Pressure drop, **psi** (placeholder –1).

    Source
    ------
    https://petroleumoffice.com/function/pwvwihrpcpb/
    """
    return -1


def pw_vwihrpmb(
    time: float,
    prod_data: float,
    bl: float,
    ul: float,
    c: float,
    rw: float,
    s: float,
    ct: float,
    porosity: float,
    h: float,
    k: float,
    l1: float,
    l2: float,
) -> float:
    """
    Vertical well with **perpendicular mixed boundaries**
    (boundary 1 – sealing fault, boundary 2 – constant pressure).

    See `pw_vwihrpcpb` for argument descriptions.

    Source
    ------
    https://petroleumoffice.com/function/pwvwihrpmb/
    """
    return -1


def pw_vwihrpsfb(
    time: float,
    prod_data: float,
    bl: float,
    ul: float,
    c: float,
    rw: float,
    s: float,
    ct: float,
    porosity: float,
    h: float,
    k: float,
    l1: float,
    l2: float,
) -> float:
    """
    Vertical well with **perpendicular sealing-fault** boundaries.

    See `pw_vwihrpcpb` for argument descriptions.

    Source
    ------
    https://petroleumoffice.com/function/pwvwihrpsfb/
    """
    return -1
