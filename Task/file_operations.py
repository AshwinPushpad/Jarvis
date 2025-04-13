
import os

def find_file(filename, search_path="C:\\"):  # Change search_path if needed
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

file_name = "example.txt"  # Change to the file you want to search
file_path = find_file(file_name)

if file_path:
    print(f"File found: {file_path}")
else:
    print("File not found.")




# Read Screen
import pyautogui
import pytesseract
from PIL import Image
import pyttsx3

# Set Tesseract-OCR path (change this if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speed if needed

def read_screen():
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save("screen.png")

    # Extract text from the image
    text = pytesseract.image_to_string(Image.open("screen.png"))
    
    if text.strip():
        print("Extracted Text:\n", text)
        engine.say(text)
        engine.runAndWait()
    else:
        print("No text detected on screen.")

# Call the function
read_screen()


## 📸 3. Screenshots and Image Recognition
# ✅ 3.1 Take a Screenshot
screenshot = pyautogui.screenshot()
screenshot.save("screenshot.png")  # Saves it as a file
# ✅ 3.2 Locate an Image on Screen
position = pyautogui.locateOnScreen("button.png")  # Finds image coordinates
print(position)  # Returns (x, y, width, height)
# ✅ 3.3 Click on an Image
button = pyautogui.locateCenterOnScreen("button.png")
pyautogui.click(button)  # Clicks the center of the button
