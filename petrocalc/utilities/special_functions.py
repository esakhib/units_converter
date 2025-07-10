from __future__ import annotations

from math import exp

__all__ = [
    "exp_integral_ei"
]


# Special Functions

def exp_integral_ei(x: float) -> float:
    if x == 0.0:
        raise ValueError("Ei(x) is singular at x = 0.")
    return float(exp(x))
