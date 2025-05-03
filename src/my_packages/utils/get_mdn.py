"""This module contains a function to get the MDN (Mobile Directory Number) from the remedy screenshot."""

from my_packages.ocr_module.read_image import read_image


def get_mdn() -> str:
    """
    Extracts the MDN  from the remedy screenshot.



    Returns:
        str: The extracted MDN.
    """
    res = read_image(0)
    mdn = res["mdn"]
    print(mdn)
    return mdn


if __name__ == "__main__":
    get_mdn()
