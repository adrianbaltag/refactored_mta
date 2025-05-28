"""`__init__.py`__
This module initializes the 'constants' package.
"""

from .constant_variables import MONITOR_INDEX, REMEDY_SCREENSHOT_INDEX
from .urls import URL_FORMY, URL_MTAS, URL_NSP, URL_REMEDY

__all__ = [
    "URL_FORMY",
    "MONITOR_INDEX",
    "REMEDY_SCREENSHOT_INDEX",
    "URL_REMEDY",
    "URL_NSP",
    "URL_MTAS",
]
