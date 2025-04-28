"""`__init__.py`__
This module initializes the 'ocr' package.
"""

from .capture_and_click import capture_and_click
from .capture_full_screenshot import capture_full_screenshot
from .click_icon import click_icon
from .gpu_checkup import gpu_checkup

__all__ = ["gpu_checkup", "capture_and_click", "capture_full_screenshot", "click_icon"]
