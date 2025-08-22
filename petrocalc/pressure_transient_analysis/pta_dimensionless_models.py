from __future__ import annotations

__all__ = [
    "pd_lssihr",
    "pdw_vwihr",
    "pdw_vwihrlcpb",
    "pdw_vwihrlsfb",
    "pdw_vwihrpcpb",
    "pdw_vwihrpmb",
    "pdw_vwihrpsfb"
]


# PTA dimensionless models
# FIXME: нет данных для реализации
def pd_lssihr(td: float, rd: float) -> float:
    """
    Dimensionless pressure drop **Pᴅ** for the line-source solution
    in an infinite homogeneous reservoir.

    Parameters
    ----------
    td : float
        Dimensionless time (*Units['td']*).
    rd : float
        Dimensionless radius (*Units['rd']*).

    Returns
    -------
    float
        Dimensionless pressure drop (placeholder value −1).

    Source
    ------
    https://petroleumoffice.com/function/pdlssihr/
    """
    return -1


def pdw_vwihr(td: float, cd: float, s: float) -> float:
    """
    Dimensionless wellbore pressure drop **Pᴅʷ** for a vertical well
    in an infinite homogeneous reservoir.

    Parameters
    ----------
    td : float
        Dimensionless time (*Units['td']*).
    cd : float
        Dimensionless wellbore-storage coefficient (*Units['cd']*).
    s : float
        Skin factor (*Units['s']*).

    Returns
    -------
    float
        Dimensionless wellbore pressure drop (placeholder −1).

    Source
    ------
    https://petroleumoffice.com/function/pdwvwihr/
    """
    return -1


def pdw_vwihrlcpb(td: float, cd: float, s: float, ld: float) -> float:
    """
    Dimensionless wellbore pressure drop **Pᴅʷ** for a vertical well
    with a *linear constant-pressure boundary*.

    Parameters
    ----------
    td : float
        Dimensionless time (*Units['td']*).
    cd : float
        Dimensionless wellbore-storage coefficient (*Units['cd']*).
    s : float
        Skin factor (*Units['s']*).
    ld : float
        Dimensionless distance to boundary (*Units['ld']*).

    Returns
    -------
    float
        Dimensionless wellbore pressure drop (placeholder −1).

    Source
    ------
    https://petroleumoffice.com/function/pdwvwihrlcpb/
    """
    return -1


def pdw_vwihrlsfb(td: float, cd: float, s: float, ld: float) -> float:
    """
    Dimensionless wellbore pressure drop **Pᴅʷ** for a vertical well
    with a *linear sealing-fault boundary*.

    Parameters
    ----------
    td : float
        Dimensionless time (*Units['td']*).
    cd : float
        Dimensionless wellbore-storage coefficient (*Units['cd']*).
    s : float
        Skin factor (*Units['s']*).
    ld : float
        Dimensionless distance to boundary (*Units['ld']*).

    Returns
    -------
    float
        Dimensionless wellbore pressure drop (placeholder −1).

    Source
    ------
    https://petroleumoffice.com/function/pdwvwihrlsfb/
    """
    return -1


def pdw_vwihrpcpb(td: float, cd: float, s: float, ld1: float, ld2: float) -> float:
    """
    Dimensionless wellbore pressure drop **Pᴅʷ** for a vertical well
    with *perpendicular constant-pressure boundaries*.

    Parameters
    ----------
    td : float
        Dimensionless time (*Units['td']*).
    cd : float
        Dimensionless wellbore-storage coefficient (*Units['cd']*).
    s : float
        Skin factor (*Units['s']*).
    ld1 : float
        Dimensionless distance to boundary 1 (*Units['ld']*).
    ld2 : float
        Dimensionless distance to boundary 2 (*Units['ld']*).

    Returns
    -------
    float
        Dimensionless wellbore pressure drop (placeholder −1).

    Source
    ------
    https://petroleumoffice.com/function/pdwvwihrpcpb/
    """
    return -1


def pdw_vwihrpmb(td: float, cd: float, s: float, ld1: float, ld2: float) -> float:
    """
    Dimensionless wellbore pressure drop **Pᴅʷ** for a vertical well
    with *perpendicular mixed boundaries* (fault + constant pressure).

    Parameters
    ----------
    td : float
        Dimensionless time (*Units['td']*).
    cd : float
        Dimensionless wellbore-storage coefficient (*Units['cd']*).
    s : float
        Skin factor (*Units['s']*).
    ld1 : float
        Dimensionless distance to boundary 1 (*Units['ld']*).
    ld2 : float
        Dimensionless distance to boundary 2 (*Units['ld']*).

    Returns
    -------
    float
        Dimensionless wellbore pressure drop (placeholder −1).

    Source
    ------
    https://petroleumoffice.com/function/pdwvwihrpmb/
    """
    return -1


def pdw_vwihrpsfb(td: float, cd: float, s: float, ld1: float, ld2: float) -> float:
    """
    Dimensionless wellbore pressure drop **Pᴅʷ** for a vertical well
    with *perpendicular sealing-fault boundaries*.

    Parameters
    ----------
    td : float
        Dimensionless time (*Units['td']*).
    cd : float
        Dimensionless wellbore-storage coefficient (*Units['cd']*).
    s : float
        Skin factor (*Units['s']*).
    ld1 : float
        Dimensionless distance to boundary 1 (*Units['ld']*).
    ld2 : float
        Dimensionless distance to boundary 2 (*Units['ld']*).

    Returns
    -------
    float
        Dimensionless wellbore pressure drop (placeholder −1).

    Source
    ------
    https://petroleumoffice.com/function/pdwvwihrpsfb/
    """
    return -1
