import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import speech_recognition as sr
from tts import speak
from mrk2 import handle_command
import os
from time import sleep
# ======================
# Tray Icon + Menu Setup
# ======================

def create_icon_image():
    # Create a simple blue circle icon
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill="blue")
    return image

def start_listening():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.dynamic_energy_adjustment_damping = 0.3
    r.dynamic_energy_ratio = 0.9
    r.pause_threshold = 0.5
    r.operation_timeout = None
    r.non_speaking_duration = 0.5

    with sr.Microphone() as source:
        print("🎙️ Calibrating...")
        r.adjust_for_ambient_noise(source, duration=1)
        speak("Hi sir, what can I help you with?")
        print("🔊 Listening...")

        try:
            audio = r.listen(source, phrase_time_limit=5)
            print("✅ Processing...")
            text = r.recognize_google(audio)
            print(f"🗣️ You said: {text}")

            ai_response = handle_command(text)
            if ai_response == "Goodbye!":
                speak("Then I'be taking my leave sir.")
                return
            else:
                speak(ai_response)
                sleep(0.5)
            speak("Then I'be taking my leave sir.")
            # print(ai_response)


        except sr.UnknownValueError:
            print("🤷 Couldn't understand.")
            speak("Pardon me sir, Can you repeat.")
        except sr.RequestError as e:
            print(f"❌ Error from Google: {e}")

def on_start_listening(icon, item):
    # Run listening in a separate thread so the tray doesn't freeze
    threading.Thread(target=start_listening).start()

def on_quit(icon, item):
    speak("Then I'be taking my leave sir.")
    icon.stop()

# ==================
# Run the Tray Icon
# ==================

def setup_tray():
    icon = Icon(
        "JarvisTray",
        create_icon_image(),
        "Jarvis Assistant",
        menu=Menu(
            MenuItem("🎤 Start Listening", on_start_listening),
            MenuItem("❌ Quit", on_quit),
        ),
    )
    icon.run()

# Start tray in background
threading.Thread(target=setup_tray).start()
