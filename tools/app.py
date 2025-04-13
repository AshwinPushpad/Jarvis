import os

def open_app(app_name="notepad.exe"):
    print(f"Launching {app_name}...")
    os.system(app_name)
