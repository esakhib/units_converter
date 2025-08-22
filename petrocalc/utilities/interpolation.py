from __future__ import annotations

__all__ = [
    "cubic_spline_differentiate",
    "cubic_spline_integrate",
    "cubic_spline_integrate_t1_t2",
    "cubic_spline_interpolate",
    "cubic_splines_intersection",
    "data_differentiate",
    "linear_spline_differentiate",
    "linear_spline_integrate",
    "linear_spline_integrate_t1_t2",
    "linear_spline_interpolate",
    "linear_splines_intersection",
    "step_interpolate",
    "proximal_interpolate",
]


# Utilities

# Interpolation
# FIXME: не совпадает с источником
def cubic_spline_differentiate(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t: float,
) -> float:
    """
    Natural cubic spline – **first derivative** at point *t*.

    Parameters
    ----------
    x_values : sequence of float
        Sampled *x* values (*Units['x_values']*).
    y_values : sequence of float
        Sampled *y* values (*Units['y_values']*).
    t : float
        Target point (abscissa) (*Units['t']*).

    Returns
    -------
    float
        d*y*/d*x* at *x = t*.

    Source
    ------
    https://petroleumoffice.com/function/cubicsplinedifferentiate/
    """
    return -1


def cubic_spline_integrate(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t: float,
) -> float:
    """
    Natural cubic spline – **definite integral** from *x₀* to *t*.

    See also
    --------
    `cubic_spline_integrate_t1_t2` – integrate between arbitrary limits.

    Source
    ------
    https://petroleumoffice.com/function/cubicsplineintegrate/
    """
    return -1


def cubic_spline_integrate_t1_t2(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t1: float,
        t2: float,
) -> float:
    """
    Natural cubic spline – **definite integral** from *t₁* to *t₂*.

    Source
    ------
    https://petroleumoffice.com/function/cubicsplineintegratet1t2/
    """
    return -1


def cubic_spline_interpolate(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t: float,
) -> float:
    """
    Natural cubic spline – **interpolated value** at point *t*.

    Source
    ------
    https://petroleumoffice.com/function/cubicsplineinterpolate/
    """
    return -1


def cubic_splines_intersection(
        x_values1: list[float] | tuple[float, ...],
        y_values1: list[float] | tuple[float, ...],
        x_values2: list[float] | tuple[float, ...],
        y_values2: list[float] | tuple[float, ...],
) -> float:
    """
    **x-coordinate** of the intersection point of two natural cubic splines.

    Notes
    -----
    The function searches for a single intersection within the
    common domain of the two splines.

    Source
    ------
    https://petroleumoffice.com/function/cubicsplinesintersection/
    """
    return -1


def data_differentiate(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t: float,
) -> float:
    """
    Smoothed **numerical derivative** of discrete data at *t*.

    Source
    ------
    https://petroleumoffice.com/function/datadifferentiate/
    """
    return -1


# ────────────────────────────────────
# Linear-spline helpers
# ────────────────────────────────────
def linear_spline_differentiate(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t: float,
) -> float:
    """
    Linear spline – **first derivative** at point *t*.

    Source
    ------
    https://petroleumoffice.com/function/linearsplinedifferentiate/
    """
    return -1


def linear_spline_integrate(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t: float,
) -> float:
    """
    Linear spline – **definite integral** from *x₀* to *t*.

    Source
    ------
    https://petroleumoffice.com/function/linearsplineintegrate/
    """
    return -1


def linear_spline_integrate_t1_t2(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t1: float,
        t2: float,
) -> float:
    """
    Linear spline – **definite integral** from *t₁* to *t₂*.

    Source
    ------
    https://petroleumoffice.com/function/linearsplineintegratet1t2/
    """
    return -1


def linear_spline_interpolate(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t: float,
) -> float:
    """
    Linear spline – **interpolated value** at point *t*.

    Source
    ------
    https://petroleumoffice.com/function/linearsplineinterpolate/
    """
    return -1


def linear_splines_intersection(
        x_values1: list[float] | tuple[float, ...],
        y_values1: list[float] | tuple[float, ...],
        x_values2: list[float] | tuple[float, ...],
        y_values2: list[float] | tuple[float, ...],
) -> float:
    """
    **x-coordinate** of the intersection point of two *linear* splines.

    Source
    ------
    https://petroleumoffice.com/function/linearsplinesintersection/
    """
    return -1


# ────────────────────────────────────
# Miscellaneous interpolation
# ────────────────────────────────────
def step_interpolate(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t: float,
) -> float:
    """
    Step (zero-order hold) **interpolation** at point *t*.

    Source
    ------
    https://petroleumoffice.com/function/stepinterpolate/
    """
    return -1


def proximal_interpolate(
        x_values: list[float] | tuple[float, ...],
        y_values: list[float] | tuple[float, ...],
        t: float,
) -> float:
    """
    Proximal (nearest-neighbour) **interpolation** at point *t*.

    Source
    ------
    https://petroleumoffice.com/function/proximalinterpolate/
    """
    return -1
