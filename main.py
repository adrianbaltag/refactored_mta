import time

from src.my_packages.apps.nsp import nsp
from src.my_packages.apps.remedy import remedy


def main():
    remedy()
    time.sleep(5)  # Wait for the remedy function to complete
    nsp()


if __name__ == "__main__":
    main()
