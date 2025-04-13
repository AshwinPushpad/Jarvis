import subprocess
import webbrowser
import os
import pygame
def open_app(command):
    try:
        subprocess.Popen([f"{command}.exe"], shell=True)
    except Exception as e:
        pass

# Dictionary to map site names to URLs
website_dict = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "reddit": "https://www.reddit.com"
}

def open_website(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        pass
# Set the path to your music folder
MUSIC_FOLDER = r"C:\Users\YourName\Music"  # <-- Change this to your actual music folder

def find_song(song_name):
    for root, dirs, files in os.walk(MUSIC_FOLDER):
        for file in files:
            if song_name.lower() in file.lower() and file.endswith(('.mp3', '.wav', '.ogg')):
                return os.path.join(root, file)
    return None

def play_video(video):
    try:
        webbrowser.open(f"https://www.youtube.com/results?search_query={video}")
    except Exception as e:
        pass

def main():
    song_name = input("Enter the song name to play: ")
    song_path = find_song(song_name)
    
    if song_path:
        play_music(song_path)
    else:
        print("Sorry, the song was not found.")

FOLDER_PATH = r"C:\Users\arpan\Desktop"  # Change this to your desired folder

def open_file_by_name(file_name):
    for root, dirs, files in os.walk(FOLDER_PATH):
        for file in files:
            if file_name.lower() in file.lower():
                file_path = os.path.join(root, file)
                print(f"Opening: {file_path}")
                os.startfile(file_path)  # Windows only
                return
    print("File not found.")


if __name__ == "__main__":
    command ="notepad"
    open_app(command)
    open_website()
    main()
    name = input("Enter the file name (without extension is okay): ")
    open_file_by_name(name)

