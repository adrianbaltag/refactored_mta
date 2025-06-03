"""This script hold the logic for mars app."""

import time

import keyboard
import pyautogui as pg

from my_packages.constants_module.urls import URL_MARS
from my_packages.docx_module.update_word_docx import update_word_docx
from my_packages.ocr_module.capture_full_screenshot import capture_full_screenshot

# open mars app
from my_packages.ocr_module.click_icon import click_icon
from my_packages.ocr_module.crop_by_index_top_only import crop_by_index_top_only
from my_packages.utils.get_mdn import get_mdn
from my_packages.utils.move_file_by_index import move_file_by_index
from my_packages.utils.open_app import open_app


# ! ask for type of mars app:4g / 5g
def mars_records_type():
    """_summary_:Function to ask the user for the type of MARS records they want to access.
    It prompts the user to enter '4' for 4G records or '5' for 5G records and calls the appropriate function based on the input.
    If the input is not '5', it defaults to 4G records."""
    input("Enter the type of MARS records you want to access (4 - 4G / 5 - 5G): ")

    if input == "4":
        print("You have selected 4G records.")
        mars4g()
    else:
        print("You have selected 5G records.")
        mars5g()


# # '''mars 5g working'''
def mars5g():
    """__summary__:Main function to execute the MARS logic -5G.
    It opens the MARS URL in the default web browser.

    """
    mdn = get_mdn()  # Get the MDN from the user input
    time.sleep(1)  # Wait for the MDN to be processed
    open_app(URL_MARS)  # Open the MARS URL in the default web browser
    time.sleep(2)  # Wait for the MARS page to load
    click_icon("mars-login.png")  # Click on the "Verify" button
    time.sleep(3)  # Wait for the login to complete

    click_icon("mars-call-record.png")  # Click on the "Verify" button

    click_icon("5g.png")  # Click on the "Verify" button
    time.sleep(1)  # Wait for the 5G option to be selected
    click_icon("5g-records.png")  # Click on the "Verify" button
    time.sleep(1)  # Wait for the 5G records to be selected
    click_icon("5g-add-mdn.png")  # Click on the "Verify" button
    time.sleep(1)  # Wait for the MDN input to be ready
    keyboard.write(mdn)  # Type the MDN into the input field
    click_icon("1week.png")  # Click on the "Submit" button
    time.sleep(3)  # Wait for the MDN to be processed

    click_icon("arrow-mars.png")  # Click on the "Submit" button

    pg.scroll(-9000)  # Scroll down the page

    capture_full_screenshot()
    time.sleep(1)  # Wait for the screenshot to be taken
    crop_by_index_top_only(0)
    time.sleep(1)  # Wait for the screenshot to be taken
    # move the mars screenshot to images
    move_file_by_index("src/my_packages/img_to_read", "src/my_packages/images", 1)
    # # update word doc
    update_word_docx([7], width=6)  # update the docx file with mtas screenshot
    time.sleep(1)  # Wait for the screenshot to be taken


"""mars 4g"""


def mars4g():
    """__summary__:Main function to execute the MARS logic -4G.
    It opens the MARS URL in the default web browser.

    """
    mdn = get_mdn()  # Get the MDN from the user input
    time.sleep(1)  # Wait for the MDN to be processed
    open_app(URL_MARS)  # Open the MARS URL in the default web browser
    time.sleep(2)  # Wait for the MARS page to load
    click_icon("mars-login.png")  # Click on the "Verify" button
    time.sleep(3)  # Wait for the login to complete

    click_icon("mars-call-record.png")  # Click on the "Verify" button

    click_icon("data-record.png")  # Click on the "Verify" button
    time.sleep(1)  # Wait for the 5G option to be selected
    click_icon("lte.png")  # Click on the "Verify" button
    time.sleep(1)  # Wait for the 5G records to be selected
    click_icon("volte-cdr-mars.png")  # Click on the "Verify" button
    time.sleep(1)  # Wait for the MDN input to be ready
    click_icon("current-mars.png")  # Click on the "Verify" button
    time.sleep(1)  # Wait for the MDN input to be ready
    click_icon("5g-add-mdn.png")  # Click on the "Verify" button
    #     time.sleep(1)  # Wait for the MDN input to be ready
    keyboard.write(mdn)  # Type the MDN into the input field
    time.sleep(1)  # Wait for the MDN input to be ready
    click_icon("1week.png")  # Click on the "Submit" button
    time.sleep(3)  # Wait for the MDN to be processed

    capture_full_screenshot()
    time.sleep(1)  # Wait for the screenshot to be taken
    crop_by_index_top_only(0)
    # time.sleep(1)  # Wait for the screenshot to be taken
    # move the mars screenshot to images
    move_file_by_index("src/my_packages/img_to_read", "src/my_packages/images", 1)
    # # update word doc
    update_word_docx([7], width=6)  # update the docx file with mtas screenshot
    time.sleep(1)  # Wait for the screenshot to be taken


if __name__ == "__main__":
    mars_records_type()
