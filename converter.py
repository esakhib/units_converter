from collections.abc import Iterable

import numpy as np

from categories import UnitData


class UnitConverter:
    @staticmethod
    def convert_unit(from_unit: UnitData, to_unit: UnitData, value: float | Iterable[float]) -> float | np.ndarray:
        """
        Convert from one unit to another within a specified category.

        Parameters
        ----------
        from_unit : UnitData
            The source unit.
        to_unit : UnitData
            The target unit.
        value : float | Iterable[float]
            The value(s) to be converted.

        Returns
        -------
        float | np.ndarray
            The converted value.

        """

        is_seq = isinstance(value, Iterable) and not isinstance(value, (str, bytes))
        v = np.array(value) if is_seq else value

        # this part only for temperature
        if from_unit.offset or to_unit.offset:
            conv_base = (v + from_unit.offset) * from_unit.factor
            return conv_base / to_unit.factor - to_unit.offset

        return v * (from_unit.factor / to_unit.factor)


def output_result(from_unit: UnitData, to_unit: UnitData, values: float | Iterable[float],
                  result: float | np.ndarray) -> None:
    """
    Outputs the results of unit conversion.

    Parameters
    ----------
    from_unit : UnitData
        The unit being converted from.
    to_unit : UnitData
        The unit being converted to.
    values : float | Iterable[float]
        The original values in the source unit.
    result : float | np.ndarray
        The converted values in the target unit.

    """

    if isinstance(values, Iterable):
        for original, converted in zip(values, result):
            print(f"{original} {from_unit.abbr} = {converted} {to_unit.abbr}")
    else:
        print(f"{values} {from_unit.abbr} = {result} {to_unit.abbr}")
