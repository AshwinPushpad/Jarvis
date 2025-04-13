
import asyncio
import edge_tts  # optional for voice response
import tempfile
import os
# For speech
import pygame
import asyncio

async def speak(text):
    communicate = edge_tts.Communicate(text, voice="en-IN-NeerjaNeural")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        file_path = tmp.name
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                tmp.write(chunk["data"])

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait until finished
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(2)
    pygame.mixer.quit()

    os.remove(file_path)
asyncio.run(speak(text="Yes?"))

