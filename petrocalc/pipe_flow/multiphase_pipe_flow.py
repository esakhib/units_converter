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


# FIXME: нужно очеь много всего и непонятно где брать
# Multiphase Pipe Flow

# Hagedorn and Brown Correlation


def pressure_gradient_har_brown() -> float:
    return -1


def inlet_pressure_har_brown() -> float:
    return -1


def outlet_pressure_har_brown() -> float:
    return -1


# Beggs and Brill Correlation
def pressure_gradient_beggs_brill() -> float:
    return -1


def inlet_pressure_beggs_brill() -> float:
    return -1


def outlet_pressure_beggs_brill() -> float:
    return -1


# Gray Correaltion

def pressure_gradient_gray() -> float:
    return -1


def inlet_pressure_gray() -> float:
    return -1


def outlet_pressure_gray() -> float:
    return -1
