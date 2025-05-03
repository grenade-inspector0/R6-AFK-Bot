import os
import time
import ctypes
import pytesseract
from PIL import Image, ImageGrab

# default path - C:/Program Files/Tesseract-OCR/tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

coords = {
    "lobby": [(375, 505, 174, 250), (208, 318, 52, 90), (374, 450, 52, 90), (84, 441, 100, 257), (309, 440, 760, 815)],
    "queueing": [(808, 1026, 38, 68), (862, 987, 36, 64), (385, 530, 185, 251)],
    "end_of_game": [(1261, 1465, 1002, 1033), (1541, 1755, 980, 1030), (1587, 1784, 996, 1044)],
    "popups": [(692, 727, 920, 950), (664, 732, 963, 996), (679, 1197, 173, 260), (1562, 1648, 843, 876), (689, 963, 176, 245), (689, 963, 176, 245)],
    "reconnect": (837, 1080, 38, 68),
    "account_actions": (655, 1045, 38, 68)
}

button_coords = {
    "lobby": [(132, 71), (110, 220), (343, 780), (1030, 791), (836, 783)]
}

keywords = {
    "in_lobby": ["play again", "operators", "locker", "new playlist", "new event", "tactical"],
    "queueing": ["crossplay", "match found"],
    "end_of_game": ["find another", "new match with", "ready to play"],
    "popups": ["ok", "cancel", "close", "next", "reconnect", "menu", "get your", "reputation"],
    "reconnect": "reconnect",
    "account_actions": ["suspended", "banned", "sanction"]
}

# Coords layout
# lobby :
# 0 - play_again
# 1 - operators
# 2 - locker
# 3 - new_gamemode
# 4 - section_1

# queueing :
# 0 - queueing_for_game
# 1 - match_found
# 2 - queueing_reconnect

# end_of_game : 
# 0 - find_new_match
# 1 - new_match_with_squad
# 2 - ready_up

# popups :
# 0 - ok_popup
# 1 - badge_popup
# 2 - reputation_popup
# 2 - big_popup
# 3 - other_popups



# Buttons Coords Layout
# lobby : 
# 0 - return to main menu
# 1 - click on play
# 2 - click on tactical
# 3 - queue for standard
# 4 - queue for standard if the UI menu is different (usually happens if the account is below lvl 10 or below lvl 20)



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

def detect_state(active, mnk):
    state = {
        "in_lobby": False, "queueing": False, "in_game": True, "reconnect": False, "popup": (False, None),
        "end_of_game": False, "squad_leader": False, "ready_up": False, "banned": False, "sanctioned": False
    }
    
    # In Lobby
    state["in_lobby"] = True if read_screenshot(coords["lobby"][0], keywords["in_lobby"][0]) else False

    if not state["in_lobby"]:
        # Banned check
        if read_screenshot(coords["account_actions"], keywords["account_actions"][0]) or read_screenshot(coords["account_actions"], keywords["account_actions"][1]):
            state["banned"] = True
            return state
        # Sanctioned Check
        elif read_screenshot(coords["account_actions"], keywords["account_actions"][2]):
            state["sanctioned"] = True
            return state
        # If all the other checks are False, then do a secondary check to make sure that the account is in the lobby
        elif read_screenshot(coords["lobby"][1], keywords["in_lobby"][1]) or read_screenshot(coords["lobby"][2], keywords["in_lobby"][2]):
            # ^^^ This checks if there's the button that says "New PLaylist Available"
            # Failcheck to ensure that the bot actually isn't in the lobby, if it is, but the layout of the gamemode menu is different, then it will queue a different way
            mnk.select_button(active, button_coords["lobby"][0][0], button_coords["lobby"][0][1], sleep_range=(4, 4.5)) # Bring the user to the main menu
            if read_screenshot(coords["lobby"][3], keywords["in_lobby"][3]) or read_screenshot(coords["lobby"][3], keywords["in_lobby"][4]):
                mnk.select_button(active, button_coords["lobby"][1][0], button_coords["lobby"][1][1], sleep_range=(4, 4.5))
                if read_screenshot(coords["lobby"][4], keywords["in_lobby"][5]):
                    mnk.select_button(active, button_coords["lobby"][2][0], button_coords["lobby"][2][1], sleep_range=(4, 4.5))
                    mnk.select_button(active, button_coords["lobby"][3][0], button_coords["lobby"][3][1], sleep_range=(4, 4.5))
                else:
                    mnk.select_button(active, button_coords["lobby"][4][0], button_coords["lobby"][4][1], sleep_range=(4, 4.5))
                    mnk.select_button(active, button_coords["lobby"][3][0], button_coords["lobby"][3][1], sleep_range=(4, 4.5))
            else:
                state["in_lobby"] = True

    # Queueing 
    state["queueing"] = read_screenshot(coords["queueing"][0], keywords["queueing"][0])
    if not state["queueing"]:
        state["queueing"] = read_screenshot(coords["queueing"][1], keywords["queueing"][1])

    # End of game
    state["end_of_game"] = read_screenshot(coords["end_of_game"][0], keywords["end_of_game"][0])
    if not state["end_of_game"]:
        if read_screenshot(coords["end_of_game"][1], keywords["end_of_game"][1]):
            state["end_of_game"] = True
            state["squad_leader"] = True
        elif read_screenshot(coords["end_of_game"][2], keywords["end_of_game"][2]):
            state["end_of_game"] = True
            state["ready_up"] = True

    # Normal Popup
    state["popup"] = (True, "normal") if read_screenshot(coords["popups"][0], keywords["popups"][0]) else (False, None)
    
    # Badge Popup
    if not state["popup"][0]:
        state["popup"] = (True, "badge") if read_screenshot(coords["popups"][1], keywords["popups"][2]) else (False, None)
    
    # Reputation Popup
    if not state["popup"][0]:
        state["popup"] = (True, "reputation") if read_screenshot(coords["popups"][2], keywords["popups"][7]) else (False, None)

    # Special / Other Popups
    if not state["popup"][0]:
        for x in range(1, len(keywords["popups"])):
            state["popup"] = (True, "special") if read_screenshot(coords["popups"][3], keywords["popups"][x]) else (False, None) # Special popup type
            if not state["popup"][0]:
                state["popup"] = (True, "normal") if read_screenshot(coords["popups"][4], keywords["popups"][x]) else (False, None) # Other popups that weren't caught
            if state["popup"][0]:
                break

    if state["popup"][0]:
        state["in_lobby"] = False
        state["queueing"] = False
        state["in_game"] = False
        state["reconnect"] = False
        state["end_of_game"] = False
        return state
    
    state["reconnect"] = read_screenshot(coords["reconnect"], keywords["reconnect"])
    if state["reconnect"]:
        if not read_screenshot(coords["queueing"][2], keywords["reconnect"]):
            state["reconnect"] = False
    
    for key, value in state.items():
        if value == True:
            if key != "in_game":
                state["in_game"] = False
                break
    return state
