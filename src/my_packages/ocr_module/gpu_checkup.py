"""This script check if CUDA is available on the system in order to use GPU with Torch and print GPU info"""

import pyautogui
import torch


def gpu_checkup():
    """Check if CUDA is available and print GPU information."""
    print("CUDA Available:", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("Number of GPUs:", torch.cuda.device_count())
        print("GPU Name:", torch.cuda.get_device_name(0))
    else:
        print("No GPU found. Using CPU version.")

    print("\nPyTorch version:", torch.__version__)
    print("PyAutoGUI version:", pyautogui.__version__)


if __name__ == "__main__":
    print("Running GPU checkup...")
    gpu_checkup()
