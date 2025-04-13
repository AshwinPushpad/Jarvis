import speech_recognition as sr

def main():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.dynamic_energy_adjustment_damping = 0.3
    r.dynamic_energy_ratio = 0.9
    r.pause_threshold = 0.5
    r.operation_timeout = None
    r.non_speaking_duration = 0.5

    with sr.Microphone() as source:
        print("Calibrating for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)

        print("Ready! Press [Enter] to speak. Ctrl+C to exit.")

        try:
            while True:
                input("▶ Press [Enter] to listen: ")
                print("🎙 Listening...")
                audio = r.listen(source, phrase_time_limit=5)
                try:
                    text = r.recognize_google(audio)
                    print(f"🗣 You said: {text}")
                except sr.UnknownValueError:
                    print("🤷 Couldn't understand audio.")
                except sr.RequestError as e:
                    print(f"❌ Request failed: {e}")
        except KeyboardInterrupt:
            print("\n🔚 Stopped by user.")

main()
