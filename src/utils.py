import time

def set_timezone_from_env(default: str = "UTC") -> None:
    """
    Set the system timezone from the TZ environment variable, if available.
    Args:
        default (str): The default timezone if TZ is not set.
    """
    tz = os.environ.get("TZ", default)
    try:
        os.environ["TZ"] = tz
        time.tzset()
    except (AttributeError, Exception):
        # time.tzset() is not available on all platforms (e.g., Windows)
        pass
import os
import re

def get_env_variable(name: str, default: str) -> str:
    """
    Get an environment variable or return a default value.
    Args:
        name (str): The environment variable name.
        default (str): The default value if the variable is not set.
    Returns:
        str: The value of the environment variable or the default.
    """
    return os.environ.get(name, default)

def parse_interval(interval_str: str) -> int:
    """
    Parse a time interval string (e.g., '2h', '30m', '1d', '3600') into seconds.
    Supported units: s (seconds), m (minutes), h (hours), d (days).
    If no unit is given, seconds are assumed.
    """
    interval_str = interval_str.strip().lower()
    match = re.fullmatch(r"(\d+)([smhd]?)", interval_str)
    if not match:
        raise ValueError(f"Invalid interval format: {interval_str}")
    value, unit = match.groups()
    value = int(value)
    if unit == '':
        return value
    elif unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 3600
    elif unit == 'd':
        return value * 86400
    else:
        raise ValueError(f"Unknown time unit: {unit}")