import os
import sys
import time

KNOWN_POSITIVE_MESSAGES = [
    "gr",
    "gg",
    "ggs",
    "nt",
    "Good Round",
    "Good Game",
    "Nice Try"
]

def clean_exit(exit_reason):
    if os.path.exists(f"{os.environ.get('TEMP')}\\temp.png"):
        os.remove(f"{os.environ.get('TEMP')}\\temp.png")
    os.system("cls")
    input(f"{exit_reason}\n\nPress Enter to Exit...")
    os.system("cls")
    sys.exit()

def get_file_path(relative_path):
    if getattr(sys, 'frozen', False):
        file_path = f"{sys._MEIPASS}/{relative_path}"
    else:
        file_path = os.path.abspath(relative_path)
    return file_path

def start_siege(active, mnk):
    os.system(f'start /MAX "" "{__CONFIG.get_config()["Advanced"]["siege_path"]}"')
    start_time = time.time()
    while True:
        if time.time() >= (start_time + 1800): # After 30 minutes have passed, then exit, this is to ensure the AFK Bot from breaking.
            clean_exit("[ERROR] R6 AFK Bot failed to restart siege, manual intervention needed.")
        current_state = detect_state(active, mnk)
        current_state = [current_state["in_lobby"], current_state["reconnect"], current_state["popup"][0]]
        if True in current_state:
            # Maximize the game, then return
            for title in SIEGE_WINDOW_NAMES:
                user32 = ctypes.WinDLL('user32')
                hwnd = user32.FindWindowW(None, window_title)
                if hwnd:
                    user32.ShowWindow(hwnd, 3)
                    user32.SetForegroundWindow(hwnd)
            break
