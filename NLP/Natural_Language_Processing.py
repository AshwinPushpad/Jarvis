import asyncio
import edge_tts
import time

async def test_edge_tts(text):
    start = time.time()
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    communicate.stream()
    await communicate.save(r"saves\test.mp3")
    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")

asyncio.run(test_edge_tts("Hello Ashwin, I am Jarvis!"))


import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
# Choose a better voice (Change index based on your system)
    engine.setProperty('voice', voices[1].id)  
# Slow down speech rate
    engine.setProperty('rate', 180)
# Set max volume
    engine.setProperty('volume', 1.0)
# Speak
    engine.say(text)
    engine.runAndWait()

# speak(text="Hello Ashwin, I am Jarvis!")

