import os
import time
import ctypes
import psutil
import random
import keyboard
import threading
from src.active import ActiveManager
from src.mnk import MouseAndKeyboard
from src.utils import Start_Siege, __CONFIG
from src.__init__ import change_title, clean_exit, get_file_path
from src.screen import SCREEN_WIDTH, SCREEN_HEIGHT, detect_state
from src.randomness import get_actions, get_coord, get_direction, get_messages, get_random_time

VERSION = 3.0

USER32 = ctypes.windll.user32
USER32.SetProcessDPIAware()

__MNK = MouseAndKeyboard()
__ACTIVE = ActiveManager()

last_message = None
last_level_check = None
last_crash_detection = None

CRASH_DETECTED = True

def AFK_Bot():
    """Run the inputs."""
    global last_message
    global CRASH_DETECTED
    global last_level_check
    global last_crash_detection
    
    while True:
        active = __ACTIVE
        state = detect_state(active, __MNK)

        # CRASH PREVENTION FEATURE
        if time.time() > (last_crash_detection + 60): # Every minute check to see if the game has crashed
            for proc in psutil.process_iter(['pid', 'name']):
                for name in ["RainbowSix.exe"]:
                    if proc.info['name'].lower() == name.lower():
                        CRASH_DETECTED = False
                        break
            Start_Siege(active, __MNK) if CRASH_DETECTED else "" # Start the game if a Crash is detected
            CRASH_DETECTED = True
        
        if state["banned"]:
            __THREADS.stop()
            clean_exit("Ban Detected.\nR6 AFK Bot Deactivated.")
        
        elif state["sanctioned"]:
            __THREADS.stop()
            clean_exit("Sanction Detected.\nR6 AFK Bot Deactivated.")

        elif state["popup"][0]:
            # Accept the popup depending on the type
            if state["popup"][1] == "normal":
                __MNK.select_button(active, x_coord=744, y_coord=946)
            elif state["popup"][1] in ["badge", "reputation"]: # Badge or Reputation Drop popups
                __MNK.select_button(active, x_coord=769, y_coord=987)
            else: # For the special popup type
                for _ in range(7):
                    __MNK.select_button(active, x_coord=1612, y_coord=863) # Click the button 7 times to ensure that it removed the popup (there's mutliple clicks needed)
                continue # Continue, and scan the screen again
        
        elif state["reconnect"]:
            # reconnect to the game then sleep until in the game
            __MNK.select_button(active, x_coord=482, y_coord=215, sleep_range=(15, 16))
        
        elif state["in_lobby"]:
            # move mouse to the main menu
            __MNK.select_button(active, x_coord=132, y_coord=71, sleep_range=(4, 4.5))
            # press play again
            __MNK.select_button(active, x_coord=440, y_coord=213, sleep_range=(7.5, 7.6))

        elif state["queueing"]:
            # move mouse randomly until in a game
            for x in range(random.randint(2, 5)):
                __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
            
        elif state["in_game"]:
            action_list = get_actions(num_of_actions=random.randint(3, 5) if random.choice([1, 1, 1, 2]) == 1 else None)

            for action in action_list: 
                match action:
                    case "dk": # directional key
                        __MNK.keypress(active, key=get_direction(), duration=0)
                    case "dk_shift": # directional key + shift
                        __MNK.keypress(active, key=get_direction(), duration=0, hold_shift=True)
                    case "mm": # mouse movement
                        __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
                    case "mm_dk": # mouse movement + directional key
                        match random.randint(1, 2):
                            case 1:
                                __MNK.keypress(active, key=get_direction(), duration=0)
                                __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
                            case 2:
                                __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
                                __MNK.keypress(active, key=get_direction(), duration=0)

                time.sleep(get_random_time(0.8, 1.2))

            if __CONFIG.get_config()["Text_Chat_Messages"]["enabled"]: # TEXT CHAT MESSAGING FEATURE
                if time.time() > (last_message + random.randint(300, 420)): # every <= 5-7 minutes (DEFAULT VALUE) the bot has a chance to send a message
                    num = __CONFIG.get_config()["Text_Chat_Messages"]["num_of_messages"]
                    messages = get_messages(num=num)
                    for message in messages:
                        __MNK.send_text(active, text=message, all_chat_key=__CONFIG.get_config()["Text_Chat_Messages"]["all_chat_key"])
                        time.sleep(get_random_time(1.5, 2.5))
                    last_message = time.time()

        elif state["end_of_game"]: # SQUAD SUPPORT FEATURE
            if state["squad_leader"]:
                # press new match with squad if found to be in a squad as the squad leader
                __MNK.select_button(active, x_coord=1652, y_coord=1023, sleep_range=(3.5, 4.5))
                __MNK.select_button(active, x_coord=736, y_coord=985)
            elif state["ready_up"]:
                # press ready up if found to be in a squad, but not the squad leader
                __MNK.select_button(active, x_coord=1677, y_coord=1027)
                # move mouse randomly until in a game
                for x in range(random.randint(5, 10)):
                    __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
            else:
                # press find another match if found to not be in a squad
                __MNK.select_button(active, x_coord=1370, y_coord=1026)

        if __ACTIVE.user_active():
            time.sleep(get_random_time(2.5, 3.5)) # this sleep timer is mainly for older computers with worse graphics, but it's also useful for the state detection
            CRASH_DETECTED = True # Reset the variable to make the Crash Prevention work.
            continue
        break

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
        change_title("R6 AFK Bot | ACTIVATED")
        print("Activated.")
    else:
        __THREADS.stop()
        if os.path.exists(f"{os.environ.get('TEMP')}\\temp.png"):
            os.remove(f"{os.environ.get('TEMP')}\\temp.png")
        last_message = None
        last_level_check = None
        last_crash_detection = None
        change_title("R6 AFK Bot | DEACTIVATED")
        print("Deactivated.")

if __name__ == "__main__":
    os.system("cls")
    change_title(f"R6 AFK Bot v{VERSION}")

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
        except:
            clean_exit("[ERROR] Failed to install Tesseract OCR... Run the R6 AFK Bot to attempt the install again. If it still fails, manually download the installer from https://github.com/UB-Mannheim/tesseract/wiki, while leaving everything as default.")

    print(f'v{VERSION}') # App version goes here, add later
    print(f'Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}')

    keyboard.add_hotkey(hotkey='f2', callback=__on_press, suppress=True)
    print("Ready.")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            clean_exit("Thanks for using the R6 AFK Bot.")

