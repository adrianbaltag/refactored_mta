# # pylint: disable=import-outside-toplevel, invalid-name, too-many-arguments, too-many-locals, too-many-statements,line-too-long
# """This script captures a cropped area from a screenshot that contains multiple specified text markers.
# It uses the EasyOCR library for optical character recognition (OCR) and the mss library for screen capturing - on specified monitor"""

# import os
# import time

# import easyocr
# import mss
# import numpy as np
# from PIL import Image

# from my_packages.constants_module.constant_variables import MONITOR_INDEX


# def capture_partial_screenshot(
#     text_markers,
#     save_full=False,
#     confidence_threshold=0.7,
#     monitor_index=MONITOR_INDEX,
# ):
#     """
#     Capture a cropped area from a screenshot that contains multiple specified text markers.

#     Args:
#         text_markers (list[str]): List of text strings to find.
#         save_full (bool, optional): Save full screenshot before cropping. Defaults to False.
#         confidence_threshold (float, optional): OCR minimum confidence threshold. Defaults to 0.7.
#         monitor_index (int, optional): Monitor index (1 = primary monitor). Defaults to constant value.

#     Returns:
#         tuple[str, tuple]: (saved_path, (left, top, right, bottom))
#     """
#     # Prepare project and image directory paths
#     project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#     images_dir = os.path.join(project_root, "my_packages", "images")
#     os.makedirs(images_dir, exist_ok=True)

#     # Step 1: Check available monitors and select the correct one
#     with mss.mss() as sct:
#         monitors = sct.monitors
#         print(
#             f"Available monitors: {monitors}"
#         )  # Debugging output to show monitor list

#         if monitor_index < 1 or monitor_index >= len(monitors):
#             raise ValueError(
#                 f"Invalid monitor index {monitor_index}. Valid indexes: 1-{len(monitors) - 1}"
#             )

#         # Select monitor by index (1-based index)
#         monitor = monitors[monitor_index + 1]
#         print(
#             f"Capturing screenshot from Monitor {monitor_index}: {monitor}"
#         )  # Debugging output

#         # Capture screenshot of the selected monitor
#         screenshot = sct.grab(monitor)
#         full_image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

#     # Save full screenshot if requested
#     if save_full:
#         timestamp = time.strftime("%Y%m%d_%H%M%S")
#         full_image_path = os.path.join(images_dir, f"full_screenshot_{timestamp}.png")
#         full_image.save(full_image_path)
#         print(f"Full screenshot saved at: {full_image_path}")

#     # Step 2: Perform OCR on the screenshot
#     print("Performing OCR on screenshot...")
#     reader = easyocr.Reader(["en"], gpu=True)
#     img_np = np.array(full_image)  # Convert PIL Image to numpy array
#     ocr_results = reader.readtext(img_np, detail=1)
#     print(ocr_results)

#     # Step 3: Find bounding boxes for all text markers
#     found_boxes = []

#     for marker in text_markers:
#         matched = False
#         for bbox, text, conf in ocr_results:
#             if conf >= confidence_threshold and marker.lower() in text.lower():
#                 found_boxes.append(bbox)
#                 matched = True
#                 break  # Use the first match found
#         if not matched:
#             raise ValueError(
#                 f"Text marker '{marker}' not found with sufficient confidence."
#             )

#     # Step 4: Calculate the combined bounding box
#     all_x = []
#     all_y = []
#     for box in found_boxes:
#         for x, y in box:
#             all_x.append(x)
#             all_y.append(y)

#     left = int(min(all_x))
#     top = int(min(all_y))
#     right = int(max(all_x))
#     bottom = int(max(all_y))

#     area_coordinates = (left, top, right, bottom)
#     print(f"Found area coordinates: {area_coordinates}")

#     # Step 5: Crop the partial image
#     cropped_image = full_image.crop(area_coordinates)

#     # Step 6: Save the cropped partial image
#     timestamp = time.strftime("%Y%m%d_%H%M%S")
#     cropped_image_filename = f"cropped_area_{timestamp}.png"
#     saved_path = os.path.join(images_dir, cropped_image_filename)
#     cropped_image.save(saved_path)
#     print(f"Cropped image saved at: {saved_path}")

#     return saved_path, area_coordinates


# if __name__ == "__main__":
#     capture_partial_screenshot(
#         ["H3 Grid", "Copy"],
#         save_full=False,
#         confidence_threshold=0.7,
#     )

# # ! it working great, but need to be tested on different monitors and different text markers, also need a func to delete the additional dir creeeated to save the images"""


