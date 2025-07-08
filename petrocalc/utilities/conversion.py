from __future__ import annotations

__all__ = [
    "api_2sg",
    "sg_2api",
    "unit_converter"
]


# Conversion

def api_2sg(api: float) -> float:
    """
    Convert **API gravity** to oil *specific gravity* (water = 1.0).

    Parameters
    ----------
    api : float
        Oil gravity in degrees API (*Units['api']*).

    Returns
    -------
    float
        Oil specific gravity (*Units['sg']*).

    Notes
    -----
    Formula (ASTM D287):

        ``SG = 141.5 / (API + 131.5)``

    The result is physically meaningful for *API > 0*. Typical crude oils
    lie in the range *SG ≈ 0.5 … 1.0* (API 10 … °50).

    Source
    ------
    ttps://petroleumoffice.com/function/api2sg/
    """
    if api <= 0:
        raise ValueError("API gravity must be a positive number.")
    sg = 141.5 / (api + 131.5)
    return sg


def sg_2api(sg: float) -> float:
    """
    Convert oil *specific gravity* (water = 1.0) to **API gravity**.

    Parameters
    ----------
    sg : float
        Oil specific gravity at 60 °F (*Units['sg']*).

    Returns
    -------
    float
        API gravity (*Units['api']*).

    Notes
    -----
    Formula (ASTM D287):

        ``API = 141.5 / SG − 131.5``

    Valid for *SG > 0*. Crude oils commonly fall between
    API ≈ 10 … 50 (depending on reservoir).

    Source
    ------
    ttps://petroleumoffice.com/function/sg2api/
    """
    if sg <= 0:
        raise ValueError("Specific gravity must be a positive number.")
    api = 141.5 / sg - 131.5
    if api <= 0:
        raise ValueError("Computed API gravity is non-positive; check `sg` value.")
    return api


# TODO: связать с юнит конвертером
def unit_converter() -> float():
    return -1
