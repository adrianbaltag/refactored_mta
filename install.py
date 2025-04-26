#!/usr/bin/env python
# pylint: disable=C0301
"""
Setup script to install the package and its CUDA-enabled PyTorch dependencies.
"""

import subprocess
import sys


def install():
    """_summary__
    This function installs the package and its dependencies, including a CUDA-enabled version of PyTorch, GPU version.
    It first ensures that the `uv` package is installed in the virtual environment, then installs the package itself and its basic dependencies.
    """
    # First ensure uv is installed in the virtual environment
    print("Ensuring UV is installed...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "uv"])

    print("Installing package and basic dependencies...")
    subprocess.check_call([sys.executable, "-m", "uv", "pip", "install", "-e", "."])

    print("Removing CPU version of PyTorch...")
    # For each package, uninstall separately without -y flag
    for package in ["torch", "torchvision", "torchaudio"]:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "uv", "pip", "uninstall", package]
            )
        except subprocess.CalledProcessError:
            print(f"Note: {package} was not installed or couldn't be removed.")

    print("Installing PyTorch with CUDA support...")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "uv",
            "pip",
            "install",
            "torch>=2.6.0",
            "torchvision>=0.21.0",
            "torchaudio>=2.6.0",
            "--index-url",
            "https://download.pytorch.org/whl/cu126",
        ]
    )

    print("Installation complete!")


if __name__ == "__main__":
    install()
