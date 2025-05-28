import time

from src.my_packages.apps.mtas import mtas
from src.my_packages.apps.nsp import nsp
from src.my_packages.apps.remedy import remedy


def main():
    """_summary_: Main function to execute the workflow of the application."""
    remedy()
    time.sleep(3)  # Wait for the remedy function to complete
    nsp()
    time.sleep(3)  # Wait for the nsp function to complete
    mtas()


if __name__ == "__main__":
    main()
