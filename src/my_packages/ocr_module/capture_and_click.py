# pylint:disable=missing-module-docstring, missing-function-docstring, invalid-name,line-too-long,import-error
"""This module takes a screenshot of a specified monitor, searches for a keyword using OCR, and clicks on it.
It uses the `mss` library for screen capture, `easyocr` for text recognition, and `pyautogui` for mouse control.
Save the screenshot to the Desktop in a folder named 'BROWSER_FULL_SCREENSHOT'.
It also uses `pygetwindow` to get the active window's position."""

import os
import re

import easyocr
import mss
import mss.tools
import pyautogui
import pygetwindow as gw
from PIL import Image

from my_packages.constants_module.constant_variables import MONITOR_INDEX


def capture_and_click(screenshot_name, keyword, monitor_index=MONITOR_INDEX):
    """Captures a screenshot of the specified monitor, searches for a keyword, and clicks it.

    Args:
        screenshot_name (str): Name of the screenshot file (without extension).
        keyword (str): The text to search for using OCR and regex.
        monitor_index (int): Index of the monitor to capture (0-based).
    """
    # Step 1: Get active window for reference
    browser_window = gw.getActiveWindow()
    if not browser_window:
        print("No active window found!")
        return

    window_center_x = browser_window.left + browser_window.width // 2
    window_center_y = browser_window.top + browser_window.height // 2
    print(f"Active window center at ({window_center_x}, {window_center_y})")

    # Step 2: Create screenshot directory
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    new_folder = os.path.join(desktop_path, "BROWSER_FULL_SCREENSHOT")
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print(f"Directory created: {new_folder}")

    screenshot_path = os.path.join(new_folder, f"{screenshot_name}.png")

    # Step 3: Use mss to capture the screen - it handles negative coordinates correctly
    with mss.mss() as sct:
        # Get monitor information
        monitors = sct.monitors

        # Print all monitors for debugging
        print(f"Detected {len(monitors) - 1} monitors:")
        for i, m in enumerate(monitors):
            if i == 0:
                print(f"  All monitors combined: {m}")
            else:
                print(f"  Monitor {i - 1}: {m}")

        # Check if monitor_index is valid
        if monitor_index + 1 >= len(monitors):
            print(
                f"Error: Monitor index {monitor_index} is out of range. Only {len(monitors) - 1} monitors detected."
            )
            return

        # Get the requested monitor (add 1 because mss uses 1-based indexing, with 0 being "all monitors")
        target_monitor = monitors[monitor_index + 1]
        print(f"Using monitor {monitor_index}: {target_monitor}")

        # Capture screenshot
        screenshot = sct.grab(target_monitor)

        # Save to the file
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)
        print(f"Screenshot saved at: {screenshot_path}")

        # Convert to PIL Image for processing
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # Check if the image is empty or black
        if img.getbbox() is None:
            print("Warning: Screenshot appears to be empty or completely black")
            return

    # Step 4: Use OCR to extract text and positions
    print("Running OCR on the screenshot...")
    reader = easyocr.Reader(["en"], gpu=True)
    results = reader.readtext(screenshot_path)

    print(f"OCR found {len(results)} text regions")
    for i, (bbox, text, prob) in enumerate(results):
        print(f"  Text {i}: '{text}' (confidence: {prob:.2f})")

    # Step 5: Apply regex to find a keyword
    keyword_pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    print(f"Searching for keyword: '{keyword}'")

    # Track monitor origin for coordinate calculation
    mon_left = target_monitor["left"]
    mon_top = target_monitor["top"]

    for bbox, text, prob in results:
        if keyword_pattern.search(text):
            # Calculate center position - need to account for monitor position
            x_min, y_min = bbox[0]
            x_max, y_max = bbox[2]

            # Calculate center relative to the screenshot
            rel_center_x = (x_min + x_max) // 2
            rel_center_y = (y_min + y_max) // 2

            # Convert to absolute screen coordinates
            abs_center_x = mon_left + rel_center_x
            abs_center_y = mon_top + rel_center_y

            print(
                f"Found '{text}' at relative position ({rel_center_x}, {rel_center_y})"
            )
            print(
                f"Converting to absolute screen position: ({abs_center_x}, {abs_center_y})"
            )

            # Step 6: Click on the detected text
            print(f"Moving to ({abs_center_x}, {abs_center_y}) and clicking...")
            pyautogui.moveTo(abs_center_x, abs_center_y, duration=0.5)
            pyautogui.click()
            print(
                f"Clicked on '{text}' at screen position ({abs_center_x}, {abs_center_y})"
            )
            return  # Stop after the first match

    print(f"Keyword '{keyword}' not found in screenshot.")

    # Step 4: Use OCR to extract text and positions
    reader = easyocr.Reader(["en"], gpu=True)
    results = reader.readtext(screenshot_path)

    # Step 5: Apply regex to find a keyword
    keyword_pattern = re.compile(re.escape(keyword), re.IGNORECASE)


if __name__ == "__main__":
    # Example: Search for and click on "Enter last name" on monitor 0

    capture_and_click("screenshot", "Enter Number")
