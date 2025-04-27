# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name, too-many-branches, too-many-locals, too-many-statements, broad-except
import subprocess
import time

import screeninfo
from pywinauto import findwindows
from pywinauto.application import Application

# pylint: disable=import-error
from my_packages.constants_module.constant_variables import MONITOR_INDEX
from my_packages.constants_module.urls import URL_FORMY


def open_app(url, index=None):
    """__summary__:
    This function opens a new browser window on a specific monitor with the provided URL.
    Windows-only implementation.
    args:
        url: The URL to open in the browser.
        index: The index of the monitor to open the browser on (0-based).
    """
    monitors = screeninfo.get_monitors()

    for i, monitor in enumerate(monitors):
        print(
            f"Monitor {i}: X={monitor.x}, Y={monitor.y}, Width={monitor.width}, Height={monitor.height}"
        )

    # Adjust based on setup (2 = left monitor - home setup)
    target_monitor_index = index
    target_monitor = monitors[target_monitor_index]

    # Open Chrome in a new window
    try:
        subprocess.Popen(
            [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                url,
                "--new-window",
            ]
        )
    except FileNotFoundError:
        print("Chrome not found, trying default browser.")
        subprocess.Popen(["start", "chrome", url, "--new-window"], shell=True)

    time.sleep(5)  # Wait for the browser to appear (increased sleep time)

    try:
        # Wait for the Chrome window to appear
        chrome_window = None
        for _ in range(10):  # Try up to 10 times (with 1-second intervals)
            # Look for windows with "Chrome" in the title
            windows = findwindows.find_windows(title_re=".*Chrome.*")
            if windows:
                chrome_window = windows[0]
                break
            time.sleep(1)

        if chrome_window:
            # Connect to the Chrome window using its handle
            app = Application().connect(handle=chrome_window)
            window = app.top_window()  # Get the top window (first Chrome window)

            if window:
                # Restore window in case it is minimized !!!!
                window.restore()

                # Move the browser window to the left monitor
                window.move_window(
                    target_monitor.x,
                    target_monitor.y,
                    width=target_monitor.width,
                    height=target_monitor.height,
                )

                #  bring the window to the foreground
                window.set_focus()

            time.sleep(1)  # Give it a second
        else:
            print("No Chrome window found after several attempts.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    open_app(URL_FORMY, index=MONITOR_INDEX)
