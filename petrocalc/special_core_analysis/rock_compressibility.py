from __future__ import annotations

__all__ = [
    "cf_newman_l",
    "cf_newman_s",
]


# Rock compressibility
# FIXME: нет коэффициентов для точного вычисения каждой из функций
def cf_newman_l(porosity: float) -> float:
    """
    Rock compressibility for **limestone** formations (Newman correlation).

    Parameters
    ----------
    porosity : float
        Porosity, fraction (*Units['porosity']*).

    Returns
    -------
    float
        Pore-volume compressibility (*1/psi*).

    Source
    ------
    https://petroleumoffice.com/function/cfnewmanl/
    """
    return -1


def cf_newman_s(porosity: float) -> float:
    """
    Rock compressibility for **sandstone** formations (Newman correlation).

    Parameters
    ----------
    porosity : float
        Porosity, fraction (*Units['porosity']*).

    Returns
    -------
    float
        Pore-volume compressibility (*1/psi*).

    Source
    ------
    https://petroleumoffice.com/function/cfnewmans/
    """
    return -1
