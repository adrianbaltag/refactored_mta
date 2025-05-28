import time

import keyboard
import pyautogui as pg

from my_packages.constants_module.urls import URL_MTAS
from my_packages.docx_module.update_word_docx import update_word_docx
from my_packages.ocr_module.capture_and_click import capture_and_click
from my_packages.ocr_module.capture_partial_screenshot import capture_partial_screenshot
from my_packages.ocr_module.click_icon import click_icon
from my_packages.ocr_module.crop_image_by_index import crop_image_by_index
from my_packages.utils.get_mdn import get_mdn
from my_packages.utils.open_app import open_app


def mtas():
    """__summary__:Main function to execute the MTAS logic.
    It opens the MTAS URL, captures screenshots, and update the word doc.

    """
    open_app(URL_MTAS)  # Open the MTAS URL in the default web browser
    time.sleep(2)  # Wait for the form to load
    capture_and_click(
        "SCREENSHOT", "Customer Operations"
    )  # select same index as open_app
    time.sleep(1)  # Wait for the screenshot to be taken
    capture_and_click("SCREENSHOT", "Verify")  # select same index as open_app
    time.sleep(1)  # Wait for the screenshot to be taken
    capture_and_click(
        "SCREENSHOT", "Verify Subscriber"
    )  # select same index as open_app
    """logic for clean slate for mtas"""

    time.sleep(3)  # Wait for the click to register
    pg.scroll(-300)  # Scroll down the page
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("mtas-clear-results.png")
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("mtas-ok-close-pg.png")
    """'end of clean slate logic for mtas"""

    mdn = get_mdn()  # Call the decorated get_mdn function to get the MDN number
    print(f"This is the mdn {mdn}")
    click_icon("mtas-mdn.png")  # select same index as open_app
    # add mdn to the input field
    keyboard.write(mdn)
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("volte_mtas.png")
    time.sleep(1)  # Wait for the screenshot to be taken
    capture_and_click("SCREENSHOT", "Send Transaction")  # select same index as open_app
    time.sleep(7)  # Wait for the screenshot to be taken
    pg.scroll(-900)  # Scroll down the page
    time.sleep(1)  # Wait for the screenshot to be taken
    capture_partial_screenshot(
        [
            "Hide Results",
            "Duplicate Window",
        ],
        save_full=False,
        confidence_threshold=0.7,
        zoom_factor=2.5,
        zoom_sections=4,
        enhance_contrast=1.5,
        debug=False,
    )  # select same index as open_app
    time.sleep(1)  # Wait for the screenshot to be taken
    # # crop the mtas img
    crop_image_by_index(3)
    time.sleep(1)  # Wait for the screenshot to be taken
    capture_and_click("SCREENSHOT", "SIMOTA1")  # select same index as open_app
    time.sleep(1)  # Wait for the screenshot to be taken
    pg.scroll(-300)  # Scroll down the page
    time.sleep(1)  # Wait for the screenshot to be taken
    capture_partial_screenshot(
        [
            "<resultData>",
            "</cin>",
        ],
        save_full=False,
        confidence_threshold=0.7,
        zoom_factor=2.5,
        zoom_sections=4,
        enhance_contrast=1.5,
        debug=False,
    )  # select same index as open_app

    time.sleep(1)  # Wait for the screenshot to be taken
    # # update word doc
    update_word_docx([4, 5], width=6)  # update the docx file with mtas screenshot


if __name__ == "__main__":
    mtas()
