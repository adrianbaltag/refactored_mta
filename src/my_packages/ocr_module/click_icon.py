# pylint: disable=E1101,E0401,C0301,W0612
"""This module provides a function to find and click on an image template within a specific monitor using OpenCV and pyautogui.
NOTE:
- for monitor index, add +1 to the index of the monitor you want to use.
- create a folder named 'template_img' in the 'src/my_package' directory and place your template images there.
- use the name of the image file (with extension) as the template_name argument."""

import time
from pathlib import Path

import cv2
import mss
import numpy as np
import pyautogui

# from mss import mss
from my_packages.constants_module.constant_variables import MONITOR_INDEX


def click_icon(template_name, monitor_index=MONITOR_INDEX, threshold=0.8, click=True):
    """
    Find and click on an image template within a specific monitor.

    Args:
        template_name (str): Name of the template image file (with extension)
        monitor_index (int): Index of the monitor to search on (starts at 1)
        threshold (float): Matching threshold (0.0 to 1.0), higher means more exact match
        click (bool): Whether to click on the found image or just return coordinates

    Returns:
        tuple: (x, y) coordinates of the center of the matched image, or None if not found
    """
    # Get the template path
    template_dir = Path("src/my_packages/template_img")
    template_path = template_dir / template_name

    if not template_path.exists():
        print(f"Template image not found: {template_path}")
        return None

    # Load the template image
    template = cv2.imread(str(template_path))
    if template is None:
        print(f"Failed to load template image: {template_path}")
        return None

    # Convert template to grayscale
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template_height, template_width = template_gray.shape

    # Use MSS to get monitor information and take screenshot
    with mss.mss() as sct:
        # Get monitor information
        monitors = sct.monitors

        # Print all monitors for debugging
        print(f"[INFO] Detected {len(monitors) - 1} monitors:")
        for i, m in enumerate(monitors):
            if i == 0:
                print(f"  All monitors combined: {m}")
            else:
                print(f"  Monitor {i - 1}: {m}")

        # Check if monitor_index is valid
        if monitor_index >= len(monitors):
            raise ValueError(
                f"Error: Monitor index {monitor_index} is out of range. Only {len(monitors) - 1} monitors detected."
            )

        # Get the requested monitor (mss uses 1-based indexing, and the first monitor is at index 1)
        target_monitor = monitors[monitor_index]
        print(f"[INFO] Using monitor {monitor_index}: {target_monitor}")

        # Wait for the monitor to be ready
        time.sleep(1)

        # Capture screenshot of the entire monitor
        print(f"[INFO] Capturing monitor {monitor_index}...")
        screenshot = sct.grab(target_monitor)
        # Convert to numpy array
        img = np.array(screenshot)

        # Convert to grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

        # Perform template matching
        result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        # Find the best match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if match is good enough
        if max_val < threshold:
            print(
                f"No match found for {template_name} (best match: {max_val:.2f}, threshold: {threshold})"
            )
            return None

        # Calculate the center of the matched region
        match_x = max_loc[0] + template_width // 2
        match_y = max_loc[1] + template_height // 2

        # Adjust coordinates to global screen space
        global_x = match_x + target_monitor["left"]
        global_y = match_y + target_monitor["top"]

        # Click on the match if requested
        if click:
            pyautogui.click(global_x, global_y)
            print(f"Clicked on {template_name} at ({global_x}, {global_y})")

        return (global_x, global_y)


if __name__ == "__main__":
    # Example usage
    click_icon("000115.png", threshold=0.8, click=True)
