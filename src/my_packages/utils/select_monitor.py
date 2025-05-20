"""
This module contains a function to select a monitor based on its index."""

import screeninfo

from my_packages.constants_module.constant_variables import MONITOR_INDEX


def select_monitor(index=MONITOR_INDEX):
    """__summary__:
    This function selects a monitor based on the provided index and prints its details.
    It also returns the selected monitor object.
    args:
        index: The index of the monitor to select (0-based) --> assigned the constant MONOITOR_INDEX.
    """
    monitors = screeninfo.get_monitors()

    for i, monitor in enumerate(monitors):
        print(
            f"Monitor {i}: X={monitor.x}, Y={monitor.y}, Width={monitor.width}, Height={monitor.height}"
        )

    target_monitor_index = index
    target_monitor = monitors[target_monitor_index]

    print(
        f"Selected Monitor {target_monitor_index}: X={target_monitor.x}, Y={target_monitor.y}, Width={target_monitor.width}, Height={target_monitor.height}"
    )
    return target_monitor


if __name__ == "__main__":
    select_monitor()
