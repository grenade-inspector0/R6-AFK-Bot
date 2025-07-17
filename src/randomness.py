import random
from src.__init__ import get_file_path, POSITIVE_MESSAGES

last_dk_key = None
coord_range = {"maximum_x": 1000, "maximum_y": 1000}

def get_actions():
    actions = []
    last_action = None
    for _ in range(random.randint(3, 8)):
        action_list = ["dk", "dk_shift", "mm", "mm_dk"]
        if last_action == "mm" and "mm" in action_list:
            action_list.remove("mm")
        weights = [1, 3, 1, 2]
        new_action = random.choices(action_list, weights=weights[:len(action_list)], k=1)[0]
        last_action = new_action
        actions.append(new_action)
    if not any(action in ["dk", "dk_shift"] for action in actions):
        guaranteed_action = random.choice(["dk", "dk_shift"])
        actions.insert(random.randint(0, len(actions)), guaranteed_action)
    return actions

def get_coord(coord_type=None):
    return random.randint(1, coord_range["maximum_x"]) if coord_type == "x" else random.randint(1, coord_range["maximum_y"])

def get_direction():
    global last_dk_key
    keys = ["w", "a", "s", "d"]
    keys.remove(last_dk_key) if last_dk_key != None else ""
    key = random.choice(keys)
    last_dk_key = key
    return key

def get_messages(num=1, limit_messages=False):
    messages = []
    # Select the positive messages to choose from
    if limit_messages:
        positive_messages = POSITIVE_MESSAGES
    else:
        positive_messages = [line.strip() for line in open(get_file_path("assets/messages.txt"), 'r').readlines()]
    
    # Randomly selected the inputted number of messages
    for x in range(num):
        new_message = random.choice(positive_messages)
        messages.append(new_message)
    return messages
