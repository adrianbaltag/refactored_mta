"""This module contains functions to extract most used sites from OCR data."""

import os
from collections import Counter, defaultdict

import easyocr
import numpy as np
from PIL import Image


def crop_left_side_by_index(index):
    """
    Crops the left side of an image (100px wide default) based on its index in the 'src/my_packages/images' directory,
    and saves it with a new name in the 'cropped_img' folder, then reads the cropped image using EasyOCR.
    returns the detected text from the image.

    :param index: Index of the image to crop.
    :return: a list of detected text strings from the cropped image.
    """
    clean_list = []
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")

    # Define the image directory path
    image_dir = os.path.join(current_dir, "..", "images")  # Path to the images folder
    print(f"Image directory: {image_dir}")

    # Check if the 'cropped_img' folder exists, if not, create it
    output_dir = "cropped_img"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all image filenames from the specified directory
    image_files = [
        f
        for f in os.listdir(image_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    print(f"Found {len(image_files)} image(s) in the directory.")

    # Check if the index is valid
    if index < 0 or index >= len(image_files):
        print("Invalid index. Please provide a valid index.")
        return

    # Get the image file based on the index
    image_file = image_files[index]
    image_path = os.path.join(image_dir, image_file)
    print(f"Processing image: {image_file} from path: {image_path}")

    try:
        # Open the image
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Define the cropping box (left side with width 100px)
    width, height = img.size
    crop_box = (0, 0, 100, height)  # (left, top, right, bottom)
    print(f"Cropping image with box: {crop_box}")

    try:
        # Crop the image
        cropped_img = img.crop(crop_box)
    except Exception as e:
        print(f"Error cropping image: {e}")
        return

    # Save the cropped image
    output_path = os.path.join(output_dir, f"cropped_{image_file}")
    print(f"Saving cropped image to: {output_path}")

    try:
        cropped_img.save(output_path)
    except Exception as e:
        print(f"Error saving cropped image: {e}")
        return

    # Convert the cropped image to a NumPy array
    cropped_img_np = np.array(cropped_img)

    # Initialize the EasyOCR reader
    reader = easyocr.Reader(["en"], gpu=True)

    # Perform OCR on the cropped image
    try:
        result = reader.readtext(cropped_img_np)

    except Exception as e:
        print(f"Error reading text from image: {e}")

    # readable result
    for res in result:
        # The text is the second item in the tuple
        detected_text = res[1]
        print(f"Detected Text: {detected_text}")
        print(type(detected_text))  # Print the type of detected_text
        # #! Append the detected text to the clean list --> just the enodeB
        clean_list.append(detected_text)
    print(clean_list[2:-1])
    return clean_list[2:-1]


# # info: """This script extracts the most common base and suffix from a list of sites returned by crop_left_side_by_index func."""


# def extract_base_and_suffix(val):
#     """summary: Extracts the base and suffix from a given value.
#     Args:
#         val (str): The value to be processed."""
#     # Normalize to dot as separator
#     val = val.replace(",", ".")

#     # Handle cases where there's an underscore but no dot (like '58_23144')
#     if "_" in val and "." not in val:
#         # Split by underscore
#         parts = val.split("_")
#         if len(parts) == 2:
#             prefix = parts[0]
#             numbers = parts[1]

#             # For values like '58_23144'
#             if len(numbers) >= 4:
#                 base = f"{prefix}_{numbers[:3]}"
#                 # Use a fixed pattern suffix for this special case
#                 suffix = "4.4"  # Match the expected pattern
#                 return base, suffix

#     # Handle cases with both underscores and dots
#     if "_" in val and "." in val:
#         # Split by underscore first
#         main_parts = val.split("_")
#         if len(main_parts) == 2:
#             prefix = main_parts[0]
#             rest = main_parts[1]

#             # Find the first dot in the rest part
#             dot_index = rest.find(".")
#             if dot_index != -1:
#                 base = f"{prefix}_{rest[:dot_index]}"
#                 suffix = rest[dot_index + 1 :]  # Everything after the first dot
#                 return base, suffix

#     # Default case - just split by first dot
#     parts = val.split(".")
#     base = parts[0]
#     suffix = ".".join(parts[1:]) if len(parts) > 1 else ""

#     return base, suffix


def extract_base_and_suffix(val):
    """
    Extracts the base and suffix from a given value.
    Args:
        val (str): The value to be processed.
    Returns:
        tuple: (base, suffix)
    """
    # Check if val is a string
    if not isinstance(val, str):
        return "", ""

    # Normalize to dot as separator
    val = val.replace(",", ".")

    # For debugging
    print(f"Processing value: {val}")

    # Handle cases with underscore
    if "_" in val:
        parts = val.split("_")
        if len(parts) == 2:
            prefix = parts[0]
            rest = parts[1]

            # Check if there are digits at the start of 'rest'
            base_part = ""
            suffix_part = ""

            # For values like '109_295.3.7', separate the digits before first dot as base
            if "." in rest:
                dot_index = rest.find(".")
                base_part = rest[:dot_index]
                suffix_part = rest[dot_index + 1 :]
                return f"{prefix}_{base_part}", suffix_part

            # For values like '109_2953.1', we need to determine how to split
            # Assuming the base is always 3 digits after the underscore
            elif len(rest) >= 3:
                base_part = rest[:3]
                if len(rest) > 3:
                    if "." in rest[3:]:
                        suffix_part = rest[3:]  # Include the dot in suffix
                    else:
                        # If no dot in the remaining part, assume it's a suffix
                        suffix_part = rest[3:]
                return f"{prefix}_{base_part}", suffix_part

    # Default case - split by first dot
    parts = val.split(".")
    base = parts[0]
    suffix = ".".join(parts[1:]) if len(parts) > 1 else ""

    return base, suffix


# # info: """This script returns the most used site/s."""


# def get_most_common_site(index):
#     """summary: This function retrieves the most common site from a list of values.
#     Args:
#         index (int): The index of the image to be processed.
#     Returns:
#         str: The most common site in the format 'base/suffix1/suffix2/...'"""
#     values = crop_left_side_by_index(index)

#     base_to_suffixes = defaultdict(list)

#     for val in values:
#         base, suffix = extract_base_and_suffix(val)
#         if base and suffix:  # Only consider entries with both base and suffix
#             base_to_suffixes[base].append(suffix)

#     if not base_to_suffixes:
#         return "No valid values with suffixes found"

#     # Count how many times each base appears
#     base_counts = Counter()
#     for base, suffixes in base_to_suffixes.items():
#         base_counts[base] += len(suffixes)

#     # Find the most common base
#     most_common_base = base_counts.most_common(1)[0][0]
#     suffixes = base_to_suffixes[most_common_base]

#     # Keep only unique suffixes while preserving order of first appearance
#     unique_suffixes = []
#     for suffix in suffixes:
#         if suffix not in unique_suffixes:
#             unique_suffixes.append(suffix)

#     # Construct the result
#     result = (
#         f"{most_common_base}/{'/'.join(unique_suffixes)}"
#         if unique_suffixes
#         else most_common_base
#     )
#     return result


def get_most_common_site(index):
    """
    This function retrieves the most common site from a list of values.
    Args:
        index (int): The index of the image to be processed.
    Returns:
        str: The most common site in the format 'base/suffix1/suffix2/...'
    """
    values = crop_left_side_by_index(index)

    if not values:
        return "No values found in the image"

    # Debug the values
    print(f"Values from OCR: {values}")

    # Count occurrences of each base
    base_counter = Counter()
    # Track suffixes for each base
    base_to_suffixes = defaultdict(list)

    for val in values:
        base, suffix = extract_base_and_suffix(val)
        print(f"Extracted: {val} -> Base: {base}, Suffix: {suffix}")  # Debug line

        if base:  # Only count if we have a base
            base_counter[base] += 1
            if suffix:  # Only add suffix if it exists
                base_to_suffixes[base].append(suffix)

    if not base_counter:
        return "No valid bases found"

    # Find the most common base
    most_common_bases = base_counter.most_common()
    print(f"Base counts: {most_common_bases}")  # Debug line

    most_common_base = most_common_bases[0][0]
    suffixes = base_to_suffixes[most_common_base]

    print(f"Base {most_common_base} has suffixes: {suffixes}")  # Debug line

    # Keep only unique suffixes while preserving order of first appearance
    unique_suffixes = []
    for suffix in suffixes:
        if suffix not in unique_suffixes:
            unique_suffixes.append(suffix)

    # Construct the result
    result = (
        f"{most_common_base}/{'/'.join(unique_suffixes)}"
        if unique_suffixes
        else most_common_base
    )
    return result


if __name__ == "__main__":
    result = get_most_common_site(0)
    print("Most common site:", result)
