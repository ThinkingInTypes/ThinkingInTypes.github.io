from dataclasses import dataclass
from typing import Union

# Allowed special keywords for parameters.
ALLOWED_KEYWORDS = {"MIN", "MAX", "DEF"}

# Parameter type alias to allow either a numeric value or a special keyword.
ParamType = Union[float, str]


def _validate_param(value: ParamType, name: str) -> ParamType:
    """
    Validate and normalize a parameter value.

    Args:
        value: The parameter value, expected to be either a float (or int)
               or one of the allowed keyword strings.
        name: The name of the parameter (for error messages).

    Returns:
        The normalized value (if string, converted to uppercase) or the numeric value.

    Raises:
        ValueError: If the value is invalid or of an unexpected type.
    """
    match value:
        case str(s):
            s = s.upper()
            if s not in ALLOWED_KEYWORDS:
                raise ValueError(f"Invalid {name} parameter: {s}")
            return s
        case int() | float() as numeric if numeric > 0:
            return numeric
        case _:
            raise ValueError(f"Unexpected type for {name} parameter: {value}")


@dataclass
class MeasureVoltageDC:
    """
    Models the MEASure:VOLTage:DC? command for the Keysight 34401A.

    Attributes:
        range: Voltage measurement range as a float or special keyword ("MIN", "MAX", "DEF").
        resolution: Voltage resolution as a float or special keyword ("MIN", "MAX", "DEF").

    The __post_init__ method uses pattern matching via _validate_param to validate the fields.
    """

    range: ParamType = "DEF"
    resolution: ParamType = "DEF"

    def __post_init__(self) -> None:
        self.range = _validate_param(self.range, "range")
        self.resolution = _validate_param(self.resolution, "resolution")

        # Enforce that if resolution is non-default, range must also be non-default.
        if (
            isinstance(self.range, str)
            and self.range == "DEF"
            and not (isinstance(self.resolution, str) and self.resolution == "DEF")
        ):
            raise ValueError("Resolution specified without a valid (non-'DEF') range.")

    def command(self) -> str:
        """
        Constructs the SCPI command string for measuring DC voltage.

        Returns:
            A string representing the SCPI command.
        """
        base = "MEAS:VOLT:DC?"
        if self.range == "DEF" and self.resolution == "DEF":
            return base
        parts = []
        if self.range != "DEF":
            parts.append(str(self.range))
        if self.resolution != "DEF":
            parts.append(str(self.resolution))
        return f"{base} {'/'.join(parts)}".replace("/", ",")  # join with commas


@dataclass
class ConfigCurrentAC:
    """
    Models the CONFigure:CURRent:AC command for the Keysight 34401A.

    Attributes:
        range: Current measurement range as a float or special keyword ("MIN", "MAX", "DEF").
        resolution: Current resolution as a float or special keyword ("MIN", "MAX", "DEF").

    The __post_init__ method uses _validate_param to handle duplicated validation logic.
    """

    range: ParamType = "DEF"
    resolution: ParamType = "DEF"

    def __post_init__(self) -> None:
        self.range = _validate_param(self.range, "range")
        self.resolution = _validate_param(self.resolution, "resolution")

        # Enforce that if resolution is non-default, the range must also be non-default.
        if (
            isinstance(self.range, str)
            and self.range == "DEF"
            and not (isinstance(self.resolution, str) and self.resolution == "DEF")
        ):
            raise ValueError("Resolution specified without a valid (non-'DEF') range.")

    def command(self) -> str:
        """
        Constructs the SCPI command string for configuring AC current measurement.

        Returns:
            A string representing the SCPI configuration command.
        """
        base = "CONF:CURR:AC"
        if self.range == "DEF" and self.resolution == "DEF":
            return base
        parts = []
        if self.range != "DEF":
            parts.append(str(self.range))
        if self.resolution != "DEF":
            parts.append(str(self.resolution))
        return f"{base} {'/'.join(parts)}".replace("/", ",")  # join with commas


# Demonstration of usage:
if __name__ == "__main__":
    # Valid command with numeric parameters.
    mv_cmd = MeasureVoltageDC(range=10.0, resolution=0.001)
    print("MeasureVoltageDC command:", mv_cmd.command())

    # Valid command using special keywords (input as lower case, but validated to upper case).
    cc_cmd = ConfigCurrentAC(range="min", resolution="max")
    print("ConfigCurrentAC command:", cc_cmd.command())

    # An attempt that should fail: specifying a non-default resolution without a non-default range.
    try:
        bad_cmd = MeasureVoltageDC(resolution=0.001)
    except ValueError as error:
        print("Error:", error)
