import os
import sys
import time
import ctypes

def change_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

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

def get_input(prompt, allowed_answers=None):
    while True:
        os.system("cls")
        answer = input(f"{prompt}\n\n> ").strip()
        if answer in ["", " "]:
            continue
        elif allowed_answers != None and answer not in allowed_answers: # Lets you to restrict the answers allowed
            print("Answer not allowed, allowed answers are:\n" + "\n".join(f"- {answer}" for answer in allowed_answers))
            time.sleep(5)
            continue
        return answer
