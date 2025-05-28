"""`__init__.py`__
This module initializes the 'ocr' package.
"""

from .capture_and_click import capture_and_click
from .capture_full_screenshot import capture_full_screenshot
from .capture_partial_screenshot import capture_partial_screenshot
from .click_icon import click_icon
from .crop_image_by_index import crop_image_by_index
from .gpu_checkup import gpu_checkup
from .nsp_extract_sites import get_most_common_site

__all__ = [
    "gpu_checkup",
    "capture_and_click",
    "capture_full_screenshot",
    "click_icon",
    "capture_partial_screenshot",
    "get_most_common_site",
    "crop_image_by_index",
]
