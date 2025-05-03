# pylint: disable=import-outside-toplevel, invalid-name, too-many-arguments, too-many-locals, too-many-statements,line-too-long
"""This script captures a cropped area from a screenshot that contains multiple specified text markers.
It uses the EasyOCR library for optical character recognition (OCR) and the mss library for screen capturing - on specified monitor"""

import os
import time

import easyocr
import mss
import numpy as np
from PIL import Image

from my_packages.constants_module.constant_variables import MONITOR_INDEX


def capture_partial_screenshot(
    text_markers,
    save_full=False,
    confidence_threshold=0.7,
    monitor_index=MONITOR_INDEX,
):
    """
    Capture a cropped area from a screenshot that contains multiple specified text markers.

    Args:
        text_markers (list[str]): List of text strings to find.
        save_full (bool, optional): Save full screenshot before cropping. Defaults to False.
        confidence_threshold (float, optional): OCR minimum confidence threshold. Defaults to 0.7.
        monitor_index (int, optional): Monitor index (1 = primary monitor). Defaults to constant value.

    Returns:
        tuple[str, tuple]: (saved_path, (left, top, right, bottom))
    """
    # Prepare project and image directory paths
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    images_dir = os.path.join(project_root, "my_packages", "images")
    os.makedirs(images_dir, exist_ok=True)

    # Step 1: Check available monitors and select the correct one
    with mss.mss() as sct:
        monitors = sct.monitors
        print(
            f"Available monitors: {monitors}"
        )  # Debugging output to show monitor list

        if monitor_index < 1 or monitor_index >= len(monitors):
            raise ValueError(
                f"Invalid monitor index {monitor_index}. Valid indexes: 1-{len(monitors) - 1}"
            )

        # Select monitor by index (1-based index)
        monitor = monitors[monitor_index + 1]
        print(
            f"Capturing screenshot from Monitor {monitor_index}: {monitor}"
        )  # Debugging output

        # Capture screenshot of the selected monitor
        screenshot = sct.grab(monitor)
        full_image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    # Save full screenshot if requested
    if save_full:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        full_image_path = os.path.join(images_dir, f"full_screenshot_{timestamp}.png")
        full_image.save(full_image_path)
        print(f"Full screenshot saved at: {full_image_path}")

    # Step 2: Perform OCR on the screenshot
    print("Performing OCR on screenshot...")
    reader = easyocr.Reader(["en"], gpu=True)
    img_np = np.array(full_image)  # Convert PIL Image to numpy array
    ocr_results = reader.readtext(img_np, detail=1)
    print(ocr_results)

    # Step 3: Find bounding boxes for all text markers
    found_boxes = []

    for marker in text_markers:
        matched = False
        for bbox, text, conf in ocr_results:
            if conf >= confidence_threshold and marker.lower() in text.lower():
                found_boxes.append(bbox)
                matched = True
                break  # Use the first match found
        if not matched:
            raise ValueError(
                f"Text marker '{marker}' not found with sufficient confidence."
            )

    # Step 4: Calculate the combined bounding box
    all_x = []
    all_y = []
    for box in found_boxes:
        for x, y in box:
            all_x.append(x)
            all_y.append(y)

    left = int(min(all_x))
    top = int(min(all_y))
    right = int(max(all_x))
    bottom = int(max(all_y))

    area_coordinates = (left, top, right, bottom)
    print(f"Found area coordinates: {area_coordinates}")

    # Step 5: Crop the partial image
    cropped_image = full_image.crop(area_coordinates)

    # Step 6: Save the cropped partial image
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    cropped_image_filename = f"cropped_area_{timestamp}.png"
    saved_path = os.path.join(images_dir, cropped_image_filename)
    cropped_image.save(saved_path)
    print(f"Cropped image saved at: {saved_path}")

    return saved_path, area_coordinates


if __name__ == "__main__":
    capture_partial_screenshot(
        ["Customer Details", "eNB Name"],
        save_full=True,
        confidence_threshold=0.4,
    )
