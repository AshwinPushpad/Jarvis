import os

## launch a program
app = "code"
# os.startfile(f"{app}.exe")    # doesn't work on sm apps
# os.system(f"start {app}")     # most effective

import pygetwindow as gw
now = gw.getActiveWindow()
now.restore()


import pyautogui
# Go Back
pyautogui.hotkey("alt", "left")  # Works in Chrome, Edge, File Explorer
# Go Forward
pyautogui.hotkey("alt", "right")  # Works in Chrome, Edge, File Explorer


## Scroll
pyautogui.scroll(500)  # Scroll up
pyautogui.scroll(-500)  # Scroll down


# # Press any where with context
import pyautogui

image_location = pyautogui.locateOnScreen("image.png", confidence=0.8)

if image_location:
    pyautogui.click(image_location)  # Clicks on the detected button
else:
    print("image not found!")

