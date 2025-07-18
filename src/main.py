import os
import time
import ctypes
import psutil
import random
import keyboard
import threading
from src.config import __CONFIG
from src.mnk import MouseAndKeyboard
from src.active import SIEGE_WINDOW_NAMES, ActiveManager
from src.__init__ import GAMEMODE_INDEXS, clean_exit, get_file_path
from src.randomness import get_actions, get_coord, get_direction, get_messages
from src.screen import SCREEN_WIDTH, SCREEN_HEIGHT, button_coords, detect_state



VERSION = 3.32

USER32 = ctypes.windll.user32
USER32.SetProcessDPIAware()

__MNK = MouseAndKeyboard()
__ACTIVE = ActiveManager()

last_message = None
last_level_check = None
last_crash_detection = None

CRASH_DETECTED = True

def start_siege():
    # Move the CMD Prompt window running the .exe / .py file to a specfic location; this prevents the R6 AFK Bot from not being able to detect that the game's reloaded
    current_window = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.MoveWindow(current_window, SCREEN_WIDTH-800, 0, 800, 600, True)

    os.system(f'start /MAX "" "{__CONFIG.get_config()["Advanced"]["siege_path"]}"')
    start_time = time.time()
    while True:
        if time.time() >= (start_time + 1800): # After 30 minutes have passed, then exit, this is to keep the AFK Bot from breaking.
            __ACTIVE.switch_active()
            __THREADS.stop()
            clean_exit("[ERROR] R6 AFK Bot failed to restart siege, manual intervention needed.")
        current_state = detect_state()
        current_state = [current_state["in_lobby"], current_state["reconnect"], current_state["popup"][0]]
        if True in current_state:
            # Maximize the game, then return
            for title in SIEGE_WINDOW_NAMES:
                user32 = ctypes.WinDLL('user32')
                hwnd = user32.FindWindowW(None, title)
                if hwnd:
                    user32.ShowWindow(hwnd, 3)
                    user32.SetForegroundWindow(hwnd)
            break

def AFK_Bot():
    """Run the inputs."""
    global last_message
    global CRASH_DETECTED
    global last_level_check
    global last_crash_detection
    
    while __ACTIVE.user_active():
        active = __ACTIVE
        state = detect_state()

        # CRASH DETECTION
        if time.time() > (last_crash_detection + 60): # Every minute check to see if the game has crashed
            for proc in psutil.process_iter(['pid', 'name']):
                for name in SIEGE_WINDOW_NAMES:
                    if proc.info['name'].lower() == "RainbowSix.exe".lower():
                        CRASH_DETECTED = False
                        break
            start_siege() if CRASH_DETECTED else "" # Start the game if a Crash is detected
            CRASH_DETECTED = True # Reset the variable to make the Crash Detection work.
        
        if state["banned"]:
            # If the account is banned, then exit
            clean_exit(f"Ban Detected.\nR6 AFK Bot Deactivated.")

        elif state["sanctioned"]:
            # If the account isn't banned, only sanctioned, then idle until the sanction is no longer detected
            continue

        elif state["popup"][0]:
            # Accept the popup depending on the type
            if state["popup"][1] == "normal":
                __MNK.select_button(active, x_coord=button_coords["popups"][0][0], y_coord=button_coords["popups"][0][1])
            else:
                __MNK.select_button(active, x_coord=button_coords["popups"][1][0], y_coord=button_coords["popups"][1][1])
        
        elif state["reconnect"]:
            # reconnect to the game then sleep until in the game
            __MNK.select_button(active, x_coord=button_coords["lobby"][1][0], y_coord=button_coords["lobby"][1][1], sleep_range=(15, 16))
        
        elif state["in_lobby"]:
            # move mouse to the main menu
            __MNK.select_button(active, x_coord=button_coords["lobby"][0][0], y_coord=button_coords["lobby"][0][1], sleep_range=(4, 4.5))

            if not __CONFIG.get_config()["Mode_Selection"]["enabled"]:
                # press play again
                __MNK.select_button(active, x_coord=button_coords["lobby"][1][0], y_coord=button_coords["lobby"][1][1], sleep_range=(7.5, 7.6))
                continue
            
            # open the menu to select a gamemode
            __MNK.select_button(active, x_coord=button_coords["lobby"][2][0], y_coord=button_coords["lobby"][2][1], sleep_range=(7.5, 7.6))

            try:
                index = GAMEMODE_INDEXS[__CONFIG.get_config()["Mode_Selection"]["gamemode"].lower().strip()]
            except KeyError:
                index = random.choice([i for n, i in GAMEMODE_INDEXS.items()])

            # select the user's gamemode
            __MNK.select_button(active, x_coord=button_coords["lobby"][index][0], y_coord=button_coords["lobby"][index][1], sleep_range=(7.5, 7.6))

        elif state["queueing"]:
            # move mouse randomly until in a game
            for x in range(random.randint(2, 5)):
                __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
            
        elif state["in_game"]:
            action_list = get_actions()

            for action in action_list: 
                match action:
                    case "dk": # directional key
                        __MNK.keypress(active, key=get_direction(), duration=0)
                    case "dk_shift": # directional key + shift
                        __MNK.keypress(active, key=get_direction(), duration=0, hold_shift=True)
                    case "mm": # mouse movement
                        __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
                    case "mm_dk": # mouse movement + directional key
                        if random.randint(1, 2) == 1:
                            __MNK.keypress(active, key=get_direction(), duration=0)
                            __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
                        else:
                            __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
                            __MNK.keypress(active, key=get_direction(), duration=0)

                time.sleep(random.uniform(0.8, 1.2))

            if __CONFIG.get_config()["Text_Chat_Messages"]["enabled"]:
                message_interval = __CONFIG.get_config()["Advanced"]["message_interval"]
                if time.time() > (last_message + random.randint((message_interval[0]*60), (message_interval[1]*60))): # every <= 5-7 minutes (DEFAULT VALUE) the bot has a chance to send 1+ message(s)
                    num = __CONFIG.get_config()["Text_Chat_Messages"]["num_of_messages"]
                    messages = get_messages(num=num, limit_messages=__CONFIG.get_config()["Advanced"]["limit_messages"])
                    for message in messages:
                        __MNK.send_text(active, text=message, all_chat_key=__CONFIG.get_config()["Text_Chat_Messages"]["all_chat_key"])
                        time.sleep(random.uniform(1.5, 2.5))
                    last_message = time.time()

        elif state["end_of_game"]:
            # Press find another match
            __MNK.select_button(active, x_coord=button_coords["end_of_game"][0][0], y_coord=button_coords["end_of_game"][0][1])

        time.sleep(random.uniform(2.5, 3.5)) # this sleep timer is mainly for older computers with worse graphics, but it's also useful for the state detection

