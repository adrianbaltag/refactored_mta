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
import mss.tools
import numpy as np
import pyautogui

from my_packages.constants_module.constant_variables import MONITOR_INDEX
from my_packages.utils.select_monitor import select_monitor


def click_icon(
    template_name, monitor_index=MONITOR_INDEX, threshold=0.7, click=True, debug=False
):
    """
    Find and click on an image template within a specific monitor.

    Args:
        template_name (str): Name of the template image file (with extension)
        monitor_index (int): Index of the monitor to search on (0-based)
        threshold (float): Matching threshold (0.0 to 1.0), higher means more exact match
        click (bool): Whether to click on the found image or just return coordinates
        debug (bool): Whether to save debug screenshots

    Returns:
        tuple: (x, y) coordinates of the center of the matched image, or None if not found
    """
    # Import mss correctly - import the specific mss class, not the module

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

    # Get the target monitor using select_monitor function
    target_monitor = select_monitor()
    print(
        f"[INFO] Using monitor {monitor_index}: X={target_monitor.x}, Y={target_monitor.y}, Width={target_monitor.width}, Height={target_monitor.height}"
    )

    # Wait for the monitor to be ready
    time.sleep(1)

    # Define the monitor region for mss
    monitor_region = {
        "left": target_monitor.x,
        "top": target_monitor.y,
        "width": target_monitor.width,
        "height": target_monitor.height,
    }

    # Capture screenshot using mss
    print(f"[INFO] Capturing monitor {monitor_index} using mss...")
    with mss.mss() as sct:  # Use mss.mss() to create the instance
        # Capture the monitor
        screenshot = sct.grab(monitor_region)

        # Convert to numpy array - mss returns BGR format
        img = np.array(screenshot)

        # For debugging: Save the screenshot to a temporary file
        if debug:
            debug_dir = Path("temp_screenshots")
            debug_dir.mkdir(exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            debug_filename = (
                debug_dir / f"debug_{template_name.split('.')[0]}_{timestamp}.png"
            )
            # Use the proper way to save the screenshot with mss.tools
            mss.tools.to_png(
                screenshot.rgb, screenshot.size, output=str(debug_filename)
            )
            print(f"Saved debug screenshot to {debug_filename}")

    # Convert to grayscale - mss returns BGRA format
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
    global_x = match_x + target_monitor.x
    global_y = match_y + target_monitor.y

    # Click on the match if requested
    if click:
        pyautogui.click(global_x, global_y)
        print(f"Clicked on {template_name} at ({global_x}, {global_y})")

    return (global_x, global_y)


if __name__ == "__main__":
    # Example usage
    click_icon(
        "enter-number.png",
        debug=True,
    )
