import os
import json
import time
import ctypes
import tkinter as tk
from tkinter import filedialog
from src.screen import detect_state
from src.__init__ import clean_exit, get_file_path

# Default Siege .exe Path - "C:\Program Files (x86)\Ubisoft\Ubisoft Game launcher\games\Tom Clancy's Rainbow Six Siege\RainbowSix.exe"

class Config:
    def __init__(self):
        self.default_config = json.load(open(get_file_path("assets/default_config.json"), "r"))
        self.default_siege_path = f"{os.getenv('ProgramFiles(x86)')}\\Ubisoft\\Ubisoft Game launcher\\games\\Tom Clancy's Rainbow Six Siege\\RainbowSix.exe"
    
    def get_siege_path(self):
        root = tk.Tk()
        root.withdraw()
        siege_path = filedialog.askopenfilename(
            title="Select RainbowSix.exe",
            initialdir="C:/Program Files (x86)/Ubisoft/Ubisoft Game launcher/games/Tom Clancy's Rainbow Six Siege",
            filetypes=[("Executable files", "*.exe")]
        )

        if siege_path:
            root.destroy()
            return siege_path
        else:
            clean_exit("[ERROR] Failed to generate new config file.\nExiting...")
            

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

        # Prevents issues from older versions
        if config["Advanced"]["siege_path"].lower() == "default":
            os.system("cls")
            print("Older version detected, regenerating config.json...")
            time.sleep(1.5)
            self.create_config()
            clean_exit("[DONE] Successfully regenerated config.json! Start the .exe again, and it should work! If this error persists, contact Support.")

        # Verify the siege_path variable actually exists and ends with .exe
        if not os.path.exists(config["Advanced"]["siege_path"]) or not config["Advanced"]["siege_path"].endswith(".exe"):
            errors.append("Invalid Siege Path.")

        # Verify the message interval
        if len(config["Advanced"]["message_interval"]) > 2 or not all(isinstance(item, (int)) for item in config["Advanced"]["message_interval"]):
            errors.append("Invalid Message Interval length")

        if errors:
            # Check if the error is only an invalid siege path, if so, exit, while telling the user that the path is wrong, otherwise delete the old config
            if len(errors) == 1 and errors[0] == "Invalid Siege Path.":
                clean_exit("[ERROR] Config Check Failed.\nInvalid Siege Path, please input a valid path, then run the R6 AFK Bot again.")
            else:
                self.create_config()
                clean_exit("[ERROR] Config Check Failed.\nDeleting Old Config File...\nCreating new Config File...\n\nSuccessfully created new Config File!")
        return
        
    def create_config(self):
        config = self.default_config
        config["Advanced"]["siege_path"] = self.default_siege_path if os.path.exists(self.default_siege_path) else self.get_siege_path()

        with open("./config.json", "w") as f:
            json.dump(config, f, indent=5)

__CONFIG = Config()