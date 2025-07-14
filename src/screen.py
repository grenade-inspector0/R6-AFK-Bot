import os
import time
import ctypes
import pytesseract
from PIL import Image, ImageGrab

# default path - C:/Program Files/Tesseract-OCR/tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# UPDATE LOBBY COORDS
coords = {
    "lobby": [(85, 231, 836, 925), (208, 318, 52, 90), (374, 450, 52, 90)],
    "queueing": [(808, 1026, 38, 68), (862, 987, 36, 64), (87, 188, 850, 915)],
    "end_of_game": (1206, 1435, 982, 997),
    "popups": [(692, 727, 920, 950), (664, 732, 963, 996), (679, 1197, 173, 260), (685, 943, 909, 1008), (622, 773, 938, 1000), (689, 963, 176, 245)],
    "reconnect": (875, 1070, 40, 70),
    "ban_check": (655, 1045, 38, 68)
}

button_coords = {
    "lobby": [(132, 71), (130, 876), (122, 986), (1100, 531), (740, 531), (407, 531)],
    "end_of_game": (1316, 1022),
    "popups": [(744, 946), (769, 987)]
}

keywords = {
    "lobby": ["play again", "operators", "locker"],
    "queueing": ["crossplay", "match found"],
    "end_of_game": "find another",
    "popups": ["ok", "cancel", "close", "next", "reconnect", "menu", "get your", "reputation"],
    "reconnect": "reconnect",
    "ban_check": ["suspended", "banned", "sanction"]
}

"""
(Explainations for each index)

## Coords layout 
# lobby :
0 - play_again
    - Coords to check for the phrase "play again" in the bottom left when in lobby
1 - operators
    - Coords to check for the word "operator" in the top left when in lobby
2 - locker
    - Coords to check for the word "locker" in the top left when in lobby


# queueing :
0 - queueing_for_game
    - Coords to check for the word "queueing" at the top center of the screen while looking for a game
1 - match_found
    - Coords to check for the phrase "match found" at the top center of the screen while loading into a game
2 - queueing_reconnect
    - Coords for secondary verification of the R6 AFK Bot needing to reconnect to the game


# end_of_game : 
- find_new_match
    - Coords to check for the phrase "find another" in the bottom right at the end of a match


# popups :
0 - normal_popup : Popups that appear often; "Failed to connect to server", "Reconnect", etc.
1 - badge_popup : Popup that appears when you get a badge 
2 - reputation_popup : Popup that appears when you get a reputation drop
3 - advertising_popups : Popup(s) that appear when the game wants to you to buy an item from the shop
4 - misc_popup : Popup that appears when you level up and other times
5 - other_popups : Popups that weren't caught on the first check

## Button Coords layout (Explainations for each index)
# lobby :
0 - Return to main menu button ("Play" button in the top left corner of the lobby)
1 - "Play Again" button
2 - "Playlist" button
3 - Ranked button in the "Playlist" submenu
4 - Unranked button in the "Playlist" submenu
5 - Casual button in the "Playlist" submenu


# end_of_game
0 - "Find New Match" button at the end screen of a match
1 - "New Match With Squad" button at the end screen of a match
2 - "Ready up" button at the end screen of a match


# popups :
0 - normal_popup
1 - other_popups
"""


win32 = ctypes.windll.user32
win32.SetProcessDPIAware()

SCREEN_WIDTH = win32.GetSystemMetrics(0)
SCREEN_HEIGHT = win32.GetSystemMetrics(1)

def get_res_scale_x(x):
    return int(SCREEN_WIDTH/1920 * x)

def get_res_scale_y(y):
    return int(SCREEN_HEIGHT/1080 * y)

def take_screenshot(coords=None):
    im = ImageGrab.grab(bbox=coords) # lowest x, lowest y, highest x, highest y
    im.save(f'{os.environ.get('TEMP')}\\temp.png')

def read_screenshot(screen_coords=None, keyword=None):
    if screen_coords != None and keyword != None:
        take_screenshot((get_res_scale_x(screen_coords[0]), get_res_scale_y(screen_coords[2]), get_res_scale_x(screen_coords[1]), get_res_scale_y(screen_coords[3])))
        result = pytesseract.image_to_string(Image.open(f'{os.environ.get('TEMP')}\\temp.png'))
        if keyword in result.lower():
            return True
        else:
            return False

def detect_state():
    state = {
        "in_lobby": False, "queueing": False, "in_game": True, "reconnect": False, "popup": (False, None),
        "end_of_game": False, "banned": False, "sanctioned": False
    }
    
    # In Lobby
    state["in_lobby"] = True if read_screenshot(coords["lobby"][0], keywords["lobby"][0]) else False 

    if not state["in_lobby"]:
        # Banned check
        if read_screenshot(coords["ban_check"], keywords["ban_check"][0]) or read_screenshot(coords["ban_check"], keywords["ban_check"][1]):
            state["banned"] = True
            return state
        # Sanctioned Check
        elif read_screenshot(coords["ban_check"], keywords["ban_check"][2]):
            state["sanctioned"] = True
            return state
        # 2nd In Lobby Check
        elif read_screenshot(coords["lobby"][1], keywords["lobby"][1]) or read_screenshot(coords["lobby"][2], keywords["lobby"][2]):
            state["in_lobby"] = True

    # Queueing 
    state["queueing"] = read_screenshot(coords["queueing"][0], keywords["queueing"][0])
    if not state["queueing"]:
        state["queueing"] = read_screenshot(coords["queueing"][1], keywords["queueing"][1])

    # End of game
    state["end_of_game"] = read_screenshot(coords["end_of_game"], keywords["end_of_game"])

    # Normal Popup
    state["popup"] = (True, "normal") if read_screenshot(coords["popups"][0], keywords["popups"][0]) else (False, None)
    
    # 2nd Popup Check (For ones that weren't caught)
    if not state["popup"][0]:
        for x in range(1, len(keywords["popups"])):
            if not state["popup"][0]:
                state["popup"] = (True, "normal") if read_screenshot(coords["popups"][5], keywords["popups"][x]) else (False, None)
            if state["popup"][0]:
                break

    # Other Popups (Badge Popups, Reputation Popups, Advertising Popups, etc.)
    if not state["popup"][0]:
        popups = [
            read_screenshot(coords["popups"][1], keywords["popups"][2]), # Badge Popup
            read_screenshot(coords["popups"][2], keywords["popups"][7]), # Reputation Popup
            read_screenshot(coords["popups"][3], keywords["popups"][2]), # Advertising Popup
            read_screenshot(coords["popups"][4], keywords["popups"][2]) # Misc. Popup
        ]

        state["popup"] = (True, "other") if True in popups else (False, None)

    
    
    # If there's a popup, then set all other states to False, and return
    if state["popup"][0]:
        state["in_lobby"] = False
        state["queueing"] = False
        state["in_game"] = False
        state["reconnect"] = False
        state["end_of_game"] = False
        return state
    
    # Reconnect Detection
    state["reconnect"] = read_screenshot(coords["reconnect"], keywords["reconnect"])
    if state["reconnect"]:
        if not read_screenshot(coords["queueing"][2], keywords["reconnect"]):
            state["reconnect"] = False
    
    # Defaults to the "in_game" state if no other states are found to be True
    for key, value in state.items():
        if value == True:
            if key != "in_game":
                state["in_game"] = False
                break
    return state

