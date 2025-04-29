# pylint:disable=W0012,E1101
# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name, too-many-branches, too-many-locals, too-many-statements, broad-except
import os

import cv2
import easyocr

# from my_packages.constants_module.constant_variables import REMEDY_SCREENSHOT_INDEX


def read_image(img_index: int) -> dict:
    """
    Read an image by its index and return the extracted text as a dictionary.

    Args:
        img_index: The index of the image to read

    Returns:
        A dictionary with paragraph numbers as keys and extracted text as values
    """
    # Get the current script directory
    current_dir = os.path.dirname(__file__)
    print(f"Current directory: {current_dir}")

    # go up one level to the parent directory where 'img_to_read' is located
    parent_dir = os.path.dirname(current_dir)
    # Define the image folder path (assuming 'img_to_read' is at the same level as the current directory)
    img_folder = os.path.join(parent_dir, "img_to_read")
    print(f"Image folder path: {img_folder}")

    # Get all image files from the folder
    image_files = [
        f for f in os.listdir(img_folder) if f.endswith((".png", ".jpg", ".jpeg"))
    ]
    print(f"Found image files: {image_files}")

    # Sort the images to ensure consistent indexing
    image_files.sort()

    # Get the image path based on the index
    if img_index < 0 or img_index >= len(image_files):
        raise ValueError(
            f"Image index out of range. Valid range: 0-{len(image_files) - 1}"
        )

    img_path = os.path.join(img_folder, image_files[img_index])
    print(f"Reading image from: {img_path}")

    # Create an EasyOCR reader instance with English language support and GPU acceleration
    reader = easyocr.Reader(["en"], gpu=True)

    # Read the image using OpenCV
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: Could not read the image {img_path}")
        return {}

    # Use EasyOCR to read the text from the image
    result = reader.readtext(img, detail=0, paragraph=True)
    print(result)

    ticket_number = "Trouble-ID"
    try:
        index = result.index(ticket_number)
    except ValueError:
        print(f"Element '{ticket_number}' not found in the result list.")
        ticket = "Not found"
    else:
        ticket = result[index + 1]
    print(f"Ticket number: {ticket}")

    cx_mdn = "MDN"
    try:
        index = result.index(cx_mdn)
    except ValueError:
        print(f"Element '{cx_mdn}' not found in the result list.")
        mdn = "Not found"
    else:
        mdn = result[index + 1]
    print(f"MDN: {mdn}")

    prob_desc = "Problem Description"
    try:
        index = result.index(prob_desc)
    except ValueError:
        print(f"Element '{prob_desc}' not found in the result list.")
        issue = "Not found"
    else:
        issue = result[index + 1]
    print(f"Problem description: {issue}")

    # Return a dictionary with the extracted information
    return {"ticket": ticket, "mdn": mdn, "issue": issue}


if __name__ == "__main__":
    read_image(0)
