import pyautogui
import time

# Action Cords
WIFI = (1433, 484)
BLUETOOTH = (1596, 479)
NIGHT_MODE = (1793, 625)
BATTERY_SAVER = (1630, 626)
MIN_VOLUME = (1450, 865)
MAX_VOLUME = (1800, 865)

# Actions from Action menu
def toggle_action(cords):
    # Wifi
    # Get the current mouse position
    origin_x, origin_y = pyautogui.position()
    # Open Action Center (Windows shortcut: Win + A)
    pyautogui.hotkey("win", "a")
    time.sleep(.2)  # Wait for Action Center to open
    # Move cursor to toggle position (adjust based on your screen)
    x,y = cords
    pyautogui.click(x,y)  # Adjust coordinates for your screen
    pyautogui.hotkey("win", "a")
    pyautogui.moveTo(origin_x, origin_y)  # Get back
# toggle_action(cords=BLUETOOTH)


def get_mouse_cords():
    print("Move your cursor to the desired position in 2 seconds...")
    # pyautogui.hotkey("win", "a")
    time.sleep(4)  # Gives you time to move the cursor
    # Get and print the current mouse position
    x, y = pyautogui.position()
    print(f"Mouse Position: ({x}, {y})")
# pyautogui.hotkey("win", "a")
# get_mouse_cords()



# Volume
def volume(level='mute'):
    """
    Toggle volume to a specific level.
    Args:
    level (str or int): max, min, mute, up, down or int-value(0-100)
    """
    match level:
        case 'max':
            # level = 100
            toggle_action(cords=MAX_VOLUME)
        case 'min':
            # level = 0
            toggle_action(cords=MIN_VOLUME)
        case 'mute':
            # level = 0
            pyautogui.press("volumemute")
        case 'up':
            # level += 6
            for _ in range(3): pyautogui.press("volumeup")
        case 'down':
            # level -= 6
            for _ in range(3): pyautogui.press("volumedown")
        case int():
            x = 1460 + (level*3.5)
            cords = (x, 865)
            # print(cords)
            toggle_action(cords)
        case _:
            pyautogui.press("volumemute")
# volume()

# Brightness
def brightness(level=50):
    """ Toggle brightness to a specific level.
    Args:
    level (str or int): max, min, up, down or int value(0-100)
    """
    import screen_brightness_control as sbc
    match level:
        case 'max':
            change = 100
        case 'min':
            change = 0
        case 'up':
            change = sbc.get_brightness()[0] + 10
        case 'down':
            change = sbc.get_brightness()[0] - 10
        case int():
            change = level
            print('level:',change)
        case _:
            print('unknown')
            change = 100
    
    sbc.set_brightness(change)
# brightness()

# Date - time
# use datetime module