"""Capture a screenshot of a specific monitor using mss."""

# pylint: disable=E0401, W0105,W0012,W0612, F841, C0301
import os
import time

import mss
import mss.tools
from PIL import Image

from my_packages.constants_module.constant_variables import MONITOR_INDEX


def capture_full_screenshot(monitor_index: int = MONITOR_INDEX) -> str:
    """Captures a screenshot of a specific monitor.
    Screenshots are saved in the 'img_to_read' directory.
    The directory is created if it doesn't exist.

    Args:
        monitor_index (int): Index of the monitor to use (0-based).
    """
    # Build path to src/my_package/images
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    package_root_dir = os.path.abspath(os.path.join(current_file_dir, ".."))
    images_dir = os.path.join(package_root_dir, "img_to_read")
    os.makedirs(images_dir, exist_ok=True)

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
        if monitor_index + 1 >= len(monitors):
            raise ValueError(
                f"Error: Monitor index {monitor_index} is out of range. Only {len(monitors) - 1} monitors detected."
            )

        # Get the requested monitor (add 1 because mss uses 1-based indexing, with 0 being "all monitors")
        target_monitor = monitors[monitor_index + 1]
        print(f"[INFO] Using monitor {monitor_index}: {target_monitor}")
        time.sleep(5)  # Wait for the monitor to be ready
        # Capture screenshot of the entire monitor
        print(f"[INFO] Capturing monitor {monitor_index}...")
        screenshot = sct.grab(target_monitor)

        # Convert to PIL Image for processing and saving
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # Check if the image is empty or black
        if img.getbbox() is None:
            raise ValueError(
                "[ERROR] Screenshot appears to be empty or completely black"
            )

    # Save the screenshot
    filename = f"monitor{monitor_index}.png"
    save_path = os.path.join(images_dir, filename)

    img.save(save_path)
    print(f"✅ Screenshot saved to: {save_path}")
    return save_path


if __name__ == "__main__":
    # Capture the first monitor (index 0)
    capture_full_screenshot()
