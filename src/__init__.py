import os
import sys
import time

POSITIVE_MESSAGES = [
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
