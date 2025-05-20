# pylint:disable=W0105,C0413
# ruff: noqa: E402
# cSpell:ignore pyautogui,Volte,
"""This script holds the logic for the nsp application."""

"""WIP -NSP NOT WORKING - RETEST THE SCRIPT BY PIECES!!!!!!"""
import time

import keyboard
import pyautogui as pg

from my_packages.constants_module.constant_variables import (
    ADJUSTMENT_MARKER,
    MONITOR_INDEX,
    SINR_SCREENSHOT_WIDTH,
    SITES_SCREENSHOT_WIDTH,
)
from my_packages.constants_module.urls import URL_NSP
from my_packages.docx_module.update_word_docx import update_word_docx
from my_packages.docx_module.update_word_text import update_word_text
from my_packages.ocr_module.capture_and_click import capture_and_click
from my_packages.ocr_module.capture_partial_screenshot import capture_partial_screenshot
from my_packages.ocr_module.click_icon import click_icon
from my_packages.ocr_module.nsp_extract_sites import get_most_common_site
from my_packages.utils.get_mdn import get_mdn
from my_packages.utils.open_app import open_app


def nsp():
    """__summary__:Main function to execute the nsp logic.
    It opens a specific URL, captures a screenshot, and processes the image to extract text.
    """
    open_app(
        URL_NSP
    )  # Open the form URL in the default web browser, on selected monitor index based
    time.sleep(5)  # Wait for the form to load
    mdn = get_mdn()  # Call the get_mdn function to get the MDN number

    capture_and_click("SCREENSHOT", "Enter MDN")  # select same index as open_app
    time.sleep(1)  # Wait for the screenshot to be taken
    keyboard.write(mdn)
    keyboard.press_and_release("enter")
    time.sleep(10)  # Wait for loading the pa

    # # click having degraded service
    capture_and_click("SCREENSHOT", "Subscriber")  # select same index as open_app
    time.sleep(1)  # Wait for the screenshot to be taken
    keyboard.press_and_release("enter")
    time.sleep(3)  # Wait for loading the page
    # # pyautogui  scroll down

    pg.scroll(-7000)  # Scroll down the page
    time.sleep(3)  # Wait for the scroll to complete

    # Take the partial screenshot that includes both words
    capture_partial_screenshot(
        ["eNodeB", "Last used (UTC)"],
        save_full=True,
        confidence_threshold=0.7,
    )

    # CLick on thr "home" icon
    click_icon(
        "nsp-home-icon.png",
    )
    time.sleep(5)  # Wait for the screenshot to be taken
    # Click on x to close pop up
    click_icon(
        "x.png",
        monitor_index=MONITOR_INDEX,
        click=True,
    )

    # todo: add logic for femto !!!??? - depending on tab loading time.....

    time.sleep(3)  # Wait for the screenshot to be taken
    # Click on "Summary" tab
    capture_and_click(
        "SCREENSHOT",
        "Summary",
    )
    time.sleep(5)  # Wait for the screenshot to be taken

    capture_and_click("SCREENSHOT", "Ticket Number")
    time.sleep(1)  # Wait for the screenshot to be taken
    capture_and_click("SCREENSHOT", "Ticket Number")

    time.sleep(3)  #
    capture_and_click(
        "SCREENSHOT",
        "MDN",
    )

    # # click to add the mdn
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon(
        "enter-number.png",
        monitor_index=MONITOR_INDEX,
        threshold=0.8,
        click=True,
    )
    time.sleep(1)  # Wait for the screenshot to be taken
    # # add the mdn number
    keyboard.write(mdn)
    time.sleep(1)  # Wait for the screenshot to be taken
    # # click submit icon
    click_icon(
        "submit-btn.png",
        monitor_index=MONITOR_INDEX,
        threshold=0.8,
        click=True,
    )
    time.sleep(1)  # Wait for the screenshot to be taken
    pg.scroll(-700)  # Scroll down the page
    time.sleep(5)  # Wait for the page to load

    click_icon("marker2.png", threshold=0.7, adjustment=ADJUSTMENT_MARKER)
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("marker2.png", threshold=0.7, adjustment=ADJUSTMENT_MARKER)
    time.sleep(3)  # Wait for the screenshot to be taken

    capture_partial_screenshot(
        ["H3 Grid", "More Details"],
        save_full=False,
        confidence_threshold=0.7,
        zoom_factor=2.5,
        zoom_sections=4,
        enhance_contrast=1.5,
        debug=False,
    )
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("layers.png", threshold=0.5, click=True)
    time.sleep(3)  # Wait for the screenshot to be taken
    click_icon("outdoor.png", threshold=0.5, click=True)

    time.sleep(3)

    click_icon("marker2.png", threshold=0.7, click=True, adjustment=ADJUSTMENT_MARKER)
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("marker2.png", threshold=0.7, click=True, adjustment=ADJUSTMENT_MARKER)
    time.sleep(1)  # Wait for the screenshot to be taken

    capture_partial_screenshot(
        ["H3 Grid", "More Details"],
        save_full=False,
        confidence_threshold=0.7,
        zoom_factor=2.5,
        zoom_sections=4,
        enhance_contrast=1.5,
        debug=False,
    )
    time.sleep(1)  # Wait for the screenshot to be taken

    # update the docx file with sites screenshot
    update_word_docx(
        [0], SITES_SCREENSHOT_WIDTH
    )  # update the docx file with sites screenshot
    time.sleep(1)

    # get the most common sites
    most_used_sites = get_most_common_site(0)
    update_word_text(most_used_sites)

    time.sleep(1)  # Wait for the screenshot to be taken
    # update with  sinr screenshot
    update_word_docx(
        [1], SINR_SCREENSHOT_WIDTH
    )  # update the docx file with INDOOR SINR screenshot
    time.sleep(1)
    update_word_docx(
        [1, 2], SINR_SCREENSHOT_WIDTH
    )  # update the docx file with OUTDOOR SINR screenshot
    time.sleep(1)
    """close the browser"""
    keyboard.press_and_release("ctrl+w")
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("nsp_leave.png", threshold=0.7, click=True)


if __name__ == "__main__":
    nsp()
