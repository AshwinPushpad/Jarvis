from tools.browser import open_on_web
from tools.app import open_app
from tools.music import play_music
from tools.video import play_video
from tools.file import find_file
TOOL_MAP = {
    "open_on_web": open_on_web,
    "open_app": open_app,
    "play_music": play_music,
    "play_video": play_video,
    "find_file": find_file
}