class Threads:
    def __init__(self) -> None:
        self.runner_thread = threading.Thread(target=AFK_Bot)

    def start(self):
        # Start R6 AFK Bot
        self.runner_thread.start()

    def stop(self):
        # Stop R6 AFK Bot
        self.runner_thread.join()
        if not self.runner_thread.is_alive():
            self.runner_thread = threading.Thread(target=AFK_Bot)

__THREADS = Threads()

def __on_press():
    # Activate/deactivate the bot when the hot key is pressed.
    global last_message
    global last_level_check
    global last_crash_detection
    __ACTIVE.switch_active()

    if __ACTIVE.user_active():
        __THREADS.start()
        if last_message == None:
            last_message = time.time()
        if last_level_check == None:
            last_level_check = time.time()
        if last_crash_detection == None:
            last_crash_detection = time.time()
        print("Activated.")
    else:
        __THREADS.stop()
        if os.path.exists(f"{os.environ.get('TEMP')}\\temp.png"):
            os.remove(f"{os.environ.get('TEMP')}\\temp.png")
        last_message = None
        last_level_check = None
        last_crash_detection = None
        print("Deactivated.")

if __name__ == "__main__":
    os.system("cls")
    ctypes.windll.kernel32.SetConsoleTitleW(f"R6 AFK Bot v{VERSION}")

    # Create the config file if it doesn't exist
    if not os.path.exists("./config.json"):
        __CONFIG.create_config()
        clean_exit("[ERROR] Config file not found...\nCreating new Config File...\n\nSuccessfully created new Config File!")
    
    # Check for Tesseract (https://github.com/UB-Mannheim/tesseract/wiki)
    if not os.path.exists(f"C:/Program Files/Tesseract-OCR/tesseract.exe"):
        try: # Try to install Tesseract OCR, if the install fails, then exit.
            os.system("cls")
            print("[ERROR] Tesseract.exe not found...")
            print("Attempting to install Tesseract OCR automatically...")
            # Install here, while also adding Tesseract OCR to path
            os.system(f"{get_file_path("assets/tesseract-installer.exe")} /S")
            os.environ["PATH"] += os.pathsep + "C:/Program Files/Tesseract-OCR"
            input("[SUCCESS] Successfully installed Tesseract OCR!\n\nPress Enter to continue...") 
            os.system("cls")
        except:
            clean_exit("[ERROR] Failed to install Tesseract OCR... Run the R6 AFK Bot to attempt the install again. If it still fails, manually download the installer from https://github.com/UB-Mannheim/tesseract/wiki, while leaving everything as default.")

    # Create the READ_IMPORTANT file if it doesn't exist
    if not os.path.exists("./READ_IMPORTANT.txt"):
        with open("./READ_IMPORTANT.txt", "w") as f:
            data = open(get_file_path("assets/READ_IMPORTANT.txt")).read()
            f.write(data)
        os.system("notepad.exe ./READ_IMPORTANT.txt")

    print(f'v{VERSION}')
    print(f'Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}')

    keyboard.add_hotkey(hotkey='f2', callback=__on_press, suppress=True)
    print("Ready.")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            clean_exit("Thanks for using the R6 AFK Bot.")
