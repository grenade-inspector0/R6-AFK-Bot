import os
import json
import time
import ctypes
from screen import detect_state
from active import SIEGE_WINDOW_NAMES
from __init__ import clean_exit, get_file_path

class Config:
    def __init__(self):
        self.default_config = json.load(open(get_file_path("assets/config.json"), "r"))
    
    def get_config(self):
        if not os.path.exists("./config.json"):
            self.create_config()
        with open("./config.json", "r") as f:
            config = json.load(f)
        self.check_config(config, self.default_config)
        return config

    def check_config(config, default, path="root"):
        errors = []
        if not isinstance(config, dict) or not isinstance(default, dict):
            return [f"Type mismatch at {path}: expected {type(default).__name__}, got {type(config).__name__}"]
        
        for key, default_value in default.items():
            if key not in config:
                errors.append(f"Missing key at {path}.{key}")
                continue
            
            config_value = config[key]
            if isinstance(default_value, dict):
                errors.extend(check_config(config_value, default_value, f"{path}.{key}"))
            elif isinstance(default_value, list):
                if not isinstance(config_value, list):
                    errors.append(f"Type mismatch at {path}.{key}: expected list, got {type(config_value).__name__}")
                elif config_value and not all(isinstance(i, type(default_value[0])) for i in config_value):
                    errors.append(f"List element type mismatch at {path}.{key}")
            elif not isinstance(config_value, type(default_value)):
                errors.append(f"Type mismatch at {path}.{key}: expected {type(default_value).__name__}, got {type(config_value).__name__}")
        
        # Verify the siege_path variable actually exists and isn't the word: "default"
        if config["Advanced"]["siege_path"] != "default" and not os.path.exists(config["Advanced"]["siege_path"]):
            errors.append("Invalid Siege Path.")
        elif not config["Advanced"]["siege_path"].endswith(".exe"):
            errors.append("Invalid Siege Path.")

        if errors:
            # Check if the error is only an invalid siege path, if so, exit, while telling the user that the path is wrong, otherwise delete the old config
            if len(errors) == 1 and errors[0] == "Invalid Siege Path.":
                clean_exit("[ERROR] Config Check Failed.\nInvalid Siege Path, please input a valid path, then run the R6 AFK Bot again.")
            else:
                self.create_config()
                clean_exit("[ERROR] Config Check Failed.\nDeleting Old Config File...\nCreating new Config File...\n\nSuccessfully created new Config File!")
        
        return
        
    def create_config(self):
        with open("./config.json", "w") as f:
            json.dump(self.default_config, f, indent=5)
    
def Start_Siege(active, mnk):
    # Find the user's siege path
    if __CONFIG.get_config()["Advanced"]["siege_path"] == "default":
        SIEGE_PATH = f"{os.getenv('ProgramFiles(x86)')}\\Ubisoft\\Ubisoft Game launcher\\games\\Tom Clancy's Rainbow Six Siege\\RainbowSix.exe"
    else:
        SIEGE_PATH = __CONFIG.get_config()["Advanced"]["siege_path"]
    os.system(f'start /MAX "" "{SIEGE_PATH}"')
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

__CONFIG = Config()