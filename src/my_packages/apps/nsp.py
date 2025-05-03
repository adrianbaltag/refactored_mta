# pylint:disable=W0105,C0413
# ruff: noqa: E402
"""This script holds the logic for the nsp application."""

"""WIP -NSP NOT WORKING - RETEST THE SCRIPT BY PIECES!!!!!!"""
import time

import keyboard
import pyautogui as pg

from my_packages.constants_module.constant_variables import MONITOR_INDEX
from my_packages.constants_module.urls import URL_NSP
from my_packages.ocr_module.capture_and_click import capture_and_click
from my_packages.ocr_module.capture_partial_screenshot import capture_partial_screenshot
from my_packages.ocr_module.click_icon import click_icon
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

    # Create the tool
    capture_partial_screenshot(
        ["eNodeB", "Last used (UTC)"],
        save_full=True,
        confidence_threshold=0.7,
    )

    # Cick on thr "home" icon
    click_icon(
        "nsp-home-icon.png",
    )
    time.sleep(5)  # Wait for the screenshot to be taken
    # Clic on x to close pop up
    click_icon(
        "x.png",
        monitor_index=MONITOR_INDEX,
        click=True,
    )
    time.sleep(3)  # Wait for the screenshot to be taken
    # Click on "Summary" tab
    capture_and_click(
        "SCREENSHOT",
        "Summary",
    )
    time.sleep(3)  # Wait for the screenshot to be taken

    capture_and_click("SCREENSHOT", "Ticket Number")
    time.sleep(1)  # Wait for the screenshot to be taken
    capture_and_click("SCREENSHOT", "Ticket Number")

    time.sleep(2)  # Wait for the screenshot to be taken
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
    time.sleep(10)  # Wait for the page to load

    # # Take a screenshot that includes both words
    # # saved_picture, picture_location = screenshot_tool.capture_area_by_multiple_text(
    # #     ["Customer Details", "Volte"],
    # #     confidence=0.7,
    # #     monitor_index=2,
    # # )
    capture_partial_screenshot(
        ["Customer Details", "Volte"],
        save_full=True,
        confidence_threshold=0.4,
    )
    time.sleep(1)

    click_icon("marker.png", threshold=0.7)
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("marker.png", threshold=0.7)
    time.sleep(3)  # Wait for the screenshot to be taken

    # # screenshot_tool.capture_area_by_multiple_text(
    # #     ["H3 Grid", "More Details"],
    # #     confidence=0.7,
    # #     monitor_index=2,
    # # )
    capture_partial_screenshot(
        ["H3 Grid", "More Details"],
        save_full=True,
        confidence_threshold=0.5,
    )
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("layers.png", threshold=0.5, click=True)
    time.sleep(3)  # Wait for the screenshot to be taken
    click_icon("outdoor.png", threshold=0.5, click=True)

    time.sleep(1)

    click_icon("marker.png", threshold=0.7, click=True)
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("marker.png", threshold=0.7, click=True)
    time.sleep(1)  # Wait for the screenshot to be taken

    # # screenshot_tool.capture_area_by_multiple_text(
    # #     ["H3 Grid", "More Details"],
    # #     confidence=0.7,
    # #     monitor_index=2,
    # # )
    capture_partial_screenshot(
        ["H3 Grid", "More Details"],
        save_full=True,
        confidence_threshold=0.5,
    )
    time.sleep(1)  # Wait for the screenshot to be taken
    click_icon("click-volte.png", threshold=0.5, click=True)
    time.sleep(1)  # Wait for the screenshot to be taken
    pg.scroll(-700)  # Scroll down the page
    time.sleep(1)  # Wait for the scroll to complete

    # click on ex[port to download the file
    click_icon("export.png", threshold=0.5, click=True)
    # pg.scroll(-1000)  # Scroll udown the page
    # time.sleep(1)  # Wait for the scroll to complete

    # gET THE SITES
    # result = screenshot_tool.capture_area_by_multiple_text(
    #     ["eNB Name", "Search"],
    #     confidence=0.7,
    #     monitor_index=2,
    # )

    # print(result)

    """close the browser"""
    # keyboard.press_and_release("ctrl+w")


if __name__ == "__main__":
    nsp()