# pylint: disable=import-outside-toplevel, invalid-name, too-many-arguments, too-many-locals, too-many-statements,line-too-long,E1101
# cSpell:ignore mss,pyautogui,pygetwindow,ImageEnhance,ImageDraw,easyocr,ImageGrab,readtext,frombytes,ImageGrab,LANCZOS,ImageDraw,ImageEnhance,ImageGrab,ImageDraw,ImageEnhance,ImageGrab,ImageDraw,ImageEnhance
"""This script captures a cropped area from a screenshot that contains multiple specified text markers.
It uses the EasyOCR library for optical character recognition (OCR) and the mss library for screen capturing - on specified monitor"""

import os
import time
from typing import List

import easyocr
import mss
import numpy as np
from PIL import Image, ImageEnhance

from my_packages.constants_module.constant_variables import MONITOR_INDEX


def capture_partial_screenshot(
    text_markers: List[str],
    save_full: bool = False,
    confidence_threshold: float = 0.7,
    monitor_index: int = MONITOR_INDEX,
    zoom_factor: float = 2.0,
    zoom_sections: int = 4,
    enhance_contrast: float = 1.5,
    debug: bool = False,
):
    """
    Capture a cropped area from a screenshot that contains multiple specified text markers.
    Uses zoom-in scanning to better detect small text.

    Args:
        text_markers (list[str]): List of text strings to find.
        save_full (bool, optional): Save full screenshot before cropping. Defaults to False.
        confidence_threshold (float, optional): OCR minimum confidence threshold. Defaults to 0.7.
        monitor_index (int, optional): Monitor index (1 = primary monitor). Defaults to constant value.
        zoom_factor (float, optional): Factor to zoom in by when scanning for small text. Defaults to 2.0.
        zoom_sections (int, optional): Number of sections to divide screen into for zoomed scanning. Defaults to 4.
        enhance_contrast (float, optional): Factor to enhance contrast before OCR. Defaults to 1.5.
        debug (bool, optional): Save debug images during processing. Defaults to False.

    Returns:
        tuple[str, tuple]: (saved_path, (left, top, right, bottom))
    """
    # Prepare project and image directory paths
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    images_dir = os.path.join(project_root, "my_packages", "images")
    os.makedirs(images_dir, exist_ok=True)
    if debug:
        debug_dir = os.path.join(images_dir, "debug")
        os.makedirs(debug_dir, exist_ok=True)

    # Step 1: Check available monitors and select the correct one
    with mss.mss() as sct:
        monitors = sct.monitors
        print(f"Available monitors: {monitors}")

        if monitor_index < 1 or monitor_index >= len(monitors):
            raise ValueError(
                f"Invalid monitor index {monitor_index}. Valid indexes: 1-{len(monitors) - 1}"
            )

        # Select monitor by index (1-based index)
        monitor = monitors[monitor_index + 1]
        print(f"Capturing screenshot from Monitor {monitor_index}: {monitor}")

        # Capture screenshot of the selected monitor
        screenshot = sct.grab(monitor)
        full_image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    # Save full screenshot if requested
    if save_full:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        full_image_path = os.path.join(images_dir, f"full_screenshot_{timestamp}.png")
        full_image.save(full_image_path)
        print(f"Full screenshot saved at: {full_image_path}")

    # Step 2: Initialize OCR reader
    print("Initializing OCR reader...")
    reader = easyocr.Reader(["en"], gpu=True)

    # Step 3: First attempt - try full image OCR with contrast enhancement
    enhanced_image = enhance_image(full_image, enhance_contrast)
    if debug:
        enhanced_image.save(os.path.join(debug_dir, "enhanced_full.png"))

    img_np = np.array(enhanced_image)
    ocr_results = reader.readtext(img_np, detail=1)
    print(f"Initial OCR found {len(ocr_results)} text regions")

    # Step 4: If initial OCR doesn't find all markers, use zoom scanning
    found_markers = set()
    for bbox, text, conf in ocr_results:
        for marker in text_markers:
            if conf >= confidence_threshold and marker.lower() in text.lower():
                found_markers.add(marker)

    # If we haven't found all markers, try zoomed sections
    if len(found_markers) < len(text_markers):
        print(f"Not all markers found in initial scan. Found: {found_markers}")
        print(f"Performing zoomed scanning with factor {zoom_factor}...")

        # Prepare to store all OCR results from zoomed sections
        all_ocr_results = ocr_results.copy()

        # Divide the image into sections and scan each with zoom
        width, height = full_image.size
        section_width = width // zoom_sections
        section_height = height // zoom_sections

        for row in range(zoom_sections):
            for col in range(zoom_sections):
                # Calculate section coordinates
                left = col * section_width
                top = row * section_height
                right = min((col + 1) * section_width, width)
                bottom = min((row + 1) * section_height, height)

                # Extract and zoom the section
                section = full_image.crop((left, top, right, bottom))
                zoomed_section = section.resize(
                    (
                        int(section.width * zoom_factor),
                        int(section.height * zoom_factor),
                    ),
                    Image.LANCZOS,
                )

                # Enhance contrast
                zoomed_section = enhance_image(zoomed_section, enhance_contrast)

                if debug:
                    zoomed_section.save(
                        os.path.join(debug_dir, f"zoomed_section_{row}_{col}.png")
                    )

                # Perform OCR on zoomed section
                section_np = np.array(zoomed_section)
                section_results = reader.readtext(section_np, detail=1)

                # Adjust bounding box coordinates to match original image
                for i, (bbox, text, conf) in enumerate(section_results):
                    adjusted_bbox = []
                    for x, y in bbox:
                        # Convert from zoomed coordinates back to original section coordinates
                        orig_x = (x / zoom_factor) + left
                        orig_y = (y / zoom_factor) + top
                        adjusted_bbox.append((orig_x, orig_y))
                    section_results[i] = (adjusted_bbox, text, conf)

                # Add to overall results
                all_ocr_results.extend(section_results)
                print(f"Section {row},{col}: Found {len(section_results)} text regions")

        ocr_results = all_ocr_results

    # Step 5: Find bounding boxes for all text markers
    found_boxes = []
    found_markers = set()
    marker_details = {}

    print("OCR Results:")
    for bbox, text, conf in ocr_results:
        print(f"Text: {text}, Confidence: {conf}")
        for marker in text_markers:
            if conf >= confidence_threshold and marker.lower() in text.lower():
                found_boxes.append(bbox)
                found_markers.add(marker)
                marker_details[marker] = {
                    "bbox": bbox,
                    "confidence": conf,
                    "full_text": text,
                }
                print(f"Found marker: '{marker}' in '{text}' with confidence {conf}")
                break

    # Check if all markers were found
    missing_markers = set(text_markers) - found_markers
    if missing_markers:
        # Try with lower confidence as fallback
        fallback_threshold = confidence_threshold * 0.7
        print(f"Trying fallback with lower confidence threshold: {fallback_threshold}")
        for marker in missing_markers.copy():
            for bbox, text, conf in ocr_results:
                if conf >= fallback_threshold and marker.lower() in text.lower():
                    found_boxes.append(bbox)
                    found_markers.add(marker)
                    missing_markers.remove(marker)
                    marker_details[marker] = {
                        "bbox": bbox,
                        "confidence": conf,
                        "full_text": text,
                    }
                    print(
                        f"Found marker (fallback): '{marker}' in '{text}' with confidence {conf}"
                    )
                    break

    if missing_markers:
        raise ValueError(
            f"Text markers not found: {missing_markers}. "
            f"Try increasing zoom_factor or reducing confidence_threshold."
        )

    # Step 6: Calculate the combined bounding box
    all_x = []
    all_y = []
    for box in found_boxes:
        for x, y in box:
            all_x.append(x)
            all_y.append(y)

    # Add padding to the bounding box
    padding = 10
    left = max(0, int(min(all_x)) - padding)
    top = max(0, int(min(all_y)) - padding)
    right = min(full_image.width, int(max(all_x)) + padding)
    bottom = min(full_image.height, int(max(all_y)) + padding)

    area_coordinates = (left, top, right, bottom)
    print(f"Found area coordinates: {area_coordinates}")

    # Step 7: Crop the partial image
    cropped_image = full_image.crop(area_coordinates)

    # Step 8: Save the cropped partial image
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    cropped_image_filename = f"cropped_area_{timestamp}.png"
    saved_path = os.path.join(images_dir, cropped_image_filename)
    cropped_image.save(saved_path)
    print(f"Cropped image saved at: {saved_path}")

    # Save debug visualization if requested
    if debug:
        debug_image = full_image.copy()
        from PIL import ImageDraw

        draw = ImageDraw.Draw(debug_image)
        draw.rectangle(area_coordinates, outline="red", width=2)
        for marker, details in marker_details.items():
            draw.polygon(details["bbox"], outline="green", width=2)
            # Add label
            draw.text(
                (details["bbox"][0][0], details["bbox"][0][1] - 10),
                f"{marker}: {details['confidence']:.2f}",
                fill="blue",
            )
        debug_image.save(os.path.join(debug_dir, f"debug_overlay_{timestamp}.png"))

    return saved_path, area_coordinates


def enhance_image(image, contrast_factor=1.5):
    """Enhance image contrast to improve OCR text detection"""
    enhancer = ImageEnhance.Contrast(image)
    enhanced = enhancer.enhance(contrast_factor)
    # You can add more enhancements here if needed
    return enhanced


if __name__ == "__main__":
    capture_partial_screenshot(
        ["H3 Grid", "More Details"],
        save_full=False,
        confidence_threshold=0.7,
        zoom_factor=2.5,
        zoom_sections=4,
        enhance_contrast=1.5,
        debug=False,
    )
